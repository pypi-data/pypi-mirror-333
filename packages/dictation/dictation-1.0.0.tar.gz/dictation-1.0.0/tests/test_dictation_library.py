import pytest
import enum
import copy

from dictation import (
    dictation,
    AnnotationError,
)


def test_dictation_argument_instantiation():
    """Ensure that a dictation dictionary can be created and accessed as expected"""

    # Define a sample source data set as a regular built-in Python dictionary
    source = {
        "x": 1,
        "y": 2,
        "z": 3,
    }

    # Instantiate a new dictation dictionary with the contents of the source dictionary
    sample = dictation(source)

    # Confirm that the newly created dictation dictionary conforms to expectations
    assert isinstance(sample, dict)
    assert isinstance(sample, dictation)

    # Check that the expected length matches
    assert len(sample) == 3

    # Check that the dictation contains the expected keys, values, and items
    assert list(sample.keys()) == ["x", "y", "z"]
    assert list(sample.values()) == [1, 2, 3]
    assert list(sample.items()) == [("x", 1), ("y", 2), ("z", 3)]

    # Check that the dictation compares as expected with a regular dictionary
    assert sample == dict(x=1, y=2, z=3)

    # Check that the dictation compares as expected with another dictation dictionary
    assert sample == dictation(x=1, y=2, z=3)


def test_dictation_keword_argument_instantiation():
    """Ensure that the dictation dictionary can be instantiated as expected"""

    # Instantiate a new instance using keyword arguments to define the key-value pairs
    sample = dictation(x=1, y=2, z=3)

    # Confirm that the newly created dictation dictionary conforms to expectations
    assert isinstance(sample, dict)
    assert isinstance(sample, dictation)
    assert len(sample) == 3
    assert list(sample.keys()) == ["x", "y", "z"]
    assert list(sample.values()) == [1, 2, 3]
    assert list(sample.items()) == [("x", 1), ("y", 2), ("z", 3)]

    # The annotations can be retrieved from the dictation instance in a dictionary
    assert isinstance(sample.annotations, dict)

    # Newly instantiated dictation dictionaries do not have any annotations
    assert len(sample.annotations) == 0

    # Add the first test annotation ("a") using the annotate method
    sample.annotate(a=1)

    # Check that the new annotation is reflected in the annotation count
    assert len(sample.annotations) == 1

    # Check that the first test annotation ("a") has been successfully added
    assert hasattr(sample, "a") is True

    # Check that the first test annotation ("a") has the expected value
    assert sample.annotation("a") == 1
    assert sample.a == 1

    assert sample.annotations == dict(a=1)

    # Add the second test annotation ("b") using the annotate method
    sample.annotate(b=2)

    # Check that the new annotation is reflected in the annotation count
    assert len(sample.annotations) == 2

    # Check that the second test annotation ("b") has been successfully added
    assert hasattr(sample, "b") is True

    # Check that the second test annotation ("b") has the expected value
    assert sample.annotation("b") == 2
    assert sample.b == 2

    assert sample.annotations == dict(a=1, b=2)

    # Add the third test annotation using the attribute-assignment syntax
    sample.c = 3

    # Check that the third test annotation ("c") has been successfully added
    assert hasattr(sample, "c") is True

    # Check the assigned test annotations against a dictionary representation
    assert sample.annotations == dict(a=1, b=2, c=3)

    # Check the assigned test annotations using the attribute accessor syntax
    assert sample.a == 1
    assert sample.b == 2
    assert sample.c == 3

    # Delete the third test annotation using the standard attribute deletion syntax
    del sample.c

    # Check that the third test annotation has been successfully removed
    assert hasattr(sample, "c") is False


def test_dictation_combined_argument_and_keword_argument_instantiation():
    """Ensure that the dictation dictionary can be instantiated as expected"""

    source = {
        "a": 1,
        "b": 2,
        "c": 3,
    }

    sample = dictation(source, d=4, e=5)

    # Confirm that the newly created dictation dictionary conforms to expectations
    assert isinstance(sample, dict)
    assert isinstance(sample, dictation)
    assert len(sample) == 5
    assert list(sample.keys()) == ["a", "b", "c", "d", "e"]
    assert list(sample.values()) == [1, 2, 3, 4, 5]
    assert list(sample.items()) == [("a", 1), ("b", 2), ("c", 3), ("d", 4), ("e", 5)]

    # Newly instantiated dictation dictionaries do not have any annotations
    assert len(sample.annotations) == 0

    # Add a new annotation
    sample.annotate(a=1)

    # Check that the annotation is reflected in the annotation count
    assert len(sample.annotations) == 1


