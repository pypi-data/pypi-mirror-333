"""
Caching
"""

#===============================================================================
# Imports
#===============================================================================

from __future__ import annotations

import sys
from time import monotonic


#===============================================================================
# Exports
#===============================================================================

__all__ = ['cached_property', 'timed_cached_property', 'TimedCachedProperty',]


#===============================================================================
# Cached Property (prior to Python 3.8)
#===============================================================================

if sys.version_info >= (3, 8):
    from functools import cached_property
else:
    _NOT_FOUND = object()

    class cached_property: # pylint: disable=invalid-name,too-few-public-methods
        """Adapted from Python 3.8 & 3.12, for use in Python 3.7"""

        def __init__(self, func):

            self.func = func
            self.attrname = None
            self.__doc__ = func.__doc__


        def __set_name__(self, owner, name):

            if self.attrname is None:
                self.attrname = name
            elif name != self.attrname:
                raise TypeError(
                    "Cannot assign the same cached_property to two different names "
                    f"({self.attrname!r} and {name!r})."
                )


        def __get__(self, instance, owner=None):

            if instance is None:
                return self
            if self.attrname is None:
                raise TypeError(
                    "Cannot use cached_property instance without calling __set_name__ on it.")

            try:
                cache = instance.__dict__
            except AttributeError:  # not all objects have __dict__ (e.g. class defines slots)
                msg = (
                    f"No '__dict__' attribute on {type(instance).__name__!r} "
                    f"instance to cache {self.attrname!r} property."
                )
                raise TypeError(msg) from None

            val = cache.get(self.attrname, _NOT_FOUND)
            if val is _NOT_FOUND:
                val = self.func(instance)
                try:
                    cache[self.attrname] = val
                except TypeError:
                    msg = (
                        f"The '__dict__' attribute on {type(instance).__name__!r} instance "
                        f"does not support item assignment for caching {self.attrname!r} property."
                    )
                    raise TypeError(msg) from None

            return val


#===============================================================================
# Timed Cached Property
#===============================================================================

_NO_ENTRY = None, None


class TimedCachedProperty(property):
    """
    A cached property which will be "recomputed" when requested if the given
    period of time has elapsed since it was last cached.
    """

    def __init__(self, fget, life_sec: float, fset=None):

        super().__init__(fget, fset)
        self.attrname = None
        self._name = None
        self._life_sec = life_sec


    def __set_name__(self, owner, name):
        if self.attrname is None:
            self.attrname = name
            self._name = f"_{name}_cache"
        elif name != self.attrname:
            raise TypeError(
                f"Cannot assign the same {self.__class__.__name__} to two "
                f"different names ({self.attrname!r} and {name!r})."
            )


    def _cache(self, instance):

        if self.attrname is None:
            raise TypeError(
                "Cannot use timed_cached_property instance without calling "
                "__set_name__ on it.")

        try:
            cache = instance.__dict__
        except AttributeError:  # not all objects have __dict__ (e.g. class defines slots)
            msg = (
                f"No '__dict__' attribute on {type(instance).__name__!r} "
                f"instance to store {self.attrname!r} property."
            )
            raise TypeError(msg) from None

        return cache


    def __delete__(self, instance):

        cache = self._cache(instance)
        cache.pop(self._name, None)


    def __get__(self, instance, owner=None):

        if instance is None:
            return self

        cache = self._cache(instance)

        now = monotonic()
        val, expiry = cache.get(self._name, _NO_ENTRY)
        if expiry is None or now > expiry:
            val = self.fget(instance)
            try:
                cache[self._name] = (val, now + self._life_sec)
            except TypeError:
                msg = (
                    f"The '__dict__' attribute on {type(instance).__name__!r} "
                    "instance does not support item assignment for caching "
                    f"{self.attrname!r} property."
                )
                raise TypeError(msg) from None

        return val


    def __set__(self, instance, value):

        fset = self.fset

        if fset is None:
            raise AttributeError(f"property {self.attrname!r} of "
                                 f"{instance.__class__.__name__} object "
                                 "has no setter")

        cache = self._cache(instance)
        value = fset(instance, value)
        if value is not None:
            now = monotonic()
            cache[self._name] = (value, now + self._life_sec)
        else:
            cache.pop(self._name, None)


    def setter(self, func):
        return self.__class__(self.fget, self._life_sec, func)


def timed_cached_property(secs: float):
    """
    A cached property which will be "recomputed" when requested if the given
    period of time has elapsed since it was last cached.
    """

    def decorator(func):
        return TimedCachedProperty(func, secs)

    return decorator
