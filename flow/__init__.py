"""
.. currentmodule:: flow
.. moduleauthor:: Christian Gram Kalhauge <christian@kalhauge.dk>

"""

import logging
L = logging.getLogger(__name__)

from sparse import parser, lexer

KEYWORDS = ('method', 'return')
TOKENS = (
        ('ID'        , r'[a-zA-Z_]+'),
        ('SKIP'      , r'[ \t]'),
        ('NEWLINE'   , r'\n'),
        ('END'       , r';'),
        ('L_PAR'    , r'\('),
        ('R_PAR'    , r'\)'),
        ('L_CUR'    , r'\{'),
        ('R_CUR'    , r'\}'),
        )
GRAMMA = {
        'PROGRAM' : (
            (list, 'METHOD+'),
            ),
        'METHOD'  : (
            (ast.Method,      'method ID ( ARGS ) STATEMENTS return ID'),
            ),
        'ARGS'    : (
            (lambda a, args: list([a] + args), 'ARG ARGX*'),
            ),
        'ARGX'    : (
            (parser.reflex,   ', ARG'),
            ),
        'ARG'     : (
            (ast.Argument,    'ID : SET')
            ),
        'STATEMENTS' : (
            (list, 'STATEMENT+'),
            ),
        'STATEMENT' : (
            (ast.Statement, 'ID = FUNCTION_CALL'),
            ),
        'FUNCTION_CALL' : (
            (ast.FunctionCall, 'ID ( F_ARGS ) '),
            ),
        'F_ARGS'    : (
            (lambda a, args: list([a] + args), 'ARG ARGX*'),
            ),
        'F_ARGX'    : (
            (parser.reflex,   ', ARG'),
            ),
        'F_ARG'    : (
            (parser.reflex,   'FUNCTION_CALL'),
            (ast.FuncArg,   'ID'),
            ),
    }


def parse(program_str):
    """
    Parses a flow program
    """
    tokens = lexer.tokenize(program_str, TOKENS, KEYWORDS)
    return parser.parse('PROGRAM', tokens, GRAMMA)


