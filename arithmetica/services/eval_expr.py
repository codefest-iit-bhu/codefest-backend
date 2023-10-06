import sympy as sp
import re
from sympy.parsing.latex import parse_latex
class ExpressionEvaluator:
    @staticmethod
    def evaluate_latex(latex_expr, x_val):
        e = sp.symbols('e')
        x = sp.symbols('x')
        expr = sp.sympify(parse_latex(latex_expr))
        result = expr.subs(x, x_val)

        return result.evalf(subs={e: 2.71828})

    @staticmethod
    def remove_format_keywords(latex_str):
        keywords = [r'\\left', r'\\right', r'\\big', r'\\Big', r'\\bigg', r'\\Bigg']

        for keyword in keywords:
            latex_str = re.sub(keyword, '', latex_str)

        return latex_str