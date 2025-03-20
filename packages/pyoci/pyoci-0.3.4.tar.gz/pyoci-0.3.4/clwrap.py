from ast import Attribute
from inspect import Signature, getmembers
from typing import Protocol, dataclass_transform, Annotated


def compile_descriptor(
    args_signature: Signature,
    exprs: list[str],
):
    exprs = ["args = []", *exprs, "return args"]
    return compile_dynamic_function(
        "__descriptor",
        code=exprs,
        signature=args_signature,
    )


class UnwrapContainer[**P](Protocol):
    def __init__(self, *args: P.args, **kwargs: P.kwargs): ...


@dataclass_transform()
class CliArgs:
    # def __init__(self, cls: type):
    #     self.__call__ = compile_args_wrapper(  # type: ignore
    #         function_name=f"__dynamic_wrapper__{cls.__name__}",
    #         args_signature=Signature(),  # TODO
    #         exprs=[],  # TODO
    #     )

    def __init_subclass__(cls) -> None:
        cls.descriptor = ...
        # possibly bind cls.init here

    @classmethod
    def construct[**Args](
        cls: type[UnwrapContainer[Args]],
        *args: Args.args,
        **kwargs: Args.kwargs,
    ) -> list[str]: ...


class CliArg(Protocol):
    def __init__(self, value: str): ...

    def expr(self, args_append_ref: Attribute) -> str: ...


class flag(CliArg):
    # NOTE: defaults aren't encoded, they are purely for documentation
    def __init__(self, value: str, default: bool = False):
        self.value = value


def compile_dynamic_function(
    name: str,
    code: list[str],
    signature: Signature,
    filename: str = "<dynamic>",
):
    code_header = f"def {name}{signature}:\n    "
    code_string = code_header + "\n    ".join(code)

    bytecode = compile(code_string, filename, "exec")

    temp_globs = {}
    eval(bytecode, temp_globs)
    return temp_globs[name]


def partial_struct[**Fields, ContainerType: UnwrapContainer](
    struct: type[UnwrapContainer[Fields]] | type[ContainerType],
): ...


#! To future me: consider manually specifying the ifs for command-line building as a temporary solution
#! extend via args = super().__to_args__()


def nflag() -> bool: ...
