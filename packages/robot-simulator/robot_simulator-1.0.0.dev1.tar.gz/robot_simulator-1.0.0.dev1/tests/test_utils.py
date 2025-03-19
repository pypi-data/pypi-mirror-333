import pytest

from robot_simulator.core.utils import update_dict_value


@pytest.fixture
def dictionary():
    return {"key1": 2.4, "key2": "value", "key3": [3, -5, -88]}


def test_update_dict_value(dictionary):
    # Update number value
    update_dict_value(dictionary, "key1", None, 1.33)
    assert dictionary["key1"] == 1.33

    # Update value with unnecessary index
    update_dict_value(dictionary, "key1", 2, -3.5)
    assert dictionary["key1"] == -3.5

    # Update list item with valid index
    update_dict_value(dictionary, "key3", 1, 44)
    assert dictionary["key3"] == [3, 44, -88]

    # Update list item with out of bounds index
    with pytest.raises(IndexError):
        update_dict_value(dictionary, "key3", 3, 3)
    assert dictionary["key3"] == [3, 44, -88]

    # Try to update list item without index
    update_dict_value(dictionary, "key3", None, 4)  # Erase the list
    assert dictionary["key3"] == 4
