import unittest
from slp.slp import *


class TestSlp(unittest.TestCase):
    def test_tokenize_big_stmt(self):
        big_stmt = "a := 5 + 3 ; b := (print(a, a-1), 10 * a) ; print(b)"
        tokens = get_tokens(big_stmt)        
        expected = [('ID', None), ('ASSIGN', None), ('DIGIT', None), ('PLUS', None), ('DIGIT', None), 
                    ('SEMICOLON', None), ('ID', None), ('ASSIGN', None), ('L_PAREN', None), ('ID', None),
                    ('L_PAREN', None), ('ID', None), ('COMMA', None), ('ID', None), ('MINUS', None), ('DIGIT', None),
                    ('R_PAREN', None), ('COMMA', None), ('DIGIT', None), ('DIGIT', None), ('MULT', None), ('ID', None),
                    ('R_PAREN', None), ('SEMICOLON', None), ('ID', None), ('L_PAREN', None), ('ID', None),
                    ('R_PAREN', None)]
        self.assertEqual(tokens, expected)