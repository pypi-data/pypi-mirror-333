import re
from typing import List, Dict, Any
import sys
# from quantumx.quantumx_builtins import builtins as builtin_functions
from quantumx.quantumx_builtins import builtins as builtin_functions

class Token:
    def __init__(self, type_: str, value: str):
        self.type = type_
        self.value = value

    def __repr__(self):
        return f"Token({self.type}, {self.value})"

class Lexer:
    def __init__(self, code: str):
        self.code = code
        self.pos = 0
        self.tokens = []
        self.rules = [
            (r'//.*', 'COMMENT'),
            (r'```(?:.*?```|$)', None),
            (r'\bset\b', 'SET'),
            (r'\bto\b', 'TO'),
            (r'\bimport\b', 'IMPORT'),
            (r'\bfunc\b', 'FUNC'),
            (r'\bbegin\b', 'BEGIN'),
            (r'\bend\b', 'END'),
            (r'\bwhen\b', 'WHEN'),
            (r'\belse\b', 'ELSE'),
            (r'\brepeat\b', 'REPEAT'),
            (r'\breturn\b', 'RETURN'),
            (r'\boutput\b', 'OUTPUT'),
            (r'\binput\b', 'INPUT'),
            (r'\bforeach\b', 'FOREACH'),
            (r'\bfor\b', 'FOR'),
            (r'\bin\b', 'IN'),
            (r'\bif\b', 'IF'),
            (r'\belsif\b', 'ELSIF'),
            (r'-?[0-9]+', 'NUMBER'),  # Updated to support negative numbers
            (r'[a-zA-Z_][a-zA-Z0-9_]*', 'IDENTIFIER'),
            (r'[-+*/]', 'OPERATOR'),
            (r'[><=]', 'COMPARISON'),
            (r',', 'COMMA'),
            (r'\(', 'LPAREN'),
            (r'\)', 'RPAREN'),
            (r'\[', 'LBRACKET'),
            (r'\]', 'RBRACKET'),
            (r'"[^"]*"', 'STRING'),
            (r'\s+', None),
        ]

    def tokenize(self) -> List[Token]:
        while self.pos < len(self.code):
            matched = False
            for pattern, token_type in self.rules:
                regex = re.compile(pattern)
                match = regex.match(self.code, self.pos)
                if match:
                    if token_type:
                        value = match.group(0)
                        self.tokens.append(Token(token_type, value))
                    self.pos = match.end()
                    matched = True
                    break
            if not matched:
                print(f"Failed at: {self.code[self.pos:self.pos+10]}")
                raise SyntaxError(f"Invalid syntax at position {self.pos}")
        return self.tokens

class Node:
    def __init__(self, type_: str, value: Any = None, children: List['Node'] = None):
        self.type = type_
        self.value = value
        self.children = children or []

    def __repr__(self):
        return f"Node({self.type}, {self.value}, {self.children})"

