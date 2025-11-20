module Tests

open System
open Xunit
open FsUnit
open Fylang.Compiler.Lexer;
open System.IO
open Newtonsoft.Json

let parseKnownTokens json : array<Token> =
    JsonConvert.DeserializeObject<Token array> json


[<Fact>]
let ``scanWhile with whitespace predicate`` () =
    let source_code = "int main(void) { return 2; }"
    let is_valid_for_identifier: char -> bool = fun c -> Char.IsAsciiLetterOrDigit c || c = '_'
    scanWhile source_code 0 is_valid_for_identifier |> should equal 3

[<Theory>]
[<InlineData(1, "multi_digit")>]
let ``lex all`` (chapter: int) (filename: string) =
    let sourceFilePath = System.IO.Path.Combine(".", $"chapter-0{chapter}", "valid", $"{filename}.c")
    let tokensPath = System.IO.Path.Combine(".", $"chapter-0{chapter}", "valid", $"{filename}.tokens") 
    let tokens = File.ReadAllText sourceFilePath |> lex
    let expectedTokens = File.ReadAllText tokensPath |> parseKnownTokens
    tokens |> should equal expectedTokens
