# Dictation: Annotated Python Dictionaries

The Dictation library compliments Python's built-in `dict` data type by offering a fully
compatible subclass, `dictation`, which adds support for annotations – a way to carry
additional metadata within – yet separate from – the data held in the dictionary itself.

The `dictation` dictionary type also automatically assigns parent relationships to all
child dictionaries, which is useful to have access to in some data processing scenarios,
whether or not these are used in addition to the library's annotation capabilities.

The ability to assign annotations, or keep track of parent relationships for child nodes
of a nested dictionary structure can be useful where one can not modify the structure or
data held in a dictionary, because doing so could render it incompatible for some uses.

As the `dictation` data type is compatible with the built-in `dict` data type, it should
be usable anywhere an ordinary `dict` instance can be used.

The `dictation` library name is a portmanteau of `dic-tionary` and `anno-tation`.

### Requirements

The Dictation library has been tested with Python 3.9, 3.10, 3.11, 3.12 and 3.13 but may
work with some earlier versions such as 3.8 but has not been tested against this version
or any earlier. The library is not compatible with Python 2.* or earlier.

### Installation

The Dictation library is available from PyPI so may be added to a project's dependencies
via its `requirements.txt` file or similar by referencing the Dictation library's name,
`dictation`, or the library may be installed directly into the local runtime environment
using `pip install` by entering the following command, and following any prompts:

	$ pip install dictation

### Class Methods & Properties

The Dictation library's `dictation` class is a subclass of the built-in `dict` class, so
all of the built-in functionality of `dict` is available, as well as several additional
class methods and properties as documented below:

* `annotate(recursive: bool = False, **kwargs)` – The `annotate()` method can be used to
assign one or more annotations to the current `dictation` instance provided as key-value
pairs; these are held separately from and do not interfere with the actual data held in
the dictionary. The `recursive` keyword is reserved for specifying if the annotations
provided will be marked as being recursively available for the current node as well as
for any nested child nodes, when `recursive` is set to `True` – when `recursive` is set
to `False` (or simply when the `recursive` argument is not specified), the annotations
will only available for the current node. Additionally, the `annotate()` method returns
`self` upon completion so calls to `annotate()` can be chained with calls to other class
methods, such as the `get()` method.

* `unannotate(name: str) -> dictation` – The `unannotate()` method provides support for
removing a named annotation from the current node; it cannot remove any annotations that
have been inherited from ancestors in the hierarchy; to remove a recursive annotation,
it must be removed directly from the `dictation` ancestor node it was assigned to.

* `annotation(name: str, default: object = None, recursive: bool = True) -> object` –
The `annotation()` method supports recursively obtaining a named annotation value. If
the named annotation cannot be found, the `default` value will be returned if one has
been provided, and if not, the `None` value will be returned.

* `annotations (getter) -> dict[str, object]` – The `annotations` getter returns the
annotations, if any, assigned to the current `dictation` node, or inherited from any
ancestors, where those annotations were assigned and set as being recursively available.

* `annotations (setter) <- dict[str, object]` – The `annotations` setter supports
assigning one or more annotations, specified as a dictionary of key-value pairs, to the
current `dictation` node. Annotations applied via the `annotations` setter only apply to
the current `dictation` node as they are not assigned as being recursively available to
any child nodes. If an annotation needs to be made available to the current node as well
as recursively to any child nodes, it must be set via the `annotate()` method instead,
which provides control over the recursive availability of the annotation being assigned.

* `parent (getter) -> dictation | None` – The `parent` property returns a reference to
the current `dictation` instance's parent, if available, otherwise `None` is returned.

* `set(key: object, value: object) -> dictation` – The `set()` method is a compliment to
the built-in `dict` class' `get` method. The `set()` method accepts the usual key and
value as method keyword arguments, and assigns the value to the current `dictation`
instance at the provided key. Additionally, the `set()` method returns `self` upon
completion, so calls to `set()` can be chained with calls to other class methods, such
as the `annotate()` method.

* `data(metadata: bool = False, annotations: bool = False) -> dict` – The `data()`
method supports generating a dictionary representation of the dictation's data, as well
as optionally including associated metadata such as the parent reference, any assigned
annotation values, and typing information for each value.

* `print(indent: int = 0)` – The `print()` method supports generating a print-out of the
`dictation` instance's data as well as any annotations which can be useful for debugging
and data visualisation purposes.


