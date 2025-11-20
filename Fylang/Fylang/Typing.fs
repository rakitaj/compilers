namespace Fylang.Compiler

module Typing = 

     type CType = 
        | Int of int32
        | Char of int8
        | Float of float32 