def test_nested_dictation_instantiation():
    """Ensure that the dictation dictionary can be instantiated as expected"""

    source = {
        "a": {
            "b": {
                "c": 1,
            }
        },
        "d": 4,
    }

    # Instantiate a new dictation dictionary using the data provided in source
    sample = dictation(source)

    # Confirm that the newly created dictation dictionary conforms to expectations
    assert isinstance(sample, dict)
    assert isinstance(sample, dictation)
    assert len(sample) == 2
    assert list(sample.keys()) == ["a", "d"]
    assert list(sample.values()) == [{"b": {"c": 1}}, 4]
    assert list(sample.items()) == [("a", {"b": {"c": 1}}), ("d", 4)]

    assert isinstance(sample.annotations, dict)

    # Newly instantiated dictation dictionaries do not have any annotations
    assert len(sample.annotations) == 0

    # Add the first test annotation ("a") using the annotate method
    sample.annotate(a=1)

    # Check that the new annotation is reflected in the annotation count
    assert len(sample.annotations) == 1

    # Check that the first test annotation ("a") has been successfully added
    assert hasattr(sample, "a") is True

    # Check that the first test annotation ("a") has the expected value
    assert sample.annotations == dict(a=1)
    assert sample.annotation("a") == 1
    assert sample.a == 1

    # Add the second test annotation ("b") using the annotate method
    sample.annotate(b=2)

    # Check that the new annotation is reflected in the annotation count
    assert len(sample.annotations) == 2

    # Check that the second test annotation ("b") has been successfully added
    assert hasattr(sample, "b") is True

    # Check that the second test annotation ("b") has the expected value
    assert sample.annotations == dict(a=1, b=2)
    assert sample.annotation("b") == 2
    assert sample.b == 2

    # Add the third test annotation using the attribute-assignment syntax
    sample.c = 3

    # Check that the third test annotation ("c") has been successfully added
    assert hasattr(sample, "c") is True

    # Check the assigned test annotations against a dictionary representation
    assert sample.annotations == dict(a=1, b=2, c=3)

    # Check the assigned test annotations using the attribute accessor syntax
    assert sample.a == 1
    assert sample.b == 2
    assert sample.c == 3

    # Delete the third test annotation using the standard attribute deletion syntax
    del sample.c

    # Check that the third test annotation has been successfully removed
    assert hasattr(sample, "c") is False

    sample["a"]["b"].annotate(d=4, recursive=True)


def test_nested_dictation_annotation():
    source = {
        "a": {
            "b": 1,
        },
        "c": 2,
    }

    sample = dictation(source)

    assert isinstance(sample, dict)
    assert isinstance(sample, dictation)
    assert len(sample) == 2
    assert len(sample.keys()) == 2
    assert len(sample.values()) == 2
    assert list(sample.keys()) == ["a", "c"]
    assert list(sample.values()) == [{"b": 1}, 2]
    assert list(sample.items()) == [("a", {"b": 1}), ("c", 2)]

    assert sample == source
    assert dict(sample) == source
    assert dictation(sample) == source

    assert len(sample.annotations) == 0

    zample = copy.copy(sample)
    zample = copy.deepcopy(sample)

    sample.x = 123

    assert sample.x == 123
    assert sample.annotations == dict(x=123)

    sample.annotate(y=456, recursive=True)
    sample.annotate(z=789, recursive=False)

    assert sample["a"] == {"b": 1}
    assert len(sample["a"].annotations) == 1
    assert sample["a"].annotations == dict(y=456)

    sample["a"].annotate(x=321)

    assert sample["a"].annotation("x") == 321
    assert sample["a"].x == 321

    assert len(sample["a"].annotations) == 2
    assert sample["a"].annotations == dict(x=321, y=456)


def test_type(sampleA: dictation, sampleB: dictation):
    """Ensure that dictation instances are valid `dict` and `dictation` classes by
    checking their inheritance hierarchy conforms to that which is expected"""

    assert isinstance(sampleA, dict)
    assert isinstance(sampleA, dictation)
    assert isinstance(sampleB, dict)
    assert isinstance(sampleB, dictation)


def test_type_equivalence(sampleA: dictation, sampleB: dictation):
    """Ensure that the sample dictation classes conform to their expected equivalence"""

    assert sampleA is sampleA
    assert sampleA is not sampleB
    assert sampleB is sampleB
    assert sampleB is not sampleA


def test_dictation_length(sampleA: dictation):
    """Ensure that the dictation dictionary reports its length correctly"""

    assert len(sampleA) == 3


