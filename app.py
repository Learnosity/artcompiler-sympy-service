# Copyright (c) 2019, Art Compiler LLC

from pint import UnitRegistry
from sympy.physics.units import *
from sympy.vector import StdCoordSys3D, Vector, VectorZero, matrix_to_vector
from sympy.matrices import ImmutableMatrix, Matrix
from sympy.integrals import integrate, Integral, normalize_integral
from sympy.series.limits import limit, Limit
from sympy.concrete.summations import summation, Sum
from sympy.sets import *
from sympy.functions.elementary.hyperbolic import HyperbolicFunction
from sympy.functions import *
from sympy.simplify.fu import TR1, TR2, TR6, TR11, TR22
from sympy.simplify import logcombine, powsimp, powdenest, radsimp, trigsimp
from sympy.geometry.polygon import rad
from sympy.polys import factor, together, cancel
from sympy.core import *
from sympy.printing import latex

unit = UnitRegistry(autoconvert_offset_to_baseunit = True)
Q_ = unit.Quantity
R3 = StdCoordSys3D('R3')
VectorZero._latex_form = r'\mathbf{0}'

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
