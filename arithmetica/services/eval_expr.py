import sympy as sp
import re
import math
from sympy.parsing.latex import parse_latex
from sympy.parsing.sympy_parser import parse_expr
from rest_framework.exceptions import ParseError


class ExpressionEvaluator:
    def evaluate_latex(self,latex_expr, x_val):
        CONSTANTS = {
            'e': math.e,
            'pi': math.pi,
        }

        FUNCTIONS = {
            'sin': math.sin,
            'cos': math.cos,
            'tan': math.tan,
            'exp': math.exp,
            'sqrt': math.sqrt,
            'ln': math.log,
            'log': lambda x, b=10: math.log(x, b),
            'abs': abs,
        }

        try:
            expr = self.get_parsed_expr(latex_expr)
        except Exception as e:
            raise ParseError('Malformed Expression')

        try:
            symbolsUsed = [str(i) for i in expr.atoms(sp.Symbol)]
            assert symbolsUsed in [[], ['x']], 'x is not the only variable'
            functionsUsed = set([str(i.func) for i in expr.atoms(sp.Function)])
            unknownFunctionsUsed = functionsUsed - set(FUNCTIONS.keys())
            assert len(unknownFunctionsUsed) == 0, f'disallowed functions detected: {[*unknownFunctionsUsed]}'
        except AssertionError as e:
            raise ParseError(str(e))

        try:
            return float(
                parse_expr(str(expr), local_dict={**CONSTANTS, **FUNCTIONS, "x": x_val}, transformations='all',
                           evaluate=True)
            )
        except Exception as e:
            return ParseError('Malformed Expression')

    @staticmethod
    def remove_format_keywords(latex_str):
        keywords = [r'\\ ']

        for keyword in keywords:
            latex_str = re.sub(keyword, '', latex_str)

        return latex_str

    def get_parsed_expr(self,latex_expr):
        CONSTANTS = {
            'e': math.e,
            'pi': math.pi,
        }

        expr = parse_expr(str(parse_latex(latex_expr)), local_dict=CONSTANTS, transformations='all')
        return expr
