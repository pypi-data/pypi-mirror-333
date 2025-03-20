import pytest
import pickle

from dictation import (
    dictation,
    AnnotationError,
)


def test_dictation_pickling_and_unpickling():
    """Test the pickling and unpickling of dictation instances"""

    # Create dictation instance for testing with several key-value pairs and annotations
    info = dictation(a=1, b=2, c=3).annotate(x=7, y=8, z=9)

    # Check that the instance is of the expected types
    assert isinstance(info, dict)
    assert isinstance(info, dictation)

    # Check that the instance contains the expected number of key-value pairs
    assert len(info) == 3

    # Check that the instance contains the expected data keys and values
    assert info == dict(a=1, b=2, c=3)
    assert info == dictation(a=1, b=2, c=3)

    # Check that the instance contains the expected data keys and values via regular
    # keyed access, comparing the values to those set above
    assert info["a"] == 1
    assert info["b"] == 2
    assert info["c"] == 3

    # Check that the instance contains the expected data keys and values via get method
    assert info.get("a") == 1
    assert info.get("b") == 2
    assert info.get("c") == 3
    assert info.get("d") is None  # The "d" key-value has not been set, so expect None

    # Add/update a key-value pair, in this case, adding the new key, "d", and value of 4
    assert info.set("d", 4)

    # Check that the instance contains the expected number of annotations
    assert len(info.annotations) == 3

    # Check that the instance contains the expected annotation keys/names and values
    assert info.annotations == dict(x=7, y=8, z=9)
    assert info.annotations == dictation(x=7, y=8, z=9)

    # Annotations are also available as attributes on the dictation instance
    assert info.x == 7
    assert info.y == 8
    assert info.z == 9

    # Pickle the dictation dictionary for storage, transmission or other purposes
    pickled = pickle.dumps(info)

    # Check that the pickled instance has been converted to a bytes representation
    assert isinstance(pickled, bytes)

    # Un-pickle the pickled dictation dictionary, restoring its state
    info = pickle.loads(pickled)

    # Check that the instance is of the expected types
    assert isinstance(info, dict)
    assert isinstance(info, dictation)

    # Check that the instance contains the expected number of key-value pairs
    assert len(info) == 4

    # Check that the instance contains the expected data keys and values, noting that
    # an additional key-value pair, d == 4, was added after the instance's creation
    assert info == dict(a=1, b=2, c=3, d=4)
    assert info == dictation(a=1, b=2, c=3, d=4)

    # Check that the instance contains the expected number of annotations
    assert len(info.annotations) == 3

    # Check that the instance contains the expected annotation keys/names and values
    assert info.annotations == dict(x=7, y=8, z=9)
    assert info.annotations == dictation(x=7, y=8, z=9)

    # Annotations are also available as attributes on the dictation instance
    assert info.x == 7
    assert info.y == 8
    assert info.z == 9
