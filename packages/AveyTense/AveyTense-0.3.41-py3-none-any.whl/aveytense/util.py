"""
**AveyTense Utility Tools** \n
\\@since 0.3.34 \\
© 2025-Present Aveyzan // License: MIT
```ts
module aveytense.util
```
Includes utility tools, including `Final`, `Abstract` and `Frozen` classes, \\
extracted from `aveytense.types_collection`. It formally doesn't use the `tense` \\
module.
"""


# standard imports
from __future__ import annotations

import abc as _abc
import collections.abc as _collections_abc
import types as _builtins_types
import typing as _typing
import typing_extensions as _typing_ext # not standard, ensure it is installed
import sys as _sys

from ._exceptions import *
from ._exceptions import ErrorHandler as _E
from . import _init_types as _types
from . import _abc as _tense_abc

del ErrorHandler

_ch = eval # checker

_P = _types.ParamSpec("_P")
_T = _types.TypeVar("_T")
_T_cov = _types.TypeVar("_T_cov", covariant = True)
_T_func = _types.TypeVar("_T_func", bound = _types.Callable[..., _types.Any])
_RichComparable = _types.Union[_tense_abc.LeastComparable, _tense_abc.GreaterComparable]

_OptionSelection = _types.Literal["frozen", "final", "abstract", "no_reassign"] # 0.3.27rc2

def _reckon(i: _tense_abc.Iterable[_T], /):
    
    _i = 0
    
    for _ in i:
        _i += 1
        
    return _i

def _ih(id: int, /): # internal helper
    
    _m = "eval"
    _c = _i = ""
    
    if id == 10:
        
        _c, _i = "_E(113, t.__name__)", "<final-class inspect>"
        
    elif id == 11:
        
        _c, _i = "_E(116, type(self).__name__)", "<final-class inspect>"
        
    elif id == 12:
        
        _c, _i = "_E(116, t.__name__)", "<final-class inspect>"
        
    elif id == 20:
        
        _c, _i = "_E(104, type(self).__name__)", "<abstract-class inspect>"
    
    elif id == 21:
        
        _c, _i = "_E(115, type(self).__name__)", "<abstract-class inspect>"
        
    elif id == 22:
        
        _c, _i = "_E(115, t.__name__)", "<abstract-class inspect>"
        
    return compile(_c, _i, _m)

