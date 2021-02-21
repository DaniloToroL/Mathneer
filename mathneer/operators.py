import math
import operator
import numpy as np

class MathOperators:

    def __init__(self):
        
        self.EPSILON = 1e-12
        self.constants = {
            "PI": math.pi,
            "E": math.e
        }

        self.operators = {
            "+": operator.add,
            "-": operator.sub,
            "*": operator.mul,
            "/": operator.truediv,
            "^": operator.pow,
            # "!": math.factorial
        }
        self.functions = {
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

        self.measure_prefix = {
            "p": 1e-12,
            "m": 1e-3,
            "c": 1e-2,
            "d": 1e-1,
            "k": 1e3,
            "M": 1e6,
            "G": 1e9,
            "T": 1e12
        }

    def __get_unit(self,unit):
        return unit[1:-1]

    
    def convert_units(self, unit):
        unit = self.__get_unit(unit)
        if len(unit)>2 and unit[0] in self.measure_prefix:
            return self.measure_prefix[unit[0]]
        return 1

    
    def valid_units(self,s,s1):
        return True
