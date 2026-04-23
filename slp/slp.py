from enum import Enum
import re
from typing import Optional

from syntax_tree import *


class TokenType(Enum):
    ID = re.compile("[_a-zA-Z][_a-zA-Z0-9]*")
    DIGITS = re.compile("[0-9]+")
    ASSIGN = re.compile(":=")
    L_PAREN = re.compile(r"\(")
    R_PAREN = re.compile(r"\)")
    COMMA = re.compile(",")
    SEMICOLON = re.compile(";")
    PLUS = re.compile(r"\+")
    MINUS = re.compile(r"-")
    MULT = re.compile(r"\*")
    DIV = re.compile(r"/")
    WHITESPACE = re.compile(r"\s*")

def get_tokens(slp_str: str) -> list[tuple[TokenType, str]]:
    """Tokenize the input string into a list of (type,value) tuples;

        Args:
            slp_str (str): The input string to tokenize.
        Returns:
            A list of (TokenType, str) tuples. Str will be None except for ID and DIGIT types.
    """
    i = 0
    tokens = []
    while i < len(slp_str):
        for e in TokenType:
            if m := e.value.match(slp_str, i):
                start, end = m.span()
                if e != TokenType.WHITESPACE:
                    if e in {TokenType.ID, TokenType.DIGITS}:
                        token_value = slp_str[start:end]
                    else:
                        token_value = None
                    tokens.append((e, token_value))
                i += end - start
                break
    return tokens


class Parser:
    def __init__(self):
        self._tokens = None
        self._pos = 0
        self._marked_pos = 0

    def parse(self, slp_str: str):
        self._tokens = get_tokens(slp_str)
        self._pos = 0
        self._marked_pos = 0
        return self._stmt()

    def _peek(self, look_ahead=0) -> Optional[TokenType]:
        if self._pos + look_ahead >= len(self._tokens):
            # No tokens left to read
            return None
        return self._tokens[self._pos + look_ahead]

    def _stmt(self) -> Optional[Stmt]:
        stmt =  self._assign_stmt() or self._print_stmt()
        if stmt:
            if self._peek(0):
                next_type, _ = self._peek(0)
                if next_type == TokenType.SEMICOLON:
                    return self._compound_stmt_rest(stmt)
            return stmt
        return None


    def _exp(self) -> Optional[Exp]:
        return self._num()  or self._id()


    def _compound_stmt_rest(self, stmt1) -> Optional[CompoundStmt]:
        pos = self._pos
        next_type, _ = self._peek(0)
        if next_type == TokenType.SEMICOLON:
            self._pos += 1
            stmt2 = self._stmt()
            if stmt1 and stmt2:
                return CompoundStmt(stmt1=stmt1, stmt2=stmt2)
        self._pos = pos
        return None

    def _assign_stmt(self) -> Optional[AssignStmt]:
        pos = self._pos

        identifier = self._id()
        next_type, _ = self._peek(0)
        if identifier and next_type == TokenType.ASSIGN:
            self._pos += 1
            exp = self._exp()
            if exp:
                return AssignStmt(identifier, exp)
        self._pos = pos
        return None

    def _print_stmt(self) -> Optional[PrintStmt]:
        pos = self._pos
        if self._peek(0) == (TokenType.ID, "print") and self._peek(1) == (TokenType.L_PAREN, None):
            self._pos += 2
            exp_list = self._exp_list()
            if exp_list and self._peek(0) == (TokenType.R_PAREN, None):
                self._pos += 1
                return PrintStmt(exp_list)
        self._pos = pos
        return None

    def _num(self) -> Optional[Num]:
        next_token = self._peek()
        if not next_token:
            return None

        token_type, value = next_token
        if token_type == TokenType.DIGITS:
            self._pos += 1
            return Num(int(value))
        else:
            return None

    def _id(self) -> Optional[Id]:
        next_type, next_value = self._peek(0)

        if next_type == TokenType.ID:
            self._pos +=1
            return Id(next_value)
        return None

    def _exp_list(self) -> Optional[list[Exp]]:
        pos = self._pos
        exp = self._exp()
        if not exp:
            self._pos = pos
            return None
        result = [exp]
        while next_token := self._peek(0) == (TokenType.COMMA, None):
            self._pos += 1
            exp = self._exp()
            if not exp:
                self._pos = pos
                return None
            result.append(exp)
        return result




def eval(slp_str: str):
    parser = Parser()
    stmt = parser.parse(slp_str)
    locals = {}
    eval_stmt(stmt, locals)

def eval_stmt(stmt: Stmt, locals: dict[str, int]):
    match stmt:
        case AssignStmt(identifier=ident, value=exp):
            locals[ident.identifier] = eval_exp(exp, locals)
        case PrintStmt(expr_list=expr_list):
            strings = [str(eval_exp(exp, locals)) for exp in expr_list]
            output = " ".join(strings)
            print(output)
        case CompoundStmt(stmt1=s1, stmt2=s2):
            eval_stmt(s1, locals)
            eval_stmt(s2, locals)



def eval_exp(exp: Exp, locals: dict[str, int]) -> int:
    match exp:
        case Num(value=value):
            return value
        case Id(identifier=ident):
            return locals[ident]
        case _:
            raise Exception("Unknown expression {}", exp)

if __name__ == "__main__":
    while (command := input("--> ")).lower() != "q":
        eval(command)