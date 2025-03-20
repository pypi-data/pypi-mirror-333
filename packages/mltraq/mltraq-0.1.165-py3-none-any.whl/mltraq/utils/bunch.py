from __future__ import annotations

import itertools
import os
import random
from collections import OrderedDict
from typing import Iterator, Optional

from mltraq.opts import options
from mltraq.utils.exceptions import ExceptionWithMessage


class ReadOnlyError(ExceptionWithMessage):
    pass


class Bunch(OrderedDict):
    """
    Ordered dictionary whose elements can be accessed as object attributes.
    """

    def __init__(self, *args, **kwargs):
        """
        Same constructor of dict type. Additionally,
        if input is None, it returns an empty dict.
        """
        if args == (None,) and not kwargs:
            super().__init__()
        else:
            super().__init__(*args, **kwargs)

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError as e:
            raise AttributeError(key) from e

    def __setattr__(self, key, value):
        self[key] = value

    def __delattr__(self, key):
        try:
            del self[key]
        except KeyError as e:
            raise AttributeError(key) from e

    def __str__(self):
        return Bunch.bunch_to_dict_deep(self).__str__()

    def __repr__(self):
        return self.__str__()

    def _repr_html_(self):
        return self.__str__()

    @classmethod
    def dict_to_bunch_deep(cls, d: dict) -> Bunch:
        """
        Deep-conversion of a dict to a Bunch.
        """

        if isinstance(d, dict):
            return Bunch({k: Bunch.dict_to_bunch_deep(v) for k, v in d.items()})
        else:
            return d

    @classmethod
    def bunch_to_dict_deep(cls, d: Bunch) -> dict:
        """
        Deep-conversion of a Bunch to a dict.
        We return dict objects without looking for Bunch values inside them.
        """

        if isinstance(d, Bunch):
            return {k: Bunch.bunch_to_dict_deep(v) for k, v in d.items()}
        else:
            return d

    def cartesian_product(self) -> Iterator[dict]:
        """
        Cartesian product of arguments:

        Given a list of key:value pairs, values are treated as lists
        and the Cartesian product of all possible combinations of
        values form each item is returned.
        """
        for instance in itertools.product(*self.values()):
            yield dict(zip(self.keys(), instance))


class BunchEvent(Bunch):
    """
    Bunch with function triggers on events "on_setattr", "on_getattr".
    Useful to implement assertions, debugging procedures and alerts.
    """

    def __init__(self, *args, **kwargs):
        """
        Same constructor of Bunch, with initializations.
        """

        self.clear_triggers()
        super().__init__(*args, **kwargs)

    def clear_triggers(self):
        """
        Initialize triggers, removing existing ones, if any.
        """

        self._on_setattr_triggers = {}
        self._on_getattr_triggers = {}

    def on_setattr(self, key, func):
        """
        Add trigger to call `func` with parameter `key`, `value` on setattr events.
        """

        if key in self._on_setattr_triggers:
            triggers = self.on_setattr_triggers[key]
        else:
            triggers = []
            self._on_setattr_triggers[key] = triggers

        triggers.append(func)

    def on_getattr(self, key, func):
        """
        Add trigger to call `func` with parameter `key`, `value` on getattr events.
        """

        if key in self._on_getattr_triggers:
            triggers = self.on_getattr_triggers[key]
        else:
            triggers = []
            self._on_getattr_triggers[key] = triggers

        triggers.append(func)

    def __setitem__(self, key, value):
        if not key.startswith("_on_") and key in self._on_setattr_triggers:
            for func in self._on_setattr_triggers[key]:
                func(key, value)
        super().__setitem__(key, value)

    def __setattr__(self, key, value):
        self[key] = value

    def __getitem__(self, key):
        value = super().__getitem__(key)

        if not key.startswith("_on_") and key in self._on_getattr_triggers:
            for func in self._on_getattr_triggers[key]:
                func(key, value)

        return value

    def __getattr__(self, key):
        return self[key]


class BunchStore:
    """
    Basic key-value store on filesystem for a single Bunch object.
    """

    def __init__(self, pathname: Optional[str] = None, read_only: bool = False):
        """
        Initialize and load the key-value store. The bunch is serialized/deserialized to `pathname` (or its
        default value "bunchstore.pathname"), appending `suffix` if provided.
        In case of read-only use cases, specify `read_only=True` to avoid unnecessary writes.
        """

        # Importing here to avoid circular dependency.
        from mltraq.storage.serialization import deserialize, serialize  # noqa: F401

        # Storing eveyrthing as part of meta_ attribute, s.t. we can use
        # attr and item setters/getters with less overhead.
        self.meta_ = Bunch()
        self.meta_.deserialize = deserialize
        self.meta_.serialize = serialize
        self.meta_.pathname = options().get("bunchstore.pathname", prefer=pathname)
        self.meta_.read_only = read_only
        self.meta_.data = Bunch()

        # Try to read and write the inner Bunch, ensuring that the pathname is readable/writeable.
        # (if read-only, skip write test.)
        self.read()
        if not self.meta_.read_only:
            self.write()

    def read(self):
        """
        Load inner Bunch from file (if available).
        """
        if os.path.exists(self.meta_.pathname):
            self.meta_.data = self.meta_.deserialize(open(self.meta_.pathname, "rb").read())

    def __setitem__(self, key, value):
        self.meta_.data[key] = value
        self.write()

    def __getitem__(self, key):
        self.read()
        return self.meta_.data[key]

    def __getattr__(self, key):
        return self[key]

    def __setattr__(self, key, value):
        if key != "meta_":
            self[key] = value
        else:
            super().__setattr__(key, value)

    def __len__(self):
        return len(self.meta_.data)

    def __delitem__(self, key):
        del self.meta_.data[key]

    def __iter__(self):
        return iter(self.meta_.data)

    def data(self):
        return self.meta_.data

    def write(self):
        """
        Overwrite BunchStore file on filesystem, using a temporary file
        to avoid concurrency issues.
        """

        if self.meta_.read_only:
            # If the BunchStore is instantiated as read-only, raise an
            # exception if there are attempts to write it to filesystem.
            raise ReadOnlyError("Attempting to write but read-only")

        # We add some randomness to the temporary path to avoid race conditions
        # in case of threaded applications. In case of a race condition, only
        # one version will be persisted.

        randomness = random.randrange(10**5)

        with open(f"{self.meta_.pathname}.tmp.{randomness}", "wb") as f:
            f.write(self.meta_.serialize(self.meta_.data))
        os.replace(f"{self.meta_.pathname}.tmp.{randomness}", self.meta_.pathname)