class _InternalHelper:
    """
    \\@since 0.3.27rc2
    
    Class responsible to shorten code for several classes such as `Final` and `Abstract`
    """
    
    def __new__(cls, t: type[_T], o: _OptionSelection, /):
        
        _reassignment_operators = {
            "__iadd__": "+=",
            "__isub__": "-=",
            "__imul__": "*=",
            "__itruediv__": "/=",
            "__ifloordiv__": "//=",
            "__imod__": "",
            "__imatmul__": "@=",
            "__iand__": "&=",
            "__ior__": "|=",
            "__ixor__": "^=",
            "__ilshift__": "<<=",
            "__irshift__": ">>=",
            "__ipow__": "**="
        }
        
        _cannot_redo = {"tmp": "tmp2"}
        
        # assuming empty string-string dictionary
        
        if False: # < 0.3.37
            if _cannot_redo["tmp"]:
                del _cannot_redo["tmp"]
                
        else:
            _cannot_redo.clear()
        
        def _no_sa(self: _T, name: str, value): # no setattr
            
            if name in type(self).__dict__:
                _E(118, name)
                
            type(self).__dict__[name] = value
            
        def _no_da(self: _T, name: str): # no delattr
            
            if name in type(self).__dict__:
                _E(117, name)
                
        def _no_inst(self: _T, *args, **kwds): # no initialize
            _ch(_ih(20))
            
        def _no_cinst(o: object): # no check instance
            nonlocal t
            _ch(_ih(22))
            
        def _no_sub(*args, **kwds): # no subclass
            nonlocal t
            _ch(_ih(10))
            
        def _no_csub(cls: type): # no check subclass
            nonlocal t
            _ch(_ih(12))
            
        def _no_re(op: str): # no reassignment; must return callback so assigned attributes can be methods
            
            def _no_re_internal(self: _types.Self, other: _T):
                
                _op = "with operator {}".format(op)
                _E(102, _op)
                
            return _no_re_internal
        
        def _empty_mro(self: _T): # empty method resolution order; peculiar for final classes
            return None
        
        if o in ("frozen", "no_reassign"):
            
            t.__slots__ = ("__weakref__",)
            t.__setattr__ = _no_sa
            t.__delattr__ = _no_da
            
            _cannot_redo["__setattr__"] = _no_sa.__name__
            _cannot_redo["__delattr__"] = _no_da.__name__
            
            if o == "no_reassign":
                
                for key in _reassignment_operators:
                    
                    exec("t.{} = _no_re(\"{}\")".format(key, _reassignment_operators[key])) # f-strings since python 3.6
                    exec("_cannot_redo[\"{}\"] = _no_re(\"{}\").__name__".format(key, _reassignment_operators[key]))
                    
        elif o == "final":
            
            t.__slots__ = ("__weakref__",)
            t.__init_subclass__ = _no_sub
            t.__subclasscheck__ = _no_csub
            t.__mro_entries__ = _empty_mro
            
            _cannot_redo["__init_subclass__"] = _no_sub.__name__
            _cannot_redo["__subclasscheck__"] = _no_csub.__name__
            _cannot_redo["__mro_entries__"] = _empty_mro.__name__
            
        else:
            t.__init__ = _no_inst
            t.__instancecheck__ = _no_cinst
            
            _cannot_redo["__init__"] = _no_inst.__name__
            _cannot_redo["__instancecheck__"] = _no_cinst.__name__
            
        for key in _cannot_redo:
            if _cannot_redo[key] != "_no_re_internal" and eval("t.{}.__code__".format(key)) != eval("{}.__code__".format(_cannot_redo[key])):
                _E(120, key)    
        
        return t

class _FinalVar(_types.NamedTuple, _types.Generic[_T]): # 0.3.35
    x: _T
    """\\@since 0.3.35. This attribute holds the value"""
    
    def __pos__(self):
        
        return self.x
    
    def __str__(self):
        
        return "FinalVar({})".format(str(self.x) if type(self.x) is not str else self.x)
    
    def __repr__(self): # 0.3.40
        
        return "<{}.{} object: {}>".format(self.__module__, type(self).__name__, self.__str__())
    
# if not that, then it will behave like normal NamedTuple
_FinalVar = _InternalHelper(_FinalVar, "no_reassign")

types = _types
"""\\@since 0.3.37"""


class Abstract:
    """
    \\@since 0.3.26b3 \\
    https://aveyzan.glitch.me/tense#aveytense.util.Abstract
    
    Creates an abstract class. This type of class forbids class initialization. To prevent this class \\
    being initialized, this class is a protocol class.
    """
    
    def __init__(self):
        _ch(_ih(20))
        
    def __init_subclass__(cls):
        cls = _InternalHelper(cls, "abstract")
    
    def __instancecheck__(self, instance: object):
        "\\@since 0.3.27b1. Error is thrown, because class may not be instantiated"
        _ch(_ih(21))
    
    def __subclasscheck__(self, cls: type):
        "\\@since 0.3.27b1. Check whether a class is a subclass of this class"
        return issubclass(cls, type(self))
    
    if False: # 0.3.28 (use abstractmethod instead)
        @staticmethod
        def method(f: _T_func):
            """\\@since 0.3.27rc2"""
            from abc import abstractmethod as _a
            return _a(f)

def abstract(t: type[_T], /): # <- 0.3.41 slash
    """
    \\@since 0.3.27a5 (formally)
    
    Decorator for abstract classes. To 0.3.27rc2 same `abc.abstractmethod()`
    """
    t = _InternalHelper(t, "abstract")
    return t

