import importlib.resources
from pathlib import Path

import h5py
import numpy as np
import pytest

from cr39py.core.ci import SilentPlotting
from cr39py.core.data import data_dir
from cr39py.core.units import unit_registry as u
from cr39py.scan.base_scan import Axis, Scan
from cr39py.scan.cut import Cut
from cr39py.scan.subset import Subset


def test_axis():
    axis = Axis(ind=2, unit=u.um, default_range=(0, 20, 0.5))
    assert axis.ind == 2
    assert axis.unit == u.um
    print(axis.name)

    tracks = np.random.random((100, 6)) * 10
    ax = axis.axis(range=(0, 10))
    ax = axis.axis(range=(None, None), tracks=tracks)
    ax = axis.axis(tracks=tracks)

    axis = Axis(ind=2, unit=u.um, default_range=(None, None, None))
    with pytest.raises(ValueError):
        ax = axis.axis()
    ax = axis.axis(range=(0, 10))
    ax = axis.axis(tracks=tracks)


@pytest.fixture
def cr39scan():
    cpsa_path = data_dir / Path("test/test_alphas.cpsa")
    return Scan.from_cpsa(cpsa_path, etch_time=120)


def test_from_tracks(cr39scan):
    tracks = cr39scan.tracks
    scan2 = Scan.from_tracks(tracks, 120)


def test_framesize(cr39scan):
    # Set with a float
    cr39scan.set_framesize("X", 0.5 * u.cm)
    assert cr39scan.framesize("X") == 0.5 * u.cm

    cr39scan.set_framesize("X", 0.1)
    assert cr39scan.framesize("X") == 0.1 * u.cm

    assert cr39scan.framesize("Y") == cr39scan.framesize("X")
    assert cr39scan.framesize("XY") == cr39scan.framesize("X")

    # Test on a different axis
    cr39scan.set_framesize("D", 0.1 * u.um)
    assert cr39scan.framesize("D") == 0.1 * u.um

    with pytest.raises(KeyError):
        cr39scan.framesize("not a valid axis key")


def test_optimize_xy_framesize(cr39scan):
    cr39scan.optimize_xy_framesize()


def test_get_selected_tracks(cr39scan):

    # Access selected tracks
    cr39scan.selected_tracks
    cr39scan.nselected_tracks

    cr39scan.current_subset.add_cut(Cut(xmin=0))
    cr39scan.current_subset.add_cut(Cut(cmin=30))

    # Get selected tracks again, forcing it to be reset
    cr39scan.selected_tracks

    # Test with all cuts
    x = cr39scan.current_subset.apply_cuts(cr39scan.tracks)

    # Test with subset of cuts
    x = cr39scan.current_subset.apply_cuts(cr39scan.tracks, use_cuts=[0])

    # Test invert
    x = cr39scan.current_subset.apply_cuts(cr39scan.tracks, invert=True)

    # Test with ndslices
    cr39scan.current_subset.set_ndslices(5)
    cr39scan.current_subset.select_dslice(0)
    x = cr39scan.current_subset.apply_cuts(cr39scan.tracks)


def test_subset(cr39scan):

    cr39scan.add_subset()
    cr39scan.add_subset(Subset())

    # Test removing nonexistent subset
    with pytest.raises(ValueError):
        cr39scan.remove_subset(200)

    # Cannot remove current subset
    cr39scan.select_subset(0)
    with pytest.raises(ValueError):
        cr39scan.remove_subset(0)

    # Select the last tubset
    cr39scan.select_subset(-1)

    # Remove the first subset
    cr39scan.remove_subset(0)

    # Cannot select subset outside range
    with pytest.raises(ValueError):
        cr39scan.remove_subset(1000)

    # Cannot access subset outside range
    with pytest.raises(ValueError):
        cr39scan.select_subset(1000)


def test_manipulate_cuts(cr39scan):

    cr39scan.set_domain(xmin=0)
    cr39scan.add_cut(cmin=30)
    cr39scan.add_cut(Cut(dmin=10))

    cr39scan.set_ndslices(2)
    cr39scan.select_dslice(0)

    cr39scan.remove_cut(1)
    cr39scan.replace_cut(0, Cut(cmin=20))


@pytest.mark.parametrize("statistic", ["mean", "median"])
def test_track_energy(cr39scan, statistic):
    cr39scan.track_energy("D", statistic)


@pytest.mark.parametrize(
    "attribute", ["chi", "F2", "track_density", "etch_time", "ntracks"]
)
def test_access_attributes(cr39scan, attribute):
    assert hasattr(cr39scan, attribute)
    getattr(cr39scan, attribute)


def test_rotate(cr39scan):
    cr39scan.rotate(45)


cases = [None, "CHI", "F2", "TRACK DENSITY"]


@pytest.mark.parametrize("quantity", cases)
def test_histogram(cr39scan, quantity):
    cr39scan.histogram(quantity=quantity)


@pytest.mark.parametrize("fcn_name", ["cutplot", "plot", "focus_plot"])
def test_plot_functions(fcn_name, cr39scan):
    with SilentPlotting():
        getattr(cr39scan, fcn_name)()


@pytest.mark.parametrize("ext", [".csv", ".h5", ".png"])
def test_save_histogram(cr39scan, tmp_path, ext):

    # Save the histogram
    path = tmp_path / Path("test_histogram" + ext)
    cr39scan.save_histogram(path)

    # Read the data from the histogram
    if ext == ".h5":
        with h5py.File(path, "r") as f:
            assert "data" in f
            data = f["data"][...]
    elif ext == ".csv":
        data = np.loadtxt(path, delimiter=",")

    elif ext == ".png":
        # Skip the check on the data in this case
        return

    # Get the histogram for reference
    _, _, hist = cr39scan.histogram()

    # Test that the data matches expectations
    assert np.allclose(data, hist, rtol=0.05)
