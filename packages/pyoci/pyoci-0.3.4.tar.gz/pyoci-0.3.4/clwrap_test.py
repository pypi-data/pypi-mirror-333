from clwrap import CliArgs
from dataclasses import InitVar


class ExecArgs(CliArgs):
    process: str = ""
    test: int = 0


arglist = ExecArgs.init("test", 2)


def exec(args: list[str]) -> int: ...


# @argstruct(ExecArgs)
# def exec(args: ExecArgs):
#     print(args.to_a())


# exec["--log=false"]("test")