def abstractmethod(f: _T_func, /): # <- 0.3.41 slash
    """\\@since 0.3.27rc2"""
    
    # to accord python implementation
    if False:
        return Abstract.method(f)
    
    else:
        return _abc.abstractmethod(f)
    
if hasattr(_abc, "abstractproperty"):
    from abc import abstractproperty as abstractproperty # deprecated since 3.3
    
else:
    class abstractproperty(property):
        """
        \\@since 0.3.26rc1

        A decorator class for abstract properties.

        Equivalent invoking decorators `aveytense.types_collection.abstract` and in-built `property`.
        """
        __isabstractmethod__ = True

if hasattr(_abc, "abstractstaticmethod"):
    from abc import abstractstaticmethod as abstractstaticmethod # deprecated since 3.3
    
else:
    class abstractstaticmethod(staticmethod):
        """
        \\@since 0.3.26rc1

        A decorator class for abstract static methods.

        Equivalent invoking decorators `aveytense.types_collection.abstract` and in-built `staticmethod`.
        """
        __isabstractmethod__ = True
        
        def __init__(self, f: _types.Callable[_P, _T_cov]):
            f.__isabstractmethod__ = True
            super().__init__(f)

if hasattr(_abc, "abstractclassmethod"):
    from abc import abstractclassmethod as abstractclassmethod # deprecated since 3.3
    
else:
    class abstractclassmethod(classmethod):
        """
        \\@since 0.3.26rc1

        A decorator class for abstract class methods.

        Equivalent invoking decorators `aveytense.types_collection.abstract` and in-built `classmethod`.
        """
        __isabstractmethod__ = True
        
        def __init__(self, f: _types.Callable[_types.Concatenate[type[_T], _P], _T_cov]):
            f.__isabstractmethod__ = True
            super().__init__(f)

# reference to enum.Enum; during experiments and not in use until it is done
# tests done for 0.3.27rc1
class Frozen:
    """
    \\@since 0.3.27b1 (experiments finished 0.3.27rc1, updated: 0.3.27rc2) \\
    https://aveyzan.glitch.me/tense#aveytense.util.Frozen
    
    Creates a frozen class. This type of class doesn't allow change of provided fields \\
    once class has been declared and then initialized.
    """
    
    def __init_subclass__(cls):
        cls = type(cls.__name__, tuple([]), {k: _FinalVar(cls.__dict__[k]) for k in cls.__dict__ if k[:1] != "_"})

def frozen(t: type[_T], /): # <- 0.3.41 slash
    """
    \\@since 0.3.27rc1

    Alias to `dataclass(frozen = True)` decorator (for 0.3.27rc1). \\
    Since 0.3.27rc2 using different way.
    """
    t = _InternalHelper(t, "frozen")
    return t


class Final:
    """
    \\@since 0.3.26b3 (experimental; to 0.3.27b3 `FinalClass`, experiments ended 0.3.27rc1) \\
    https://aveyzan.glitch.me/tense#aveytense.util.Final

    Creates a final class. This type of class cannot be further inherited once a class extends this \\
    class. `class FinalClass(Final)` is OK, but `class FinalClass2(FinalClass)` not. \\
    However, class can be still initialized, but it is not recommended. It's purpose is only to create \\
    final classes (to 0.3.29 - error occuring due to class initialization)
    
    This class is a reference to local class `_Final` from `typing` module, with lack of necessity \\
    providing the `_root` keyword to inheritance section.
    """
    __slots__ = ("__weakref__",)

    def __init_subclass__(cls):
        cls = _InternalHelper(cls, "final")
       
    def __instancecheck__(self, instance: object):
        "\\@since 0.3.27rc1. Check whether an object is instance to this class"
        return isinstance(instance, type(self))
    
    def __subclasscheck__(self, cls: type):
        "\\@since 0.3.27rc1. Error is thrown, because this class may not be subclassed"
        _ch(_ih(11))
       
    def __mro_entries__(self):
        return None
    
    @property
    def __mro__(self):
        return None
    
    if False: # 0.3.28 (use finalmethod instead)
        @staticmethod
        def method(f: _T_func):
            """\\@since 0.3.27rc2"""
            
            if _sys.version_info >= (3, 11):
                from typing import final as _f
                
            else:
                from typing_extensions import final as _f
                
            return _f(f)
    
