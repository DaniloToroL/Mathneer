from pyparsing import *
import math
import operator

__source__ = "https://stackoverflow.com/questions/2371436/evaluating-a-mathematical-expression-in-a-string"
__note__ = "Edit for Danilo Toro Labra"
class MathParser:
    """
    exp_operator   :: '^'
    mult_operator  :: '*' | '/'
    add_operator   :: '+' | '-'
    integer :: ['+' | '-'] '0'..'9'+
    atom    :: PI | E | real | fn '(' expr ')' | '(' expr ')'
    factor  :: atom [ expop factor ]*
    term    :: factor [ multop factor ]*
    expr    :: term [ addop term ]*
    """
    def __init__(self):
        
        point = Literal(".")
        e = CaselessLiteral("E")
        pi = CaselessLiteral("PI")
        
        plus = Literal("+")
        minus = Literal("-")
        mult = Literal("*")
        div = Literal("/")
        fact = Literal("!")
        lpar = Literal("(").suppress()
        rpar = Literal(")").suppress()

        sign_operator = oneOf("+ -")
        add_operator = plus | minus
        mult_operator = mult | div
        exp_operator = Literal("^")

        fnumber = Combine(Word("+-" + nums, nums) + 
                    Optional(point + Optional(Word(nums))) + 
                    Optional(e + Word("+-" + nums, nums)))
        
        self.expresion_stack = []

    
        ident = Word(alphas, alphas + nums + "_$")
        expresion = Forward()
        atom = ((Optional(sign_operator) +
                 (ident + lpar + expresion + rpar | pi | e | fnumber).setParseAction(self.pushFirst))
                | Optional(sign_operator) + Group(lpar + expresion + rpar)
                ).setParseAction(self.pushUMinus)

        factor = Forward()
        factor << atom + ZeroOrMore((exp_operator + factor).setParseAction(self.pushFirst))
        term = factor + ZeroOrMore((mult_operator + factor).setParseAction(self.pushFirst))
        expresion << term + ZeroOrMore((add_operator + term).setParseAction(self.pushFirst))

        self.bnf = expresion

    def pushFirst(self, strg, loc, toks):
        self.expresion_stack.append(toks[0])

    def pushUMinus(self, strg, loc, toks):
        if toks and toks[0] == '-':
            self.expresion_stack.append('unary -')

    def eval(self, num_string, parseAll=True):
        self.expresion_stack = []
        results = self.bnf.parseString(num_string, parseAll)
        value = self.evaluateStack(self.expresion_stack)
        return value

    def evaluateStack(self, string):
        operation = string.pop()
        if operation == "unary -":
            return -self.evaluateStack(string)
        if operation in MathOperators.operators:
            operation_2 = self.evaluateStack(string)
            operation_1 = self.evaluateStack(string)
            return MathOperators.operators[operation](operation_1, operation_2)
        if operation in MathOperators.constants:
            return MathOperators.constants[operation]
        if operation in MathOperators.functions:
            return MathOperators.functions[operation](self.evaluateStack(string))
        if operation[0].isalpha():
            return 0
        return float(operation)


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
        "^": operator.pow
    }
    functions = {
        "sin": math.sin,
        "cos": math.cos,
        "tan": math.tan,
        "exp": math.exp,
        "abs": abs,
        "trunc": lambda a: int(a),
        "round": round,
        "sgn": lambda a: abs(a) > EPSILON and cmp(a, 0) or 0
    }
        

if __name__ == "__main__":
    nsp = MathParser()
    result = nsp.eval('sin(90*pi/180)')
    print(result)
    # 16.0
    
    
    result = nsp.eval('exp(2^4)')
    print(result)
    # 8886110.520507872