### Usage Demonstration

To use the Dictation library, simply import it and use the library's `dictation` class
as a replacement of, or compliment to, the built-in `dict` class:

```python
from dictation import dictation

# Create a new `dictation` class instance with example data and add a few annotations:
sample = dictation(a=1, b=2, c=3).annotate(x=4, y=5)

# Check that the data held by the `dictation` instance is as expected; note that as
# the `dictation` class is a subclass of the `dict` class, that the two assertions below
# comparing against another `dictation` instance as well as a `dict` instance are valid:
assert sample == dictation(a=1, b=2, c=3)
assert sample == dict(a=1, b=2, c=3)

# Check that the annotation data held by the `dictation` instance is as expected; note
# that the annotations are held completely separately from the dictionary's data:
assert sample.annotations == dictation(x=4, y=5)
assert sample.annotations == dict(x=4, y=5)

# Modify the example annotation, "y", and add an annotation, "z", making both recursive:
sample.annotate(y=0, z=6.789, recursive=True)

# Check that the updates to the annotations are as expected:
assert sample.annotations == dictation(x=4, y=0, z=6.789)

# Attempt to obtain a named annotation; this works like the `dict` class' `get` method
# whereby if the annotation is found, it's value will be returned, otherwise the default
# value, if specified, will be returned, otherwise `None` will be returned instead:
assert sample.annotation("z") == 6.789

# An annotation named "v" does not exist, so the provided default is returned:
assert sample.annotation("v", default=8) == 8

# An annotation named "v" does not exist, nor is there a default, so `None` is returned:
assert sample.annotation("v") is None

# Add a new child dictionary to the current `dictation` instance, note that the child
# dictionary will be converted to a new `dictation` instance as will any of its nested
# child dictionaries:
sample["d"] = dict(e=5, f=6)

assert isinstance(sample["d"], dict)
assert isinstance(sample["d"], dictation)

# Check that the `sample` dictionary has the expected structure and data:
assert sample == dict(a=1, b=2, c=3, d=dict(e=5, f=6))

# Check that the nested dictionary, "d", has the expected annotations; as no annotations
# have currently been assigned directly to the nested dictionary "d", it will only have
# inherited recursive annotations assigned to its parent and their parents. As per this
# example code, it currently means that the inherited annotations consist of "y" and "z"
# which were assigned to the parent dictionary, `sample`, and as they were both marked
# as recursive annotations, they are available to any nested children, including to "d":
assert sample["d"].annotations == dict(y=0, z=6.789)

# The `dictation` library also supports assigning annotations as attributes; annotations
# added as attributes cannot use the same name as any of the class' inherent attributes,
# properties or methods however; attempting to assign an attribute using the name of an
# inherent class` attribute will raise an exception. So long as the annotation names are
# distinct, annotations can easily be assigned and retrieved using attribute accessors:
sample.greeting = "hello"

# Check that the annotation, "greeting", has the expected value
assert sample.greeting == "hello"

# Annotations assigned via attributes are stored identically as annotations assigned to
# a `dictation` instance in any other way, so they can all be accessed interchangeably:
assert sample.annotation("greeting") == "hello"

# Annotations assigned via the `annotate()` method can also be accessed as attributes:
assert sample.x == 4
assert sample.y == 0
assert sample.z == 6.789

# All annotations assigned to a node can be accessed as a dictionary representation via
# the `annotations` property, which returns a `dict` instance holding the annotations:
assert sample.annotations == dict(x=4, y=0, z=6.789, greeting="hello")

# Regardless of how annotations are assigned to the `dictation` instance, they can be
# accessed, modified or removed by any of the other methods; for example, annotations
# can be removed using the `unannotate()` method, which returns `self` on completion
# so can be chained:
assert sample.unannotate("y").annotations == dict(x=4, z=6.789, greeting="hello")

# The `del` language keyword can also be used to remove previously assigned annotations:
del sample.z

assert sample.annotations == dict(x=4, greeting="hello")
```

Please Note: Like any subclass of the built-in `dict` type, instances of the `dictation`
class can not be created directly via Python's dictionary-literal `{...}` syntax, rather
they must be instantiated using the `dictation` class constructor. One can however wrap
any `{}` dictionary literal, as well as variables holding a `dict`, with a `dictation`
class constructor to convert any regular `dict` to a `dictation` class instance:

```python
from dictation import dictation

