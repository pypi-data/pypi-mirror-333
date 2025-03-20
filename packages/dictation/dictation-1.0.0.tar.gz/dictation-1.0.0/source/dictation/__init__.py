from __future__ import annotations

import logging
import copy


logger = logging.getLogger(__name__)


class AnnotationError(AttributeError):
    """Error for alerting the absence of or inability to set the requested annotation"""

    pass


class dictation(dict):
    """Annotated dictionary type supports one or more annotation stored alongside the
    standard dictionary key-value pairs, as well as automatic hierarchical links between
    root and child dictionary nodes allowing for annotations to be defined and gathered
    hierarchically from a given child dictionary node upwards to the root node."""

    _reserved: list[str] = ["recursive"]

    class _annotation(object):
        """The _annotation class holds an annotation value and its recursive state"""

        def __init__(self, value: object, recursive: bool = True):
            self._value = value

            if not isinstance(recursive, bool):
                raise TypeError("The 'recursive' argument must have a boolean value!")

            self._recursive = recursive

        @property
        def value(self) -> object | None:
            """Return the annotation class' stored value"""

            return self._value

        @value.setter
        def value(self, value: object):
            """The annotation value can only be set during class construction"""

            raise NotImplementedError

        @property
        def recursive(self) -> bool:
            """Return the annotation class' stored recursive state"""

            return self._recursive

        @recursive.setter
        def recursive(self, recursive: bool):
            """The recursive value can only be set during class construction"""

            raise NotImplementedError

        @property
        def data(self) -> dict[str, object]:
            """Provide access to the annotation in the form of a dictionary"""

            return dict(value=self.value, recursive=self.recursive)

    def __init__(self, *args, parent: dictation = None, **kwargs):
        """Initialize a `dictation` instance, which as a subclass of `dict` supports the
        same instantiation patterns as a standard `dict` class for compatibility"""

        super().__init__()

        self._special: list[str] = sorted(
            self.__class__._reserved
            + [attr for attr in dir(self) if not attr.startswith("_")]
        )

        self._annotations: dict[str, annotation] = {}

        self._parent: dictation = None

        if parent is None:
            pass
        elif isinstance(parent, dictation):
            self._parent = parent
        else:
            raise TypeError(
                "The 'parent' argument, if set, must have a `dictation` instance value!"
            )

        # Iterate through any args
        for arg in args:
            if isinstance(arg, (dict, dictation)):
                for key, value in arg.items():
                    self[key] = value

                if isinstance(arg, dictation):
                    if isinstance(annotations := arg._annotations, dict):
                        for name, annotation in annotations.items():
                            self._annotations[name] = self._annotation(
                                value=annotation.value,
                                recursive=annotation.recursive,
                            )

                    if isinstance(parent := arg.parent, dictation):
                        self._parent = parent

        for key, value in kwargs.items():
            self[key] = value

        def transform(source: object, parent: dictation = None) -> object:
            """Transform the current dictionary ensuring all subdictionaries are of the
            expected class type and that their parent relationships are set as needed"""

            if isinstance(source, dict):
                if isinstance(source, dictation):
                    if source.parent is None:
                        source._parent = parent
                else:
                    source = dictation(source, parent=parent)

                for key, value in source.items():
                    source[key] = transform(value, parent=source)
            elif isinstance(source, (list, tuple, set)):
                for index, value in enumerate(source):
                    source[index] = transform(value, parent=parent)

            return source

        transform(source=self, parent=parent)

    def __str__(self) -> str:
        return "<dictation(%s)>" % (super().__str__())

    def __copy__(self):
        """Supports the creation of shallow copies of dictation class instances"""

        data = dict()

        for key, value in self.items():
            data[key] = copy.copy(value)

        annotations = dict()

        for key, annotation in self._annotations.items():
            annotations[key] = copy.copy(annotation)

        return dictation(data).annotate(**annotations)

    def __deepcopy__(self, memo):
        """Supports the creation of deep copies of dictation class instances"""

        data = dict()

        for key, value in self.items():
            data[key] = copy.deepcopy(value, memo)

        annotations = dict()

        for key, annotation in self._annotations.items():
            annotations[key] = copy.deepcopy(annotation, memo)

        return dictation(data).annotate(**annotations)

    def __setattr__(self, name: str, value: object):
        """Supports setting class attributes or annotations via attributes; annotation
        attributes cannot have names starting with underscores as these are reserved for
        class attributes and methods, nor can annotations use the same name as inherent
        class attributes or public methods; using such names will raise an exception."""

        if not isinstance(name, str):
            raise TypeError("The 'name' argument must have a string value!")

        if name.startswith("_"):
            super().__setattr__(name, value)
        elif name in self._special:
            if isinstance(attr := getattr(self.__class__, name, None), property):
                super().__setattr__(name, value)
            else:
                raise AnnotationError(
                    "Annotations cannot use any of the following reserved word names: %s!"
                    % (", ".join(self._special))
                )
        else:
            self.annotate(**{name: value}, recursive=False)

        return self

    def __getattr__(self, name: str, recursive: bool = False) -> object | None:
        """Supports obtaining class attributes or annotations; annotation attributes
        cannot have names starting with underscores as these are reserved for class
        attributes and methods. Annotations are searched hierarchically; if a matching
        annotation is present on the current node it will be returned, alternatively all
        parent nodes up to the root node will be searched for a match; if a match cannot
        be found then an AttributeError exception will be raised to note its absence."""

        if not isinstance(name, str):
            raise TypeError("The 'name' argument must have a string value!")

        if not isinstance(recursive, bool):
            raise TypeError("The 'recursive' argument must have a boolean value!")

        if name.startswith("_") or name in self._special:
            return super().__getattribute__(name)
        elif isinstance(annotation := self._annotations.get(name), self._annotation):
            if recursive is False or annotation.recursive is True:
                return annotation.value
        elif isinstance(parent := self._parent, dictation):
            return parent.__getattr__(name=name, recursive=True)
        else:
            raise AttributeError(f"The attribute '{name}' does not exist!")

    def __delattr__(self, name: str):
        """Supports deleting previously assigned annotations"""

        if name.startswith("_") or name in self._special:
            super().__delattr__(name)
        else:
            self.unannotate(name=name)

    def __setitem__(self, key: object, value: object):
        """Supports setting a dictionary item via the usual subscript d[k]=v notation"""

        if isinstance(value, dict) and not isinstance(value, dictation):
            value = dictation(value, parent=self)

        super().__setitem__(key, value)

    def __getitem__(self, key: object) -> object:
        """Supports getting a dictionary item via the usual subscript v=d[k] notation"""

        value = super().__getitem__(key)

        if isinstance(value, dict) and not isinstance(value, dictation):
            value = dictation(value, parent=self)

        return value

    def __getstate__(self) -> dict:
        """Supports pickling the `dictation` dictionary instance"""

        return self.__dict__.copy()

    def __setstate__(self, state: dict):
        """Supports un-pickling the `dictation` dictionary instance"""

        self.__dict__.update(state)

    @property
    def parent(self) -> dictation | None:
        """Return the instance's parent relationship, if one has been assigned"""

        return self._parent

    @parent.setter
    def parent(self, parent: dictation):
        """A dictation instance's parent relationship can only be assigned internally by
        the library to ensure integrity of the hierarchical references and the correct
        determination of any recursively available annotations for child nodes."""

        raise NotImplementedError("The 'parent' property cannot be set externally!")

    def get(self, key: object, default: object = None) -> object | None:
        """Overrides the `dict` class' `get` method to support specifying the default
        value positionally as well as via its keyword argument to improve documentation
        of the code at the call site, e.g. x.get("y", 0) vs x.get("y", default=0)."""

        return super().get(key, default)

    def set(self, key: object, value: object) -> dictation:
        """Provides a `set` method to compliment the built-in `dict` class' `get` method
        which takes the usual key and value as keyword arguments, and assigns the value
        to the current dictionary instance at the provided key. As this method returns
        `self`, calls to `set()` can be chained with calls to other class methods, such
        as the `annotate()` method."""

        self[key] = value

        return self

    @property
    def annotations(self) -> dict[str, object]:
        """Obtain the current annotations associated with the current `dictation` node
        as well as any annotations assigned to ancestors that are marked as recursive"""

        def gather(source: object, annotations: dict, recursive: bool = False):
            """Recursively gather any annotations assigned to the current node as well
            as any assigned to any ancestor nodes, returning them as a dictionary"""

            if isinstance(source, dictation):
                for key, annotation in source._annotations.items():
                    # If an annotation with the same name has already been encountered
                    # do not overwrite it; this ensures that annotations assigned higher
                    # in the hierarchy (starting at the root node), do not overwrite any
                    # annotations assigned at deeper levels, such as on a child node:
                    if not key in annotations:
                        if recursive is False or annotation.recursive is True:
                            annotations[key] = annotation.value

                if isinstance(parent := source.parent, dictation):
                    gather(source=parent, annotations=annotations, recursive=True)

            return annotations

        return gather(source=self, annotations=dict())

    @annotations.setter
    def annotations(self, annotations: dict):
        """The `annotations` property setter supports assigning one or more annotations
        to the current `dictation` instance by assigning a dictionary value of key-value
        pairs. The key-value pairs will be applied to the current `dictation` instance
        as additional annotations. If any of the annotation keys overlap with existing
        annotation keys, the new value will replace the old; annotation keys which do
        not match any existing annotation keys for the current instance will be applied
        as new annotations alongside the old. This behaviour is equivalent to the `dict`
        class' `update()` method, which overwrites existing keys and adds any new keys.

        It is important to note that annotations applied to the current `dictation`
        instance via the `annotations` property will not be available recursively to
        any of the current instance's nested children. Furthermore, if a pre-existing
        recursive annotation was stored on the current instance under a key that matches
        a key provided in the annotations assigned via the property, not only will the
        new value replace the old, but it will no longer be available recursively.

        In order to control which annotations are applied recursively, one may use the
        `annotate()` method instead which provides this additional level of control."""

        if not isinstance(annotations, dict):
            raise TypeError("The annotations property must be assigned as a dictionary")
        else:
            for name, value in annotations.items():
                if not isinstance(name, str):
                    raise AnnotationError("Annotations must have string names!")
                elif name.startswith("_"):
                    raise AnnotationError(
                        "Annotations cannot have names starting with underscores!"
                    )
                elif name in self._special:
                    raise AnnotationError(
                        "Annotations cannot use any of the following reserved word names: %s!"
                        % (", ".join(self._special))
                    )

        self.annotate(**annotations)

    def annotate(self, recursive: bool = False, **annotations) -> dictation:
        """Supports assigning one or more annotations to the current dictation instance,
        specified as key-value pairs. The 'recursive' keyword is reserved for specifying
        if the annotations will be marked as being recursively available for the current
        node and any children; otherwise they are only available to the current node."""

        if not isinstance(recursive, bool):
            raise TypeError("The 'recursive' argument must have a boolean value!")

        for name, value in annotations.items():
            if not isinstance(name, str):
                raise AnnotationError("Annotations must have string names!")
            elif name.startswith("_"):
                raise AnnotationError(
                    "Annotations cannot have names starting with underscores!"
                )
            elif name in self._special:
                raise AnnotationError(
                    "Annotations cannot use any of the following reserved word names: %s!"
                    % (", ".join(self._special))
                )

            self._annotations[name] = self._annotation(
                value=value,
                recursive=recursive,
            )

        return self

    def annotation(
        self,
        name: str,
        default: object = None,
        recursive: bool = True,
    ) -> object | None:
        """Supports recursively obtaining and returning a named annotation value. If the
        named annotation cannot be found, and if a default value has been specified, it
        will be returned, otherwise the method will return the `None` value instead. If
        the named annotation should only be retrieved from the current node and not via
        a recursive lookup, the 'recursive' argument may be set to `False`."""

        if not isinstance(name, str):
            raise TypeError("The 'name' argument must have a string value!")

        if not isinstance(recursive, bool):
            raise TypeError("The 'recursive' argument must have a boolean value!")

        if isinstance(annotation := self._annotations.get(name), self._annotation):
            return annotation.value
        elif recursive is True and isinstance(parent := self._parent, dictation):
            return parent.annotation(name=name, recursive=recursive, default=default)
        elif not default is None:
            return default

    def unannotate(self, name: str) -> dictation:
        """Supports removing an annotation assigned directly to the current `dictation`
        node. The `dictation` class does not support removing annotations recursively,
        as annotations are not stored recursively, rather they are stored directly on
        the node to which they are assigned, but each annotation can be marked as being
        available recursively – or not – to any nested children. As such, to remove any
        recursively available annotation that is no longer needed, it must either be
        removed from the node that it was directly assigned to, or it can be reassigned
        to the same node without recursive availability via the `annotate()` method."""

        if not isinstance(name, str):
            raise TypeError("The 'name' argument must have a string value!")

        if name in self._annotations:
            del self._annotations[name]

        return self

    def data(self, metadata: bool = False, annotations: bool = False):
        """Supports generating a dictionary representation of a `dictation` instance's
        data, optionally including associated metadata such as any parent references,
        any assigned annotation values, and typing information for each value. This is
        primarily useful for debugging purposes."""

        if not isinstance(metadata, bool):
            raise TypeError("The 'metadata' argument must have a boolean value!")

        if not isinstance(annotations, bool):
            raise TypeError("The 'annotations' argument must have a boolean value!")

        def dump(source: object, metadata: bool = False, annotations: bool = False):
            data = {}

            if metadata is True:
                data["@type"] = str(type(source))

            if isinstance(source, dict):
                if isinstance(source, dictation):
                    if metadata is True:
                        data["@parent"] = str(source.parent) if source.parent else None

                        if annotations is True:
                            data["@annotations"] = {
                                key: value for key, value in source.annotations.items()
                            }

                if metadata is True:
                    data["@value"] = {}

                    for key, value in source.items():
                        data["@value"][key] = dump(
                            source=value,
                            metadata=metadata,
                            annotations=annotations,
                        )
                else:
                    for key, value in source.items():
                        data[key] = dump(
                            source=value,
                            metadata=metadata,
                            annotations=annotations,
                        )
            elif isinstance(source, (list, tuple)):
                if metadata is True:
                    data["@value"] = []

                    for index, value in enumerate(source):
                        data["@value"].append(
                            dump(
                                source=value,
                                metadata=metadata,
                                annotations=annotations,
                            )
                        )
                else:
                    data = []

                    for index, value in enumerate(source):
                        data.append(
                            dump(
                                source=value,
                                metadata=metadata,
                                annotations=annotations,
                            )
                        )
            else:
                if metadata is True:
                    data["@value"] = source
                else:
                    data = source

            return data

        return dump(source=self, metadata=metadata, annotations=annotations)

    def print(self, indent: int = 0):
        """Supports generating a print-out of the `dictation` instance's data as well as
        any annotations which can be useful for debugging or visualisation purposes."""

        if not isinstance(indent, int):
            raise TypeError("The 'indent' argument must have an integer value!")

        def printer(source: object, indent: int = 0):
            print(("  " * indent) + " => %s" % (type(source)))

            if isinstance(source, dictation):
                print(("  " * indent) + " => parent      -> %s" % (source.parent))
                print(("  " * indent) + " => annotations -> %s" % (source.annotations))

            if isinstance(source, dict):
                for key, value in source.items():
                    print(("  " * indent) + " => %s" % (key))

                    if isinstance(value, (dict, list, tuple)):
                        printer(value, indent=(indent + 1))
                    else:
                        print(("  " * (indent + 1)) + " => %s" % (value))
            elif isinstance(source, (list, tuple)):
                print((" " * indent) + " => parent      -> %s" % (source.parent))

                for key, index in enumerate(source):
                    print((" " * indent) + " => %s" % (index))

                    if isinstance(value, (dict, list, tuple)):
                        printer(value, indent=(indent + 1))
                    else:
                        print(("  " * (indent + 1)) + " => %s" % (value))
            else:
                print(("  " * indent) + " => %s (%s)" % (source, type(source)))

        printer(source=self, indent=indent)