class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0

    def current_token(self) -> Token:
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def consume(self, type_: str) -> Token:
        token = self.current_token()
        if token and token.type == type_:
            self.pos += 1
            return token
        raise SyntaxError(f"Expected {type_}, got {token.type if token else 'EOF'}")

    def parse(self) -> List[Node]:
        statements = []
        while self.pos < len(self.tokens):
            statements.append(self.parse_statement())
        return statements

    def parse_statement(self) -> Node:
        token = self.current_token()
        if token.type == 'SET':
            return self.parse_variable()
        elif token.type == 'FUNC':
            return self.parse_function()
        elif token.type == 'WHEN':
            return self.parse_when()
        elif token.type == 'IF':
            return self.parse_if()
        elif token.type == 'REPEAT':
            return self.parse_repeat()
        elif token.type == 'FOREACH':
            return self.parse_foreach()
        elif token.type == 'FOR':
            return self.parse_for()
        elif token.type == 'OUTPUT':
            return self.parse_output()
        elif token.type == 'INPUT':
            return self.parse_input()
        elif token.type == 'RETURN':
            return self.parse_return()
        elif token.type == 'IMPORT':
            return self.parse_import()
        elif token.type == 'IDENTIFIER' and self.pos + 1 < len(self.tokens) and self.tokens[self.pos + 1].type == 'LPAREN':
            func_name = token.value
            self.pos += 1
            return self.parse_call(func_name)
        else:
            raise SyntaxError(f"Unexpected token: {token}")

    def parse_variable(self) -> Node:
        self.consume('SET')
        var_name = self.consume('IDENTIFIER').value

        # Check if there's an index after the identifier
        if self.current_token() and self.current_token().type == 'LBRACKET':
            expr = self.parse_index(var_name)
        else:
            self.consume('TO')
            expr = self.parse_expression_or_call()

        return Node('Variable', var_name, [expr])

    def parse_function(self) -> Node:
        self.consume('FUNC')
        func_name = self.consume('IDENTIFIER').value
        self.consume('LPAREN')
        params = []
        if self.current_token().type != 'RPAREN':
            params.append(self.consume('IDENTIFIER').value)
            while self.current_token().type == 'COMMA':
                self.consume('COMMA')
                params.append(self.consume('IDENTIFIER').value)
        self.consume('RPAREN')
        self.consume('BEGIN')
        body = []
        while self.current_token().type != 'END':
            body.append(self.parse_statement())
        self.consume('END')
        return Node('Function', func_name, [Node('Params', params), Node('Block', None, body)])

    def parse_when(self) -> Node:
        self.consume('WHEN')
        condition = self.parse_expression()
        self.consume('BEGIN')
        then_block = []
        while self.current_token().type not in ['ELSE', 'END']:
            then_block.append(self.parse_statement())
        if self.current_token().type == 'ELSE':
            self.consume('ELSE')
            else_block = []
            while self.current_token().type != 'END':
                else_block.append(self.parse_statement())
        else:
            else_block = []
        self.consume('END')
        return Node('When', None, [condition, Node('Block', None, then_block), Node('Block', None, else_block)])

    def parse_if(self) -> Node:
        self.consume('IF')
        condition = self.parse_expression()
        self.consume('BEGIN')
        if_block = []
        while self.current_token() and self.current_token().type not in ['ELSIF', 'ELSE', 'END']:
            if_block.append(self.parse_statement())

        elsif_blocks = []
        while self.current_token() and self.current_token().type == 'ELSIF':
            self.consume('ELSIF')
            elsif_condition = self.parse_expression()
            self.consume('BEGIN')
            elsif_body = []
            while self.current_token() and self.current_token().type not in ['ELSIF', 'ELSE', 'END']:
                elsif_body.append(self.parse_statement())
            elsif_blocks.append(Node('Elsif', None, [elsif_condition, Node('Block', None, elsif_body)]))

        else_block = []
        if self.current_token() and self.current_token().type == 'ELSE':
            self.consume('ELSE')
            self.consume('BEGIN')
            while self.current_token() and self.current_token().type != 'END':
                else_block.append(self.parse_statement())

        self.consume('END')
        return Node('If', None, [
            condition,
            Node('Block', None, if_block),
            Node('ElsifBlocks', None, elsif_blocks),
            Node('Block', None, else_block)
        ])

    def parse_repeat(self) -> Node:
        self.consume('REPEAT')
        count = self.consume('NUMBER').value
        self.consume('BEGIN')
        body = []
        while self.current_token().type != 'END':
            body.append(self.parse_statement())
        self.consume('END')
        return Node('Repeat', int(count), [Node('Block', None, body)])

    def parse_foreach(self) -> Node:
        self.consume('FOREACH')
        var_name = self.consume('IDENTIFIER').value
        self.consume('TO')
        sequence = self.parse_expression()
        self.consume('BEGIN')
        body = []
        while self.current_token().type != 'END':
            body.append(self.parse_statement())
        self.consume('END')
        return Node('Foreach', var_name, [sequence, Node('Block', None, body)])

    def parse_for(self) -> Node:
        self.consume('FOR')
        var_name = self.consume('IDENTIFIER').value
        self.consume('IN')
        sequence = self.parse_expression_or_call()
        self.consume('BEGIN')
        body = []
        while self.current_token() and self.current_token().type != 'END':
            body.append(self.parse_statement())
        self.consume('END')
        return Node('For', var_name, [sequence, Node('Block', None, body)])

    def parse_output(self) -> Node:
        self.consume('OUTPUT')
        self.consume('LPAREN')
        args = []
        while self.current_token() and self.current_token().type != 'RPAREN':
            args.append(self.parse_expression())
            if self.current_token() and self.current_token().type == 'COMMA':
                self.consume('COMMA')
        self.consume('RPAREN')
        return Node('Output', None, [Node('Args', None, args)])

    def parse_input(self) -> Node:
        self.consume('INPUT')
        self.consume('LPAREN')
        args = []
        while self.current_token() and self.current_token().type != 'RPAREN':
            args.append(self.parse_expression())
            if self.current_token() and self.current_token().type == 'COMMA':
                self.consume('COMMA')
        self.consume('RPAREN')
        return Node('Input', None, [Node('Args', None, args)])

    def parse_return(self) -> Node:
        self.consume('RETURN')
        expr = self.parse_expression()
        return Node('Return', None, [expr])

    def parse_import(self) -> Node:
        self.consume('IMPORT')
        module_name = self.consume('IDENTIFIER').value
        return Node('Import', module_name)

    def parse_index(self, var_name: str) -> Node:
        self.consume('LBRACKET')
        index = self.parse_expression()
        self.consume('RBRACKET')
        return Node('Index', None, [Node('Identifier', var_name), index])

    def parse_expression_or_call(self) -> Node:
        token = self.current_token()
        if (token.type == 'IDENTIFIER' or token.type == 'INPUT') and self.pos + 1 < len(self.tokens) and self.tokens[self.pos + 1].type == 'LPAREN':
            self.pos += 1
            return self.parse_call(token.value)
        return self.parse_expression()

    def parse_call(self, func_name: str) -> Node:
        self.consume('LPAREN')
        args = []
        while self.current_token() and self.current_token().type != 'RPAREN':
            if self.current_token().type in ['NUMBER', 'STRING', 'IDENTIFIER', 'LPAREN', 'LBRACKET']:
                args.append(self.parse_expression())
            elif self.current_token().type == 'INPUT':
                self.pos += 1
                if self.current_token() and self.current_token().type == 'LPAREN':
                    args.append(self.parse_call('input'))
                else:
                    raise SyntaxError("Expected LPAREN after INPUT")
            else:
                raise SyntaxError(f"Unexpected token in function call arguments: {self.current_token()}")
            if self.current_token() and self.current_token().type == 'COMMA':
                self.consume('COMMA')
        self.consume('RPAREN')
        return Node('Call', func_name, [Node('Args', None, args)])

    def parse_expression(self) -> Node:
        left = self.parse_term()

        # Handle indexing
        while self.current_token() and self.current_token().type == 'LBRACKET':
            left = self.parse_index(left.value if left.type == 'Identifier' else left)

        while self.current_token() and self.current_token().type in ['OPERATOR', 'COMPARISON']:
            op = self.consume(self.current_token().type).value
            right = self.parse_term()
            left = Node('BinaryOp', op, [left, right])
        return left

    def parse_term(self) -> Node:
        token = self.current_token()
        if token.type == 'NUMBER':
            self.pos += 1
            return Node('Number', int(token.value))
        elif token.type == 'STRING':
            self.pos += 1
            return Node('String', token.value[1:-1])
        elif token.type == 'IDENTIFIER':
            self.pos += 1
            return Node('Identifier', token.value)
        elif token.type == 'LPAREN':
            self.pos += 1
            expr = self.parse_expression()
            self.consume('RPAREN')
            return expr
        elif token.type == 'LBRACKET':
            self.pos += 1
            elements = []
            while self.current_token() and self.current_token().type != 'RBRACKET':
                elements.append(self.parse_expression())
                if self.current_token() and self.current_token().type == 'COMMA':
                    self.consume('COMMA')
            self.consume('RBRACKET')
            return Node('List', None, elements)
        raise SyntaxError(f"Unexpected token in expression: {token}")