# The Python dictionary-literal syntax can only create `dict` instances:
sample = {"a": 1, "b": 2, "c": 3}
assert isinstance(sample, dictation) is False
assert isinstance(sample, dict) is True
assert sample == {"a": 1, "b": 2, "c": 3}

# So the `dictation` class constructor must be used to create all `dictation` instances,
# however, the `dictation` constructor can take a dictionary literal as input:
sample = dictation({"a": 1, "b": 2, "c": 3})
assert isinstance(sample, dictation) is True
assert isinstance(sample, dict) is True
assert sample == {"a": 1, "b": 2, "c": 3}

# Furthermore, variables holding regular `dict` values, whether created via the literal
# syntax or via the `dict` class constructor syntax...
sample = {"x": 7, "y": 8, "z": 9}
assert isinstance(sample, dictation) is False
assert isinstance(sample, dict) is True
assert sample == {"x": 7, "y": 8, "z": 9}

sample = dict(sample)
assert isinstance(sample, dictation) is False
assert isinstance(sample, dict) is True
assert sample == {"x": 7, "y": 8, "z": 9}

# ...can be passed to the `dictation` class constructor to cast to a `dictation` class:
sample = dictation(sample)
assert isinstance(sample, dictation) is True
assert isinstance(sample, dict) is True
assert sample == {"x": 7, "y": 8, "z": 9}
```

One may also pass additional key-value pairs to the `dictation` class constructor during
casting. These additional key-value pairs will overwrite any matching existing keys with
the newly assigned values, as well as adding new key-value pairs to the dictionary for
keys that have not yet been defined:

```python
from dictation import dictation

base = dict(a=1, b=2, c=3)
assert base == dict(a=1, b=2, c=3)

sample = dictation(base, c=4, x=7, y=8, z=9)  # "c" is being redefined with a value of 4

assert sample == dictation(a=1, b=2, c=4, x=7, y=8, z=9)
assert sample == dict(a=1, b=2, c=4, x=7, y=8, z=9)
```

### Contributing & Local Development

To carry out development of the Dictation library, create a fork of the repository from
the GitHub account, then clone a copy of the fork to the local machine for development
and testing:

```
$ cd path/to/local/development/directory
$ git clone git@github.com:<username>/dictation.git
```

Then create a new feature/development branch, using a descriptive name for the branch:

```
$ cd path/to/local/development/directory/dictation
$ git checkout -b new_feature_branch
```

#### Code Linting

The Dictation library adheres to the code formatting specifications detailed in PEP-8,
which are verified and applied by the _Black_ code formatting tool. When code changes
are made to the library, one needs to ensure that the code conforms to these code
formatting specifications. To simplify this, the provided `Dockerfile` creates an image
that supports running _Black_ against the latest version of the code, and will report if
any issues are found. To run the code formatting checks, perform the following commands,
which will build the Docker image and then run the formatting checks:

```
$ docker compose build
$ docker compose run black
```

If any code formatting issues are found, they will be reported by _Black_. It is also
possible to run _Black_ so that it will automatically reformat the affected files; this
can be achieved as follows, by passing the `--verbose` flag, which allows _Black_ to
report which files:

```
$ docker compose run black --verbose
```

The above will reformat any library source and unit test files that contain formatting
issues, and will report which changes are made.

#### Unit Tests

The Dictation library includes a suite of comprehensive unit tests which ensure that the
library functionality operates as expected. The unit tests were developed with and are
run via `pytest`.

To ensure that the unit tests are run within a predictable runtime environment where all
of the necessary dependencies are available, a [Docker](https://www.docker.com) image is
created within which the tests are run. To run the unit tests, ensure Docker and Docker
Compose are [installed](https://docs.docker.com/engine/install/), and run the commands
listed below, which will build the Docker image via `docker compose build` and then run
the tests via `docker compose run tests` – the output of the tests will be displayed:

```
$ docker compose build
$ docker compose run tests
```

To run the unit tests with optional command line arguments being passed to `pytest`,
append the relevant arguments to the `docker compose run tests` command, as follows, for
example passing `-v` to enable verbose output or `-s` to print standard output:

```
$ docker compose run tests -v -s
```

See the documentation for [PyTest](https://docs.pytest.org/en/latest/) regarding the
available optional command line arguments.

### Copyright & License Information

Copyright © 2024–2025 Daniel Sissman; licensed under the MIT License.