import pytest

from xavier.datastructures import MultiValueDict, MultiValueDictKeyError


def test_query_dict():
    data = {'a': [0, 1]}
    qd = MultiValueDict(data)

    assert qd.get('a') == 1
    assert qd['a'] == 1
    assert qd.get('b') is None

    with pytest.raises(MultiValueDictKeyError):
        assert qd['b'] is None

    assert qd.getlist('a') == [0, 1]
    assert qd.getlist('b') == []

    assert 'a' in qd
    assert 'b' not in qd
