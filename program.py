import argparse
import os
from pathlib import Path
from typing import Self
from dataclasses import dataclass
from lexer import Lexer
from parser import Parser
from compiler import generate_assembly

@dataclass
class ProgramArgs:
    filepath: Path
    compile: bool

    @classmethod
    def from_args(cls, args: argparse.Namespace) -> Self:
        filepath = Path(args.file)
        do_compile = bool(args.compile) or False
        return cls(filepath, do_compile)
    
    def get_filename(self) -> str:
        return self.filepath.stem
    
    def get_assembly_filename(self) -> str:
        return f"{parsed_args.get_filename()}.s"

def compile_source_to_assembly(program_source: str) -> list[str]:
    lexer = Lexer(program_source)
    tokens = lexer.lex()
    parser = Parser(tokens)
    program_ast = parser.parse_program()
    assembly = generate_assembly(program_ast)
    return assembly

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

assembly = compile_source_to_assembly(program_source)

with open(output_file, "w") as file:
    for line in assembly:
        file.write(line)
        file.write(os.linesep)
    