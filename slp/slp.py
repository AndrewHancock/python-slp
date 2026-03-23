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

    def _stmt(self) -> Stmt:
        return self._assign_stmt() or self._print_stmt()


    def _exp(self) -> Exp:
        return self._num_exp() or self._exp_list()

    def _assign_stmt(self) -> Optional[AssignStmt]:
        # If there are less than 3 tokens less, we can't parse an AssignStmt
        if len(self._tokens) - self._pos < 3:
            return None

        pos = self._pos

        current_type, current_val = self._peek()
        next_type, _ = self._peek(1)

        if current_type == TokenType.ID and next_type == TokenType.ASSIGN:
            identifier = current_val
            self._pos += 2
            exp = self._exp()

            if exp:
                return AssignStmt(identifier, exp)
        self._pos = pos
        return None

    def _print_stmt(self) -> None:
        pos = self._pos
        if self._peek(0) == (TokenType.ID, "print") and self._peek(1) == (TokenType.L_PAREN, None):
            self._pos += 2
            exp_list = self._exp_list()
            if exp_list and self._peek(0) == (TokenType.R_PAREN, None):
                self._pos += 1
                return PrintStmt(exp_list)
        self._pos = pos
        return None

    def _num_exp(self) -> Optional[NumExp]:
        next_token = self._peek()
        if not next_token:
            return None

        token_type, value = next_token
        if token_type == TokenType.DIGITS:
            self._pos += 1
            return NumExp(int(value))
        else:
            return None

    def _exp_list(self) -> Optional[ExpList]:
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
        return ExpList(result)


