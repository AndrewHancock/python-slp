from enum import Enum
import re

class TokenType(Enum):
    ID = re.compile("[_a-zA-Z][_a-zA-Z0-9]*")
    DIGITS = re.compile("[0-9]")
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
                    if e.name in {TokenType.ID, TokenType.DIGITS}:
                        token_value = slp_str[start:end]
                    else:
                        token_value = None
                    tokens.append((e.name, token_value))
                i += end - start
                break
    return tokens



