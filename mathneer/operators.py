import math
import operator
import numpy as np

class MathOperators:
    
    EPSILON = 1e-12
    constants = {
        "PI": math.pi,
        "E": math.e
    }

    operators = {
        "+": operator.add,
        "-": operator.sub,
        "*": operator.mul,
        "/": operator.truediv,
        "^": operator.pow,
        # "!": math.factorial
    }
    functions = {
        "abs": abs,
        "acos": math.acos,
        "asin": math.asin,
        "atan": math.atan,
        "cosh": math.cosh,
        "cos": math.cos,
        "exp": math.exp,
        "log": math.log,
        "log10": math.log10,
        "mean": np.mean,
        "round": round,
        "sgn": lambda a: abs(a) > EPSILON and cmp(a, 0) or 0,
        "sin": math.sin,
        "sinh": math.sinh,
        "sqrt": math.sqrt,
        "tan": math.tan,
        "tanh": math.tanh,
        "truncate": lambda a: int(a)
    }

    measure_prefix = {
        "c": 1/100,
        "m": 1/1000,
        "d": 1/10,
        "D": 10,
        "k": 1000,
        "M": 1e6,
        "G": 1e9,
        "T": 1e12
    }

    @staticmethod
    def convert_units(unit):
        unit = unit[1:-1]
        if len(unit)>2 and unit[0] in MathOperators.measure_prefix:
            return MathOperators.measure_prefix[unit[0]]
        return 1

    @staticmethod
    def valid_units(s,s1):
        return True
