import unittest
from slp.slp import get_tokens, Parser, TokenType
from syntax_tree import PrintStmt, Num, AssignStmt, Id


class TestSlp(unittest.TestCase):
    def test_tokenize_big_stmt(self):
        big_stmt = "a := 5 + 3 ; b := (print(a, a-1), 10 * a) ; print(b)"
        tokens = get_tokens(big_stmt)        
        expected = [
            (TokenType.ID, "a"),
            (TokenType.ASSIGN, None),
            (TokenType.DIGITS, "5"),
            (TokenType.PLUS, None),
            (TokenType.DIGITS, "3"),
            (TokenType.SEMICOLON, None),
            (TokenType.ID, "b"),
            (TokenType.ASSIGN, None),
            (TokenType.L_PAREN, None),
            (TokenType.ID, "print"),
            (TokenType.L_PAREN, None),
            (TokenType.ID, "a"),
            (TokenType.COMMA, None),
            (TokenType.ID, "a"),
            (TokenType.MINUS, None),
            (TokenType.DIGITS, "1"),
            (TokenType.R_PAREN, None),
            (TokenType.COMMA, None),
            (TokenType.DIGITS, "10"),
            (TokenType.MULT, None),
            (TokenType.ID, "a"),
            (TokenType.R_PAREN, None),
            (TokenType.SEMICOLON, None),
            (TokenType.ID, "print"),
            (TokenType.L_PAREN, None),
            (TokenType.ID, "b"),
            (TokenType.R_PAREN, None)
        ]
        self.assertEqual(tokens, expected)


    def test_parse_simple_assignment(self):
        stmt = "i := 5"
        p = Parser()
        actual = p.parse(stmt)
        expected = AssignStmt(identifier=Id('i'), value=Num(5))
        self.assertEqual(actual, expected)

    def test_parse_print(self):
        stmt = "print(1, 2, 3, 4)"
        p = Parser()
        actual = p.parse(stmt)
        expected = PrintStmt(expr_list=[Num(value=1), Num(value=2), Num(value=3), Num(value=4)])
        self.assertEqual(actual, expected)

