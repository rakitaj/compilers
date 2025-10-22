from __future__ import annotations

import argparse
import os
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Self

from compiler import generate_assembly
from lexer import Lexer
from parser import Parser, Program
from tokens import Token

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
        do_compile = bool(args.compile) or False
        do_dump_tokens = bool(args.debug_dump_tokens) or False
        return cls(filepath, do_compile, do_dump_tokens)

    def get_filename(self) -> str:
        return self.filepath.stem

    def get_assembly_filename(self) -> str:
        return f"{self.get_filename()}.s"


arg_parser = argparse.ArgumentParser()

arg_parser.add_argument("file", help="Path to the source file.", type=str)
arg_parser.add_argument("--compile", help="Compile instead of just generating the assembly.", type=bool)
args = arg_parser.parse_args()

parsed_args = ProgramArgs.from_args(args)

script_dir = Path(__file__).parent
# Create a new file in the same directory
output_file = script_dir / parsed_args.get_assembly_filename()

with open(parsed_args.filepath, "r") as fp:
    program_source = fp.read()

assembly = program_source | pipe(lex) | pipe(parse) | pipe(assemble)

with open(output_file, "w") as file:
    for line in assembly:
        file.write(line)
        file.write(os.linesep)

if parsed_args.debug_dump_tokens:
    tokens = program_source | pipe(lex)
    with open(output_file, "w") as file:
        