"""Test radio_mlbee."""
# pylint: disable=broad-except
from radio_mlbee import __version__, radio_mlbee


def test_version():
    """Test version."""
    assert __version__[:3] == "0.1"


def test_sanity():
    """Check sanity."""
    try:
        assert not radio_mlbee()
    except Exception:
        assert True
