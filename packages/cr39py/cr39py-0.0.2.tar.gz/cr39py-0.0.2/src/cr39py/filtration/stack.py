"""
The `~cr39py.filtration.stack` module contains the `~cr39py.filtration.stack.Stack` class, which
is used to represent filtration stacks composed of multiple layers of material, represented as
`~cr39py.filtration.layer.Layer` objects.
"""

import numpy as np

from cr39py.core.exportable_class import ExportableClassMixin, saveable_class
from cr39py.core.units import unit_registry as u
from cr39py.filtration.layer import Layer


@saveable_class()
class Stack(ExportableClassMixin):
    r"""
    An ordered list of `~cr39py.filtration.layer.Layer` objects representing a stack of filter materials.

    References
    ----------
    The ion stopping and ranging calculations performed by this clase use
    data from the `SRIM <http://www.srim.org/>`__ code :cite:p:`SRIM`.
    If you use these features, please cite SRIM.
    """

    _exportable_attributes = ["layers"]

    @classmethod
    def from_layers(cls, *args):
        """Creates a stack from a sequence of Layers.

        Each layer should be provided as a separate argument.
        """

        obj = cls()

        # Replace any strings with Layer objects
        _args = []
        for arg in args:
            _arg = Layer.from_string(arg) if isinstance(arg, str) else arg
            _args.append(_arg)

        obj.layers = list(_args)
        return obj

    def add_layer(self, layer: Layer | str):
        """Appends a layer to the stack.

        Parameters
        ----------
        layer : `~cr39py.filtration.layer.Layer` | str
            Layer to add. If a string, it will be converted to a Layer object.
        """
        if isinstance(layer, str):
            layer = Layer.from_string(layer)
        self.layers.append(layer)

    @classmethod
    def from_string(cls, s):
        """
        Create a stack from a comma separated list of Layer strings
        """
        s = s.split(",")
        layers = [Layer.from_string(si) for si in s]
        return cls.from_layers(*layers)

    def __str__(self):
        s = "Stack:\n"
        for l in self.layers:
            s += str(l) + "\n"
        return s

    def __eq__(self, other):
        if self.nlayers != other.nlayers:
            return False

        for i in range(self.nlayers):
            if self.layers[i] != other.layers[i]:
                return False
        return True

    @property
    def nlayers(self):
        return len(self.layers)

    @property
    def nactive(self):
        r"""
        The number of layers in the stack marked 'active'
        """
        return len([layer for layer in self.layers if layer.active])

    @property
    def thickness(self):
        r"""
        The total thickness of the stack.
        """
        thickness = np.array([layer.thickness.m_as(u.mm) for layer in self.layers])
        return np.sum(thickness) * u.mm

    def range_down(
        self,
        particle,
        E_in,
        dx=1 * u.um,
    ):
        """
        Calculate the energy a particle will be ranged down to through the stack.

        Parameters
        ----------
        particles : Particle
            Incident particle

        E_in : u.Quantity
            Initial energy of incident particle

        dx : u.Quantity, optional
            The spatial resolution of the numerical integration of the
            stopping power. Defaults to 1 μm.

        Returns
        -------

        E_out : u.Quantity
            Energy of the particle after leaving the stack. If zero, the
            particle stopped in the stack.

        """
        E = E_in

        for l in self.layers:

            E = l.range_down(particle, E, dx=dx)

            if E <= 0 * E.u:
                return 0 * E.u
        return E

    def reverse_ranging(
        self,
        particle,
        E_out,
        dx=1 * u.um,
        max_nsublayers=None,
    ):
        """
        Calculate the energy of a particle before ranging in the stack
        from its energy after the stack.

        Parameters
        ----------
        particle: str
            Incident particle

        E_out : u.Quantity
            Energy of the particle after the stack.

        dx : u.Quantity, optional
            The spatial resolution of the numerical integration of the
            stopping power. Defaults to 1 μm.

        Returns
        -------

        E_in : u.Quantity
            Energy of the particle before entering the stack.

        """
        E = E_out

        for l in self.layers[::-1]:

            E = l.reverse_ranging(particle, E, dx=dx)

        return E

    def ranging_energy_loss(
        self, particle: str, E_in: u.Quantity, dx=1 * u.um
    ) -> u.Quantity:
        """
        Calculate the energy a particle will lose in the stack.

        Parameters
        ----------

        particles : str
            Incident particle

        E_in : u.Quantity
            Energy of the particle before the stack.


        dx : u.Quantity
            The spatial resolution of the numerical integration of the
            stopping power. Defaults to 1 μm.


        Returns
        -------

        E_in_stack : u.Quantity
            Energy the particle leaves in the stack.

        """
        return E_in - self.range_down(particle, E_in, dx=dx)

    def lateral_straggle(self, particle: str, E_in: u.Quantity) -> u.Quantity:
        """
        Calculate the lateral straggle of a particle in the stack.

        If the particle passes through the stack, this is the straggle experienced by the particle in the stack.
        If the particle stops in the stack, this is the total straggle up to the stopping point.

        This model assumes that the lateral straggle is additive in each layer.

        See the `~cr39py.filtration.srim.SRIMData` class for formal definition of this quantity.

        Parameters
        ----------
        particle : str
            Incident particle

        E_in : u.Quantity
            Energy of the particle before ranging in the stack.

        Returns
        -------
        straggle : u.Quantity
            Lateral straggle of the particle in the stack.
        """
        straggle = 0 * u.um
        for l in self.layers:
            straggle += l.lateral_straggle(particle, E_in)

            # Range down the particle energy before calculating straggle in the next layer
            E_in = l.range_down(particle, E_in)

            # If the particle has stopped, return the accumulated straggle
            if E_in.m <= 0:
                return straggle

        return straggle
