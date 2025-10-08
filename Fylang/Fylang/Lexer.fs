namespace Fylang.Compiler

module Lexer = 

    type TokenType = 
        | LBrace
        | RBrace
        | LParen
        | RParen
        | Semicolon
        | KeywordInt
        | KeywordReturn
        | Identifier of string
        | LiteralInt of int32
        | EOF

    type Location = {
        Line: int
        Column: int
        Idx: int
    }

    type Token = {
        TokenType: TokenType
        Lexeme: string
        Location: Location
    }

    exception InvalidCharacter of string * Location

    let advance location = { location with Column = location.Column + 1; Idx = location.Idx + 1 }
    let advanceLine location = { location with Column = 1; Line = location.Line + 1; Idx = location.Idx + 1}
    let isLetter (c: char) = System.Char.IsAsciiLetter(c)

    let rec scanWhile (str: string) (idx: int) (pred: char -> bool): int =
        if idx < str.Length && pred str.[idx] then
            scanWhile str (idx + 1) pred
        else
            idx


    let singleCharTokens = [ 
        '{', TokenType.LBrace; '}', TokenType.RBrace;
        '(', TokenType.LParen; ')', TokenType.RParen; 
        ';', TokenType.Semicolon; ] |> Map.ofSeq

    let keywordTokens = [
        "return", TokenType.KeywordReturn; "int", TokenType.KeywordInt; ] |> Map.ofSeq

    let lex (sourceCode: string) =
        let rec lexInner (source: string) (location: Location) (acc: list<Token>) = 
            if location.Idx > source.Length then
                let token = { TokenType = TokenType.EOF; Lexeme = "EOF"; Location = location |> advance}
                (token :: acc)
            else
                let c = source.[location.Idx]
                match c with 
                | '{' | '}' | '(' | ')' | ';' ->
                    let token_type = Map.find c singleCharTokens
                    let token = { TokenType = token_type; Lexeme = string c ; Location = location }
                    lexInner source (location |> advance) (token :: acc)
                | ' ' -> lexInner source (location |> advance) acc
                // | c when isLetter c -> 
                | _ -> raise (InvalidCharacter ($"Unexpected character {c}", location))
        lexInner sourceCode { Line = 1; Column = 1; Idx = 0} []