def final(t: type[_T], /): # <- 0.3.41 slash
    """
    \\@since 0.3.26b3
    """
    t = _InternalHelper(t, "final")
    return t

def finalmethod(f: _T_func, /): # <- 0.3.41 slash
    """
    \\@since 0.3.27rc2
    """
    if False:
        return Final.method(f)
    
    else:
        return _types.final(f)
        
class finalproperty:
    """
    \\@since 0.3.37
    
    A decorator which creates a final (constant) property. \\
    This property cannot receive new values nor be deleted, what makes \\
    this property read-only.
    
    It does not work with `classmethod` nor `staticmethod`. If either \\
    of these has been used along with this decorator, internal code \\
    neutralizes effects of both decorators, and error will be always \\
    thrown when setting or deleting final property via instance (not via \\
    reference).
    """
        
    def __new__(cls, f: _types.Callable[[_types.Any], _T], /):
        
        _f = property(f)
        
        if _sys.version_info >= (3, 13):
            n = _f.__name__
            
        else:
            n = _f.fget.__name__
        
        # No 'self' parameter attempt. Apparently this class doesn't
        # work with 'staticmethod'.
        if isinstance(f, staticmethod):
            
            def _no_de():
                _E(122, n)
                    
            def _no_se(x):
                _E(122, n)
                    
        elif isinstance(f, (classmethod, _types.FunctionType)):
        
            def _no_de(self):
                _E(122, n)
                    
            def _no_se(self, x):
                _E(122, n)
                
        else:
            
            error = TypeError("expected a callable in-class")
            raise error
        
        return _f.deleter(_no_de).setter(_no_se).getter(f)

class FinalVar:
    """
    \\@since 0.3.26rc1 (experiments ended on 0.3.35)
    
    To 0.3.35 this class was in `aveytense.types_collection`. This class formalizes a final variable. On 0.3.35 all ways to get the value \\
    (expect with unary `+`) has been replaced with `x` attribute access. Hence you use the following: `instance.x`.
    """
    
    def __new__(cls, value: _T, /):
        
        return _FinalVar(value)
    
    def __init_subclass__(cls):
        
        def _tmp(cls: type[_types.Self], value: _T, /):
        
            return _FinalVar(value)
        
        cls.__new__ = _tmp
        
FinalVarType = _FinalVar # 0.3.38; see ~.Tense.isFinalVar()
        
@final
class ClassLike(_types.Generic[_P, _T]):
    """
    \\@since 0.3.27a3
    
    To 0.3.35 this class was in `aveytense.types_collection`. \\
    A class decorator for functions, transforming them to declarations \\
    similar to classes. Example::
    
        @ClassLike
        def test():
            return 42

        a = test() # returns 42

    """
    def __init__(self, f: _types.Callable[_P, _T]):
        self.f = f
        
    def __call__(self, *args: _P.args, **kwds: _P.kwargs):
        return self.f(*args, **kwds)
    
classlike = ClassLike # since 0.3.27a3
        
AbstractMeta = _abc.ABCMeta
"""
\\@since 0.3.27b1. Use it as::
```
class AbstractClass(metaclass = AbstractMeta): ...
```
"""

