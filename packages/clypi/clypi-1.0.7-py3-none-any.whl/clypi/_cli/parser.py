import importlib.util
import inspect
import re
import typing as t
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from types import NoneType, UnionType

from clypi._cli import type_util

HAS_V6E = importlib.util.find_spec("v6e") is not None


class UnparseableException(Exception):
    pass


def dash_to_snake(s: str) -> str:
    return re.sub(r"^-+", "", s).replace("-", "_")


def snake_to_dash(s: str) -> str:
    return s.replace("_", "-")


def normalize_args(args: t.Sequence[str]) -> list[str]:
    new_args: list[str] = []
    for a in args:
        if a.startswith("-") and "=" in a:
            new_args.extend(a.split("=", 1))
        else:
            new_args.append(a)
    return new_args


@dataclass
class Arg:
    value: str
    orig: str
    arg_type: t.Literal["long-opt", "short-opt", "pos"]

    def is_pos(self):
        return self.arg_type == "pos"

    def is_long_opt(self):
        return self.arg_type == "long-opt"

    def is_short_opt(self):
        return self.arg_type == "short-opt"

    def is_opt(self):
        return self.is_long_opt() or self.is_short_opt()


def parse_as_attr(arg: str) -> Arg:
    if arg.startswith("--"):
        return Arg(value=dash_to_snake(arg), orig=arg, arg_type="long-opt")

    if arg.startswith("-"):
        return Arg(value=dash_to_snake(arg), orig=arg, arg_type="short-opt")

    return Arg(value=arg, orig=arg, arg_type="pos")


def _parse_builtin(builtin: type) -> t.Callable[[t.Any], t.Any]:
    def inner(value: t.Any):
        if isinstance(value, list):
            value = value[0]
        return builtin(value)

    return inner


def _parse_list(_type: t.Any) -> t.Callable[[t.Any], list[t.Any]]:
    def inner(value: t.Any):
        if not isinstance(value, list):
            raise ValueError(
                f"Don't know how to parse {value!r} as {type_util.type_to_str(_type)}"
            )

        inner_type = _type.__args__[0]
        parser = from_type(inner_type)
        return [parser(x) for x in value]

    return inner


def _parse_tuple(_type: t.Any) -> t.Callable[[t.Any], tuple[t.Any]]:
    def inner(value: t.Any) -> tuple[t.Any]:
        # Tuples of size 1 are passed in as strings
        if isinstance(value, str):
            value = (value,)

        if not isinstance(value, tuple | list):
            raise ValueError(
                f"Don't know how to parse {value!r} as {type_util.type_to_str(_type)}"
            )

        # TODO: can be made more efficient
        inner_types = _type.__args__
        if inner_types[-1] is Ellipsis:
            inner_types = [inner_types[0]] * len(value)

        if len(inner_types) > len(value):
            raise ValueError(
                f"Not enough arguments for type {type_util.type_to_str(_type)} (got {value})"
            )

        ret: list[t.Any] = []
        for val, inner_type in zip(value, inner_types):
            ret.append(from_type(inner_type)(val))
        return tuple(ret)

    return inner


def _parse_union(_type: UnionType) -> t.Callable[[t.Any], t.Any]:
    def inner(value: t.Any):
        errors: list[Exception] = []
        for a in _type.__args__:
            try:
                return from_type(a)(value)
            except (ValueError, TypeError) as e:
                errors.append(e)
            except UnparseableException:
                pass

        if errors:
            raise errors[0]

    return inner


def _parse_literal(_type: t.Any) -> t.Callable[[t.Any], t.Any]:
    def inner(value: t.Any):
        if isinstance(value, list):
            value = value[0]

        for a in _type.__args__:
            if a == value:
                return value

        raise ValueError(
            f"Value {value} is not a valid choice between {type_util.type_to_str(_type)}"
        )

    return inner


def _parse_none(value: t.Any) -> None:
    if value is not None:
        raise ValueError(f"Value {value!r} is not None")
    return None


def _parse_bool(value: t.Any) -> bool:
    if value.lower() in ("y", "yes", "true"):
        return True
    if value.lower() in ("n", "no", "false"):
        return False
    raise ValueError(f"Value {value!r} is not a valid boolean")


def _parse_enum(_type: type[Enum]):
    def inner(value: t.Any) -> Enum:
        if not isinstance(value, str):
            raise ValueError(
                f"Don't know how to parse {value!r} as {type_util.type_to_str(_type)}"
            )

        for enum_val in _type:
            if value.lower() == enum_val.name.lower():
                return enum_val

        raise ValueError(
            f"Value {value} is not a valid choice between {type_util.type_to_str(_type)}"
        )

    return inner


def from_v6e(_type: t.Any) -> t.Callable[[t.Any], t.Any] | None:
    import v6e as v  # type: ignore

    v6e_builtins: dict[t.Any, t.Callable[[t.Any], t.Any]] = {
        bool: v.bool(),
        int: v.int(),
        float: v.float(),
        str: v.str(),
        Path: v.path(),
        datetime: v.datetime(),
        timedelta: v.timedelta(),
    }
    if _type in v6e_builtins:
        return v6e_builtins[_type]

    return None


@type_util.ignore_annotated
def from_type(_type: t.Any) -> t.Callable[[t.Any], t.Any]:
    if HAS_V6E and (parser := from_v6e(_type)):
        return parser

    if _type is bool:
        return _parse_bool

    if _type in (int, float, str, Path):
        return _parse_builtin(_type)

    if type_util.is_list(_type):
        return _parse_list(_type)

    if type_util.is_tuple(_type):
        return _parse_tuple(_type)

    if isinstance(_type, UnionType):
        return _parse_union(_type)

    if t.get_origin(_type) == t.Literal:
        return _parse_literal(_type)

    if _type is NoneType:
        return _parse_none

    if inspect.isclass(_type) and issubclass(_type, Enum):
        return _parse_enum(_type)

    raise UnparseableException(
        f"Don't know how to parse as {type_util.type_to_str(_type)} ({type(_type)})"
    )


Nargs: t.TypeAlias = t.Literal["*", "+"] | float


@dataclass
class CurrentCtx:
    name: str = ""
    nargs: Nargs = 0
    max_nargs: Nargs = 0

    _collected: list[str] = field(init=False, default_factory=list)

    def has_more(self) -> bool:
        if isinstance(self.nargs, float | int):
            return self.nargs > 0
        return True

    def needs_more(self) -> bool:
        if isinstance(self.nargs, float | int):
            return self.nargs > 0
        elif self.nargs == "+":
            return True
        return False

    def collect(self, item: str) -> None:
        if isinstance(self.nargs, float | int):
            self.nargs -= 1
        elif self.nargs == "+":
            self.nargs = "*"

        self._collected.append(item)

    @property
    def collected(self) -> str | list[str]:
        if self.max_nargs == 1:
            return self._collected[0]
        return self._collected

    def __bool__(self) -> bool:
        return bool(self.name)
