"""Test model_s."""
# pylint: disable=broad-except
from hf_model_s_cpu import model_s


def test_model_s():
    """Test model_s."""
    list1 = ["test", "测试", "love"]
    list2 = ["this is a test"]
    # cmat = gradio_cmat(list1, list2)

    model = model_s()
    vec1 = model.encode(list1)
    vec2 = model.encode(list2)
    cmat = vec1.dot(vec2.T)
    assert cmat.shape == (3, 1)

    assert cmat[0, 0] > 0.6
    assert cmat[1, 0] > 0.6
    assert cmat[2, 0] < 0.2