class AbstractFinal:
    """
    \\@since 0.3.27rc1 https://aveyzan.glitch.me/tense#aveytense.util.AbstractFinal
    
    Creates an abstract-final class. Typically blend of `Abstract` and `Final` classes \\
    within submodule `aveytense.util`. Classes extending this class are \\
    only restricted to modify fields (as in `TenseOptions`) or invoke static methods, \\
    because they cannot be neither initialized nor inherited.
    """
    __slots__ = ("__weakref__",)
    
    def __init__(self):
        _ch(_ih(20))
    
    def __init_subclass__(cls):
        cls = _InternalHelper(cls, "abstract")
        cls = _InternalHelper(cls, "final")
       
    def __mro_entries__(self):
        return None
    
    @property
    def __mro__(self):
        return None
    
    def __instancecheck__(self, instance: object):
        "\\@since 0.3.27rc1. Error is thrown, because class may not be instantiated"
        _ch(_ih(21))
    
    def __subclasscheck__(self, cls: type):
        "\\@since 0.3.27rc1. Error is thrown, because class may not be subclassed"
        _ch(_ih(11))

class FinalFrozen:
    """
    \\@since 0.3.27rc1
    
    Creates a final-frozen class. Typically blend of `Final` and `Frozen` classes \\
    within submodule `aveytense.util`. Classes extending this class cannot \\
    be further extended nor have fields modified by their objects.
    """
    __slots__ = ("__weakref__",)
    
    def __init_subclass__(cls):
        cls = _InternalHelper(cls, "final")
        cls = _InternalHelper(cls, "frozen")
       
    def __instancecheck__(self, instance: object):
        "\\@since 0.3.27rc1. Check whether an object is instance to this class"
        return isinstance(instance, type(self))
    
    def __subclasscheck__(self, cls: type):
        "\\@since 0.3.27rc1. Error is thrown, because this class may not be subclassed"
        _ch(_ih(11))
       
    def __mro_entries__(self):
        return None
    
    @property
    def __mro__(self):
        return None  

class AbstractFrozen:
    """
    \\@since 0.3.27rc1
    
    Creates an abstract-frozen class. Typically blend of `Abstract` and `Frozen` classes \\
    within submodule `aveytense.util`. Classes extending this class cannot \\
    be initialized, nor have their fields modified. During experiments
    
    Possible way to end the experiments would be:
    - extending `enum.Enum` and overriding only some of its declarations, such as `__new__` method
    - extending `type` and raising error in `__setattr__` and `__delattr__`
    - creating private dictionary which will store class names as keys and fields as values, further \\
        used by both pre-mentioned methods
    """
    __slots__ = ()
    
    def __init_subclass__(cls):
        
        def _no_init(self: _types.Self):
            _ch(_ih(2))
        
        cls = abstract(frozen(cls))
        
        if cls.__init__.__code__ is not _no_init.__code__:
           error = LookupError("cannot remake __init__ method code on class " + cls.__name__)
           raise error
        
    def __instancecheck__(self, instance: object):
        "\\@since 0.3.27rc1. Error is thrown, because class may not be instantiated"
        _E(115, type(self).__name__)
        
    def __subclasscheck__(self, cls: type):
        "\\@since 0.3.27rc1. Check whether a class is a subclass of this class"
        return issubclass(cls, type(self))


class SortedList(_types.Generic[_T]):
    """
    \\@since 0.3.35
    
    Creates a sorted list. Note this class doesn't inherit from `list` builtin itself.
    """
    
    def __init__(self, i: _collections_abc.Iterable[_T], /, key: _types.Optional[_types.Callable[[_T], _RichComparable]] = None, reverse = False): # 0.3.35
        
        if not isinstance(i, _collections_abc.Iterable):
            
            error = ValueError("expected an iterable")
            raise error
        
        self.__l = self.__sorted = [e for e in i]
        self.__sorted.sort(key = key, reverse = reverse)
        
    
    def __iter__(self): # 0.3.35
        
        return iter(self.__sorted)
    
    
    def __len__(self): # 0.3.35
        
        return _reckon(self.__sorted)
    
    
    def __getitem__(self, index: int, /): # 0.3.35
        
        return self.__sorted[index]
    
    
    def __contains__(self, item: _T, /): # 0.3.35
        
        return item in self.__sorted
    
    
    def __eq__(self, other, /): # 0.3.35
        
        return type(other) is type(self) and list(self) == list(other)
    
    
    def __ne__(self, other, /): # 0.3.35
        
        return (type(other) is not type(self)) or self.__eq__(other)
        
        
    def __str__(self): # 0.3.35
        
        return "{}({})".format(type(self).__name__, _reckon(self.__l))
    
    
    def __repr__(self): # 0.3.35
        
        return "<{}.{} object: {}>".format(self.__module__, type(self).__name__, self.__str__())
        
        
    def reverse(self, v = False, /):
        """\\@since 0.3.35"""
        
        if v:
            self.__sorted.reverse()
            
            
    def setKey(self, v: _types.Optional[_types.Callable[[_T], _RichComparable]] = None, /):
        """\\@since 0.3.35"""
        
        self.__sorted = self.__l
        if v is not None:
            self.__sorted.sort(key = v)

