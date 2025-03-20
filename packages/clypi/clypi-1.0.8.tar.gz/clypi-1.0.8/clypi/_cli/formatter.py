from __future__ import annotations

import typing as t
from dataclasses import dataclass
from functools import cached_property

from clypi import boxed, indented, stack
from clypi._cli import type_util
from clypi.colors import ColorType
from clypi.exceptions import format_traceback

if t.TYPE_CHECKING:
    from clypi.cli import Argument, Command


@dataclass
class ProgramConfig:
    prog: str


def _ext(ls: list[str], s: str | list[str] | None) -> None:
    if isinstance(s, str):
        ls.append(s)
    elif isinstance(s, list):
        ls.extend(s)
    return None


class Formatter(t.Protocol):
    def format_help(
        self,
        prog: list[str],
        description: str | None,
        epilog: str | None,
        options: list[Argument],
        positionals: list[Argument],
        subcommands: list[type[Command]],
        exception: Exception | None,
    ) -> str: ...


@dataclass
class ClypiFormatter:
    def __init__(self, boxed: bool = True) -> None:
        self.boxed = boxed

    @cached_property
    def theme(self):
        from clypi.configuration import get_config

        return get_config().theme

    def _maybe_boxed(
        self, *columns: list[str], title: str, color: ColorType | None = None
    ) -> list[str]:
        first_col, *rest = columns
        if not self.boxed:
            section_title = self.theme.section_title(title)

            # For non-boxed design, we just indent the first col a bit so that it looks
            # like it's inside the section
            stacked = stack(indented(first_col), *rest, lines=True)
            return [section_title] + stacked + [""]

        stacked = stack(first_col, *rest, lines=True)
        return list(boxed(stacked, width="max", title=title, color=color))

    def _format_option(self, option: Argument) -> tuple[str, ...]:
        name = self.theme.long_option(option.display_name)
        short_usage = self.theme.short_option(
            option.short_display_name if option.short else ""
        )
        type_str = self.theme.type_str(type_util.type_to_str(option.arg_type).upper())
        help = option.help or ""

        return name, short_usage, type_str, help

    def _format_options(self, options: list[Argument]) -> list[str] | None:
        if not options:
            return None

        name: list[str] = []
        short_usage: list[str] = []
        type_str: list[str] = []
        help: list[str] = []
        for o in options:
            u, su, ts, hp = self._format_option(o)
            name.append(u)
            short_usage.append(su)
            type_str.append(ts)
            help.append(hp)

        return self._maybe_boxed(name, short_usage, type_str, help, title="Options")

    def _format_positional(self, positional: Argument) -> t.Any:
        name = self.theme.positional(positional.name)
        help = positional.help or ""
        type_str = self.theme.type_str(
            type_util.type_to_str(positional.arg_type).upper()
        )

        return name, type_str, help

    def _format_positionals(
        self, positionals: list[Argument]
    ) -> list[str] | str | None:
        if not positionals:
            return None

        name: list[str] = []
        type_str: list[str] = []
        help: list[str] = []
        for p in positionals:
            n, ts, hp = self._format_positional(p)
            name.append(n)
            type_str.append(ts)
            help.append(hp)

        return self._maybe_boxed(name, type_str, help, title="Arguments")

    def _format_subcommand(self, subcmd: type[Command]) -> tuple[str, str]:
        name = self.theme.subcommand(subcmd.prog())
        help = subcmd.help() or ""
        return name, help

    def _format_subcommands(
        self, subcommands: list[type[Command]]
    ) -> list[str] | str | None:
        if not subcommands:
            return None

        name: list[str] = []
        help: list[str] = []
        for p in subcommands:
            n, hp = self._format_subcommand(p)
            name.append(n)
            help.append(hp)

        return self._maybe_boxed(name, help, title="Subcommands")

    def _format_header(
        self,
        prog: list[str],
        options: list[Argument],
        positionals: list[Argument],
        subcommands: list[type[Command]],
    ) -> list[str] | str | None:
        prefix = self.theme.usage("Usage:")
        prog_str = self.theme.prog(" ".join(prog))

        option = " [" + self.theme.long_option("OPTIONS") + "]" if options else ""
        command = self.theme.subcommand(" COMMAND") if subcommands else ""
        positional = (
            " " + " ".join(self.theme.positional(p.name.upper()) for p in positionals)
            if positionals
            else ""
        )

        return [f"{prefix} {prog_str}{option}{command}{positional}", ""]

    def _format_description(self, description: str | None) -> list[str] | str | None:
        if not description:
            return None
        return [description, ""]

    def _format_epilog(self, epilog: str | None) -> list[str] | str | None:
        if not epilog:
            return None
        return ["", epilog]

    def _format_exception(self, exception: Exception | None) -> list[str] | str | None:
        if not exception:
            return None

        return self._maybe_boxed(
            format_traceback(exception), title="Error", color="red"
        )

    def format_help(
        self,
        prog: list[str],
        description: str | None,
        epilog: str | None,
        options: list[Argument],
        positionals: list[Argument],
        subcommands: list[type[Command]],
        exception: Exception | None,
    ) -> str:
        lines: list[str] = []

        # Header
        _ext(lines, self._format_header(prog, options, positionals, subcommands))

        # Description
        _ext(lines, self._format_description(description))

        # Subcommands
        _ext(lines, self._format_subcommands(subcommands))

        # Positionals
        _ext(lines, self._format_positionals(positionals))

        # Options
        _ext(lines, self._format_options(options))

        # Epilog
        _ext(lines, self._format_epilog(epilog))

        # Exceptions
        _ext(lines, self._format_exception(exception))

        return "\n".join(lines)
