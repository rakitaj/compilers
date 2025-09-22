from parser import Program, Function, Statement, Expression

def post_order(node: Program | Function | Statement | Expression, depth: int) -> list[str]:
    if isinstance(node, Program):
        assembly: list[str] = []
        for function in node.functions:
            after = post_order(function, depth + 1)
            assembly.extend([f".globl {function.name}", f"{function.name}:"])
            assembly.extend(after)
        return assembly
    elif isinstance(node, Function):
        assembly: list[str] = []
        for statement in node.statements:
            after = post_order(statement, depth + 1)
            assembly.extend(after)
        return assembly
    elif isinstance(node, Statement):
        expr_asm = post_order(node.value, depth + 1)
        expr_asm.append("ret")
        return expr_asm
        # Hack! A statement can only have one expr right now.
    else: # Always an expression by this point
        return [f"movl ${node.value}, %eax"]

def generate_assembly(program: Program) -> list[str]:
    assembly = post_order(program, 0)
    return assembly