if False:
    class All:
        """
        @since 0.3.41 (in-code)
        
        A special class featuring `__all__` variable for all its subclasses. Experimental
        """
        
        def __new__(cls, handler: _types.Callable[[], _types.Union[dict[str, _types.Any], _builtins_types.MappingProxyType[str, _types.Any]]] = locals, mode = "public"):
            
            from re import match as _match
            from inspect import getfullargspec
            
            if not callable(handler) or _reckon(getfullargspec(handler).args) != 0:
                error = TypeError("expected a callable without arguments")
                raise error
            
            __all__ = sorted([k for k in handler() if not k.startswith("_")])
            
            if mode == "normal": # everything provided
                __all__ = sorted([k for k in handler()])
                    
            elif mode == "non-private": # no double underscore preceding
                __all__ = sorted([k for k in handler() if _match(r"^_(_)+[^_]+$", k) is not None])
                
            elif mode == "non-protected": # no single underscore preceding
                __all__ = sorted([k for k in handler() if _match(r"^_[^_]+$", k) is not None])
            
            elif mode == "non-public": # no matter how many underscores preceding
                __all__ = sorted([k for k in handler() if _match(r"^_(_)+[^_]+$", k) is not None])
                
            elif mode == "non-sunder": # no single underscores around
                __all__ = sorted([k for k in handler() if _match(r"^_[^_]+_$", k) is None])
                
            elif mode == "non-dunder": # no double underscores around
                __all__ = sorted([k for k in handler() if _match(r"^__[^_]+__$", k) is None])    
                
            elif mode == "non-underscored": # chars other than underscore
                __all__ = sorted([k for k in handler() if _match(r"^_+$", k) is None])
                
            elif mode == "private": # two or more underscores preceding
                __all__ = sorted([k for k in handler() if _match(r"^_(_)+[^_]+$", k) is not None])
                
            elif mode == "protected": # single underscore preceding
                __all__ = sorted([k for k in handler() if _match(r"^_[^_]+$", k) is not None])
                
            elif mode == "public": # no underscores preceding
                __all__ = sorted([k for k in handler() if _match(r"^_(_)+[^_]+$", k) is None])
                
            elif mode == "sunder": # one underscore around
                __all__ = sorted([k for k in handler() if _match(r"^_[^_]+_$", k) is not None])
                
            elif mode == "dunder": # two underscores around
                __all__ = sorted([k for k in handler() if _match(r"^__[^__]+__$", k) is not None])
                
            elif mode == "underscored": # no other chars than underscore
                __all__ = sorted([k for k in handler() if _match(r"^_+$", k) is not None])
                
            else:
                error = TypeError("expected a valid mode")
                raise error
            
            return __all__
        
        @classmethod
        def deprecated(self, handler: _types.Callable[[], _types.Union[dict[str, _types.Any], _builtins_types.MappingProxyType[str, _types.Any]]] = locals, mode = "public"):
            """
            @since 0.3.41
            
            All deprecated declarations. Use as::
            
                __all_deprecated__ = All.deprecated()
            """
            
            from re import match as _match
            from inspect import getfullargspec
            
            if not callable(handler) or _reckon(getfullargspec(handler).args) != 0:
                error = TypeError("expected a callable without arguments")
                raise error
            
            __all_deprecated__ = sorted([k for k in handler() if not k.startswith("_") and hasattr(handler()[k], "__deprecated__")])
            
            if mode == "normal": # everything provided
                __all_deprecated__ = sorted([k for k in handler()])
                    
            elif mode == "non-private": # no double underscore preceding
                __all_deprecated__ = sorted([k for k in handler() if _match(r"^_(_)+[^_]+$", k) is not None and hasattr(handler()[k], "__deprecated__")])
                
            elif mode == "non-protected": # no single underscore preceding
                __all_deprecated__ = sorted([k for k in handler() if _match(r"^_[^_]+$", k) is not None and hasattr(handler()[k], "__deprecated__")])
            
            elif mode == "non-public": # no matter how many underscores preceding
                __all_deprecated__ = sorted([k for k in handler() if _match(r"^_(_)+[^_]+$", k) is not None and hasattr(handler()[k], "__deprecated__")])
                
            elif mode == "non-sunder": # no single underscores around
                __all_deprecated__ = sorted([k for k in handler() if _match(r"^_[^_]+_$", k) is None and hasattr(handler()[k], "__deprecated__")])
                
            elif mode == "non-dunder": # no double underscores around
                __all_deprecated__ = sorted([k for k in handler() if _match(r"^__[^_]+__$", k) is None and hasattr(handler()[k], "__deprecated__")])    
                
            elif mode == "non-underscored": # chars other than underscore
                __all_deprecated__ = sorted([k for k in handler() if _match(r"^_+$", k) is None and hasattr(handler()[k], "__deprecated__")])
                
            elif mode == "private": # two or more underscores preceding
                __all_deprecated__ = sorted([k for k in handler() if _match(r"^_(_)+[^_]+$", k) is not None and hasattr(handler()[k], "__deprecated__")])
                
            elif mode == "protected": # single underscore preceding
                __all_deprecated__ = sorted([k for k in handler() if _match(r"^_[^_]+$", k) is not None and hasattr(handler()[k], "__deprecated__")])
                
            elif mode == "public": # no underscores preceding
                __all_deprecated__ = sorted([k for k in handler() if _match(r"^_(_)+[^_]+$", k) is None and hasattr(handler()[k], "__deprecated__")])
                
            elif mode == "sunder": # one underscore around
                __all_deprecated__ = sorted([k for k in handler() if _match(r"^_[^_]+_$", k) is not None and hasattr(handler()[k], "__deprecated__")])
                
            elif mode == "dunder": # two underscores around
                __all_deprecated__ = sorted([k for k in handler() if _match(r"^__[^__]+__$", k) is not None and hasattr(handler()[k], "__deprecated__")])
                
            elif mode == "underscored": # no other chars than underscore
                __all_deprecated__ = sorted([k for k in handler() if _match(r"^_+$", k) is not None and hasattr(handler()[k], "__deprecated__")])
                
            else:
                error = TypeError("expected a valid mode")
                raise error
            
            return __all_deprecated__
                
    # override builtins.all()
    def all(mode = "public", deprecated = False):
        """
        @since 0.3.41 (in-code)
        
        As a decorator, defines `__all__` variable in specific class. Possible modes (case sensitive):
        - `"normal"` - gets all members, no matter the status.
        - `"private"` - gets all private members that aren't dunder.
        - `"protected"` - gets all protected members that aren't private, sunder and dunder.
        - `"public"` (default value) - gets all public members. This also includes sunder and dunder members.
        - `"sunder"` - gets all sunder (single-underscored) members.
        - `"dunder"` - gets all dunder (doubly-underscored) members.
        - `"non-private"` - gets all non-private members. This list features public, protected, sunder and dunder members.
        - `"non-protected"` - gets all non-protected members. This list features public, private, sunder and dunder members.
        - `"non-public"` - gets all non-public members. This list features private and protected members only.
        - `"non-sunder"` - gets all non-sunder members. This list features public, protected, private and dunder members.
        - `"non-dunder"` - gets all non-dunder members. This list features public, protected, private and sunder members.
        
        There are also some discouraging modes:
        - `"underscored"` - gets all members whose names are created with underscores only (like `__`).
        - `"non-underscored"` - gets all members whose names aren't created with underscores only. This list features \\
            all public, protected, private, sunder and dunder methods, what means its very similar to `"normal"`.
            
        Use as::
        
            @~.util.all("<mode>") # valid value from above except <mode> or leave it empty,
            # as ~.util.all()
            class Test: ... # members
        
        In this example, `Test.__all__` will normally obtain all public members.
        """
        
        def _all(t: type[_T], /):
            
            from re import match as _match
            
            if not isinstance(t, type):
                error = TypeError("expected a class or type alias")
                raise error
            
            v = t.__dict__
            t = _typing.cast(type[_T], t)
            t.__all__ = sorted([k for k in v if not k.startswith("_")])
            
            if mode == "normal": # everything provided
                t.__all__ = sorted([k for k in v])
                    
            elif mode == "non-private": # no double underscore preceding
                t.__all__ = sorted([k for k in v if _match(r"^_(_)+[^_]+$", k) is not None])
                
            elif mode == "non-protected": # no single underscore preceding
                t.__all__ = sorted([k for k in v if _match(r"^_[^_]+$", k) is not None])
            
            elif mode == "non-public": # no matter how many underscores preceding
                t.__all__ = sorted([k for k in v if _match(r"^_(_)+[^_]+$", k) is not None])
                
            elif mode == "non-sunder": # no single underscores around
                t.__all__ = sorted([k for k in v if _match(r"^_[^_]+_$", k) is None])
                
            elif mode == "non-dunder": # no double underscores around
                t.__all__ = sorted([k for k in v if _match(r"^__[^_]+__$", k) is None])    
                
            elif mode == "non-underscored": # chars other than underscore
                t.__all__ = sorted([k for k in v if _match(r"^_+$", k) is None])
                
            elif mode == "private": # two or more underscores preceding
                t.__all__ = sorted([k for k in v if _match(r"^_(_)+[^_]+$", k) is not None])
                
            elif mode == "protected": # single underscore preceding
                t.__all__ = sorted([k for k in v if _match(r"^_[^_]+$", k) is not None])
                
            elif mode == "public": # no underscores preceding
                t.__all__ = sorted([k for k in v if _match(r"^_(_)+[^_]+$", k) is None])
                
            elif mode == "sunder": # one underscore around
                t.__all__ = sorted([k for k in v if _match(r"^_[^_]+_$", k) is not None])
                
            elif mode == "dunder": # two underscores around
                t.__all__ = sorted([k for k in v if _match(r"^__[^__]+__$", k) is not None])
                
            elif mode == "underscored": # no other chars than underscore
                t.__all__ = sorted([k for k in v if _match(r"^_+$", k) is not None])
                
            else:
                error = TypeError("expected a valid mode")
                raise error
            
            if deprecated:
                t.__all_deprecated__ = sorted([n for n in vars(t) if hasattr(vars(t)[n], "__deprecated__")])
                
            t.__all__ = [e for e in t.__all__ if e != "__all__"]
            return t
                
        return _all
            
if __name__ == "__main__":
    error = RuntimeError("This file is not for compiling, consider importing it instead.")
    raise error
    
__all__ = sorted([k for k in globals() if not k.startswith("_")]) # 0.3.41: sorted()
__all_deprecated__ = sorted([k for k in globals() if hasattr(globals()[k], "__deprecated__")])
"""
@since 0.3.41

Returns all deprecated declarations within this module.
"""
