"""Test gen_cmat, aset2pairs."""
from aset2pairs import aset2pairs
from cmat2aset import cmat2aset

from radio_mlbee.gen_cmat import gen_cmat
from radio_mlbee.loadtext import loadparas

paras1 = loadparas("radio_mlbee/data/sternstunden04-en.txt")
paras2 = loadparas("radio_mlbee/data/sternstunden04-de.txt")
cmat = gen_cmat(paras1, paras2)


def test_gen_cmat_sternstunden04():
    """Test gen_cmat sternstunden04."""
    len1, len2 = len(paras1), len(paras2)

    # note the order
    assert cmat.shape == (len2, len1)


def test_aset2pairs():
    """Test aset2pairs."""
    aset = cmat2aset(cmat)
    pairs = aset2pairs(paras1, paras2, aset)

    assert "Marseillaise" in pairs[2][0]
    assert "Marseillaise" in pairs[2][1]
    assert pairs[2][2] > 0.95
