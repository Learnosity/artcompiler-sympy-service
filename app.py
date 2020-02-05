# Copyright (c) 2019, Art Compiler LLC

from sympy import latex
from sympy import sympify

FUNC_WHITELIST = [
    'eval',
    'latex',
    'literal',
]


def eval_math(obj):
    if 'func' not in obj:
        raise ValueError('must provide func')
    func = obj['func']
    if func not in FUNC_WHITELIST:
        raise ValueError('func must be eval, latex, or literal')

    if 'expr' not in obj:
        raise ValueError('must provide expr')
    expr = obj['expr']

    if func == 'eval':
        kwargs = {'ln_notation': 'True', 'inv_trig_style': 'power'}
        return latex(eval(expr), **kwargs)
    elif func == 'latex':
        return latex(sympify(expr, evaluate=False))
    elif func == 'literal':
        return expr
    return 'error'