class Interpreter:
    def __init__(self):
        self.variables: Dict[str, Any] = {}
        self.functions: Dict[str, Node] = {}
        self.builtins: Dict[str, callable] = {}
        self.builtins.update({
            'range': lambda start, end: list(range(start, end)),
            'tup': lambda lst: tuple(lst),
            'power': lambda base, exp: base ** exp,
            'fopen': lambda filename, mode: open(filename, mode),
            'store': lambda file, text: file.write(text) or None
        })

    def debug(self, *args):
        if 'debug' in self.builtins:
            self.builtins['debug'](*args)
        else:
            print("DEBUG:", *args)

    def interpret(self, ast: List[Node]):
        for node in ast:
            self.execute(node)

    def execute(self, node: Node):
        if node.type == 'Variable':
            self.variables[node.value] = self.evaluate(node.children[0])
        elif node.type == 'Function':
            self.functions[node.value] = node
        elif node.type == 'When':
            condition = self.evaluate(node.children[0])
            if condition:
                for stmt in node.children[1].children:
                    self.execute(stmt)
            elif node.children[2].children:
                for stmt in node.children[2].children:
                    self.execute(stmt)
        elif node.type == 'If':
            condition = self.evaluate(node.children[0])
            if condition:
                for stmt in node.children[1].children:
                    self.execute(stmt)
            else:
                executed = False
                for elsif_node in node.children[2].children:
                    if self.evaluate(elsif_node.children[0]):
                        for stmt in elsif_node.children[1].children:
                            self.execute(stmt)
                        executed = True
                        break
                if not executed and node.children[3].children:
                    for stmt in node.children[3].children:
                        self.execute(stmt)
        elif node.type == 'Repeat':
            for _ in range(node.value):
                for stmt in node.children[0].children:
                    self.execute(stmt)
        elif node.type == 'Foreach':
            var_name = node.value
            sequence = self.evaluate(node.children[0])
            body = node.children[1].children
            for item in sequence:
                self.variables[var_name] = item
                for stmt in body:
                    self.execute(stmt)
        elif node.type == 'For':
            var_name = node.value
            sequence = self.evaluate(node.children[0])
            body = node.children[1].children
            for item in sequence:
                self.variables[var_name] = item
                for stmt in body:
                    self.execute(stmt)
        elif node.type == 'Output':
            args = [self.evaluate(arg) for arg in node.children[0].children]
            if 'output' in self.builtins:
                self.builtins['output'](*args)
            else:
                print("Error: 'output' function not imported")
        elif node.type == 'Input':
            args = [self.evaluate(arg) for arg in node.children[0].children]
            if 'input' in self.builtins:
                result = self.builtins['input'](*args)
                return result
            else:
                print("Error: 'input' function not imported")
        elif node.type == 'Return':
            return self.evaluate(node.children[0])
        elif node.type == 'Import':
            if node.value == 'builtins':
                self.debug(f"Importing builtins, functions = {builtin_functions}")
                self.builtins.update(builtin_functions)
            else:
                print(f"Error: Module '{node.value}' not found")
        elif node.type == 'Call':
            args = [self.evaluate(arg) for arg in node.children[0].children]
            func_name = node.value
            if func_name in self.builtins:
                return self.builtins[func_name](*args)
            raise NameError(f"Function '{func_name}' not found")

    def evaluate(self, node: Node) -> Any:
        if node.type == 'Number':
            return node.value
        elif node.type == 'String':
            return node.value
        elif node.type == 'Identifier':
            return self.variables.get(node.value, 0)
        elif node.type == 'BinaryOp':
            left = self.evaluate(node.children[0])
            right = self.evaluate(node.children[1])
            if node.value == '+':
                return left + right
            elif node.value == '-':
                return left - right
            elif node.value == '*':
                return left * right
            elif node.value == '/':
                return left / right
            elif node.value == '>':
                return left > right
            elif node.value == '<':
                return left < right
            elif node.value == '=':
                return left == right
        elif node.type == 'List':
            return [self.evaluate(elem) for elem in node.children]
        elif node.type == 'Index':
            sequence = self.evaluate(node.children[0])
            index = self.evaluate(node.children[1])
            return sequence[index]
        elif node.type == 'Call':
            func_name = node.value
            args = [self.evaluate(arg) for arg in node.children[0].children]
            if func_name in self.builtins:
                return self.builtins[func_name](*args)
            raise NameError(f"Function '{func_name}' not found")
        return None

def run_quantumx_file(filename: str):
    if not filename.endswith('.qx'):
        raise ValueError("File must have .qx extension")
    with open(filename, 'r') as file:
        code = file.read()
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    interpreter = Interpreter()
    interpreter.interpret(ast)

def main():
    if len(sys.argv) != 2:
        print("Usage: quantumx <filename.qx>")
        sys.exit(1)
    run_quantumx_file(sys.argv[1])

if __name__ == "__main__":
    main()
