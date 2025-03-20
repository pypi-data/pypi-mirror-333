"""
Provides a set of singleton objects that can declare their purpose a little bit better than None can
"""

# import enum
import types

__all__ = [
    "default",
    "is_default",
    "handle_default",
    "uninitialized",
    "is_uninitialized",
    "handle_uninitialized",
    "is_interface_like",
    "is_dict_like",
    "cached_eval"
]

class SingletonType:
    """
    A base type for singletons
    """
    __slots__ = []

class DefaultType(SingletonType):
    """
    A type for declaring an argument should use its default value (for when `None` has meaning)
    """
    __is_default__ = True
default=DefaultType()

class UninitializedType(SingletonType):
    """
    A type for declaring an argument should use its default value (for when `None` has meaning)
    """
    __is_uninitialized__ = True
uninitialized = UninitializedType()

def is_interface_like(obj, interface_types, implementation_attrs):
    return (
        isinstance(obj, interface_types)
        or all(hasattr(obj, a) for a in implementation_attrs)
    )

def is_dict_like(obj,
                 interface_types=(dict, types.MappingProxyType),
                 implementation_props=('items',)
                 ):
    return is_interface_like(obj, interface_types, implementation_props)

def is_default(obj, allow_None=True):
    if allow_None and obj is None:
        return True

    return (
            obj is default
            or isinstance(obj, DefaultType)
            or (hasattr(obj, '__is_default__') and obj.__is_default__)
    )

def handle_default(opt, default_value, allow_None=True):
    if is_default(opt, allow_None=allow_None):
        return default_value
    else:
        return opt

def is_uninitialized(obj, allow_None=True):
    if allow_None and obj is None:
        return True

    return (
            obj is uninitialized
            or isinstance(obj, UninitializedType)
            or (hasattr(obj, '__is_uninitialized__') and obj.__is_uninitialized__)
    )

def handle_uninitialized(opt, initializer, allow_None=True, args=(), kwargs=None):
    if is_uninitialized(opt, allow_None=allow_None):
        return initializer(*args, **({} if kwargs is None else kwargs))
    else:
        return opt


def cached_eval(cache, key, generator, *,
                condition=None,
                args=(),
                kwargs=None):
    condition = (condition is None or condition(key))
    if not condition:
        if kwargs is None: kwargs = {}
        return generator(*args, **kwargs)

    if key in cache:
        return cache[key]

    if kwargs is None: kwargs = {}
    val = generator(*args, **kwargs)
    cache[key] = val

    return val