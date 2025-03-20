from clypi.colors import style


class ClypiException(Exception):
    pass


class MaxAttemptsException(ClypiException):
    pass


class AbortException(ClypiException):
    pass


def format_traceback(err: BaseException) -> list[str]:
    # Get the traceback bottom up
    tb: list[BaseException] = [err]
    while tb[-1].__cause__ is not None:
        tb.append(tb[-1].__cause__)

    lines: list[str] = []
    for i, e in enumerate(reversed(tb)):
        icon = "  " * (i - 1) + " ↳ " if i != 0 else ""
        s = style(f"{icon}{str(e)}", fg="red")
        lines.append(s)
    return lines


def print_traceback(err: BaseException) -> None:
    for line in format_traceback(err):
        print(line)