def test_dictation_key_values(sampleA: dictation):
    """Ensure that the dictation dictionary key-values are as expected"""

    assert sampleA == {
        "a": 1,
        "b": 2,
        "c": 3,
    }


def test_dictation_keys_and_key_order(sampleA: dictation):
    """Ensure that the dictation dictionary reports its item keys correctly"""

    # We must cast the Python internal `dict_keys` type to `list` for the comparison
    assert list(sampleA.keys()) == ["a", "b", "c"]


def test_dictation_values_and_values_order(sampleA: dictation):
    """Ensure that the dictation dictionary reports its item keys correctly"""

    # We must cast the Python internal `dict_values` type to `list` for the comparison
    assert list(sampleA.values()) == [1, 2, 3]


def test_dictation_contains(sampleA: dictation):
    """Ensure that the dictation dictionary reports its contains status correctly"""

    assert "a" in sampleA
    assert "b" in sampleA
    assert "c" in sampleA


def test_dictation_does_not_contain(sampleA: dictation):
    """Ensure that the dictation dictionary reports its contains status correctly"""

    assert not "d" in sampleA
    assert not "e" in sampleA


def test_dictation_dictionary_and_annotation_contents(sampleB: dictation):
    """Ensure that the dictation dictionary and annotation values are as expected"""

    assert isinstance(sampleB, dict)
    assert isinstance(sampleB, dictation)

    assert len(sampleB) == 3
    assert len(sampleB.keys()) == 3
    assert list(sampleB.keys()) == ["a", "b", "c"]
    assert len(sampleB.values()) == 3
    assert list(sampleB.values()) == [1, 2, 3]
    assert len(sampleB.items()) == 3
    assert list(sampleB.items()) == [("a", 1), ("b", 2), ("c", 3)]

    assert sampleB == {
        "a": 1,
        "b": 2,
        "c": 3,
    }

    assert sampleB["a"] == 1
    assert sampleB["b"] == 2
    assert sampleB["c"] == 3

    assert isinstance(sampleB.annotations, dict)
    assert len(sampleB.annotations) == 2
    assert len(sampleB.annotations.keys()) == 2
    assert list(sampleB.annotations.keys()) == ["d", "e"]
    assert list(sampleB.annotations.values()) == [4, 5]
    assert len(sampleB.annotations.items()) == 2
    assert list(sampleB.annotations.items()) == [("d", 4), ("e", 5)]

    assert sampleB.annotations == {
        "d": 4,
        "e": 5,
    }

    assert sampleB.d == 4
    assert sampleB.e == 5

    assert sampleB.annotation("d") == 4
    assert sampleB.annotation("e") == 5


def test_dictation_annotation_with_reserved_word_name(sampleA: dictation):
    """Ensure that annotations with reserved word names cannot be set, and instead cause
    an AnnotationError exception to be raised"""

    with pytest.raises(AnnotationError) as exception:
        # Attempt to set an annotation with a reserved name
        sampleA.recursive = "abc"

        # Expect the AnnotationError exception to be raised
        assert str(exception).startswith(
            "Annotations cannot use any of the following reserved word names:"
        )


def test_dictation_annotation_that_does_not_exist(sampleA: dictation):
    """Ensure that attempted access to annotations (via attribute accessors) that do not
    exist on the current dictation instance, or recursively, raise an AttributeError"""

    with pytest.raises(AttributeError) as exception:
        assert sampleA.annotation_that_does_not_exist is None

        assert (
            str(exception)
            == "AttributeError: The attribute 'annotation_that_does_not_exist' does not exist!"
        )


def test_dictation_items_iteration(sampleA: dictation, sampleB: dictation):
    """Ensure that iterating over the dictation's items produces the expected results"""

    # Test the 'sampleA' dictation instance
    values = {}

    for key, value in sampleA.items():
        values[key] = value

    # sampleA defined in conftest.py has three options
    assert len(values) == 3

    assert values == {
        "a": 1,
        "b": 2,
        "c": 3,
    }

    annotations = {}

    for key, value in sampleA.annotations.items():
        annotations[key] = value

    # sampleA defined in conftest.py does not have any annotations
    assert len(annotations) == 0

    # Test the 'sampleB' dictation instance

    values = {}

    for key, value in sampleB.items():
        values[key] = value

    # sampleB defined in conftest.py has three values
    assert len(values) == 3

    assert values == {
        "a": 1,
        "b": 2,
        "c": 3,
    }

    annotations = {}

    for key, value in sampleB.annotations.items():
        annotations[key] = value

    # sampleB defined in conftest.py has two annotations
    assert len(annotations) == 2

    # Compare annotation key-values
    assert annotations == {
        "d": 4,
        "e": 5,
    }
