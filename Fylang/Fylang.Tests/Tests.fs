module Tests

open System
open Xunit
open FsUnit
open Fylang.Compiler.Lexer;

[<Fact>]
let ``scanWhile with whitespace predicate`` () =
    let source_code = "int main(void) { return 2; }"
    let is_valid_for_identifier: char -> bool = fun c -> Char.IsAsciiLetterOrDigit c || c = '_'
    scanWhile source_code 0 is_valid_for_identifier |> should equal 3
