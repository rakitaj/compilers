import argparse
import subprocess
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Self

from compiler import generate_assembly
from lexer import Lexer
from parser import Parser, Program
from tokens import Token, TokenEncoder

from collections.abc import Callable


class pipe[T, U]:
    def __init__(self, func: Callable[[T], U]):
        self.func = func

    def __ror__(self, value: T) -> U:
        return self.func(value)


def lex(source: str):
    return Lexer(source).lex()


def parse(tokens: list[Token]) -> Program:
    return Parser(tokens).parse_program()


def assemble(program: Program) -> list[str]:
    return generate_assembly(program)


@dataclass
class ProgramArgs:
    filepath: Path
    compile: bool
    debug_dump_tokens: bool

    @classmethod
    def from_args(cls, args: argparse.Namespace) -> Self:
        filepath = Path(args.file)
        do_compile = bool(args.compile)
        do_dump_tokens = bool(args.debug_dump_tokens)
        return cls(filepath, do_compile, do_dump_tokens)

    def get_filename(self) -> str:
        return self.filepath.stem

    def get_assembly_filename(self) -> str:
        return f"{self.get_filename()}.s"


def run(options: ProgramArgs) -> None:
    with open(parsed_args.filepath, "r") as fp:
        program_source = fp.read()

    tokens = program_source | pipe(lex)
    assembly = tokens | pipe(parse) | pipe(generate_assembly)

    script_dir = Path(__file__).parent
    # Create the assembly file in the same directory
    assembly_filepath = script_dir / parsed_args.get_assembly_filename()

    with open(assembly_filepath, "w") as fp:
        for line in assembly:
            fp.write(line)
            fp.write("\n")

    if options.compile:
        command: list[str | Path] = [
            "clang",
            "-Wall",
            "-Wextra",
            assembly_filepath,
            "-o",
            options.get_filename(),
        ]

        try:
            result = subprocess.run(command, check=True, capture_output=True, text=True)
            print("Compilation successful:")
            print(result.stdout)
        except subprocess.CalledProcessError as e:
            print(f"Compilation failed with error code {e.returncode}:")
            print(e.stderr)

    if parsed_args.debug_dump_tokens:
        tokens_json = json.dumps(tokens, cls=TokenEncoder)
        print(tokens_json)


arg_parser = argparse.ArgumentParser()

arg_parser.add_argument("file", help="Path to the source file.", type=str)
arg_parser.add_argument(
    "--compile", help="Compile instead of just generating the assembly.", action="store_true"
)
arg_parser.add_argument(
    "--debug-dump-tokens", help="Debug: Dump the internal token representation to stdout", action="store_true"
)
args = arg_parser.parse_args()

parsed_args = ProgramArgs.from_args(args)
run(parsed_args)
