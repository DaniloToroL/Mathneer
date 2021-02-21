from pyparsing import *
from operators import MathOperators

__source__ = "https://stackoverflow.com/questions/2371436/evaluating-a-mathematical-expression-in-a-string"
__note__ = "Edit for Danilo Toro Labra"

class Parser:
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

        self.math_operators = MathOperators()

        self.integer = Word(nums)
        
        self.point = Literal(".")
        self.e = CaselessLiteral("E")
        self.pi = CaselessLiteral("PI")
        
        self.plus = Literal("+")
        self.minus = Literal("-")
        self.mult = Literal("*")
        self.div = Literal("/")
        self.fact = Literal("!")

        self.sign_operator = oneOf(["+","-"])
        self.add_operator = self.plus | self.minus
        self.mult_operator = self.mult | self.div
        self.exp_operator = Literal("^")
        self.equal_operator = Literal("=")

        self.unit = Combine(Literal("[") + OneOrMore(Word(alphanums)) + Literal("]"))

        self.list = Combine(Literal("[") + ZeroOrMore(Word(alphanums) + Optional(Literal(","))) + Literal("]"))
        self.set = Combine(Literal("{") + ZeroOrMore(Word(alphanums) + Optional(Literal(","))) + Literal("}"))


class MathParser(Parser):
    
    def __init__(self):

        super().__init__()

        lpar = Literal("(").suppress()
        rpar = Literal(")").suppress()

        fnumber = Combine(Word("+-" + nums, nums) + 
                    Optional(self.point + Optional(self.integer)) + 
                    Optional(self.e + Word("+-" + nums, nums)) +   
                    Optional(self.unit))
        
        self.expresion_stack = []

    
        ident = Combine(Word(alphas, alphas + nums + "_$") + Optional(self.unit))
        expresion = Forward()
        atom = ((Optional(self.sign_operator) +
                 (ident + lpar + expresion + rpar | self.pi | self.e | fnumber).setParseAction(self.pushFirst))
                | Optional(self.sign_operator) + Group(lpar + expresion + rpar)
                ).setParseAction(self.pushUMinus)

        factor = Forward()
        factor << atom + ZeroOrMore((self.exp_operator + factor).setParseAction(self.pushFirst))
        term = factor + ZeroOrMore((self.mult_operator + factor).setParseAction(self.pushFirst))
        expresion << term + ZeroOrMore((self.add_operator + term).setParseAction(self.pushFirst))

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

    def evaluateStack(self, string, algebra=False):
        
        operation = string.pop()
        if operation == "unary -":
            return str(-self.evaluateStack(string))
        if operation in self.math_operators.operators:
            operation_2 = self.evaluateStack(string)
            operation_1 = self.evaluateStack(string)
            if self.math_operators.valid_units(operation_1, operation_2): 
                return self.math_operators.operators[operation](operation_1, operation_2)
            raise Exception("Units are not supported")

        if operation in self.math_operators.constants:
            return self.math_operators.constants[operation]

        if operation in self.math_operators.functions:
            return self.math_operators.functions[operation](self.evaluateStack(string))

        if list(self.unit.scanString(operation)):
            position = list(self.unit.scanString(operation))[0][1]
            unit = list(self.unit.scanString(operation))[0][0][0]
            multiple = self.math_operators.convert_units(unit)
            return float(operation[:position])* multiple
        if operation[0].isalpha():
            return 0
        return float(operation)


class AlgebraParser(MathParser):
    def __init__(self):
        super().__init__()

        ident = Word(alphas, alphanums)
        real = Regex(r'\d+\.\d*')
        arith_expresion = self.bnf
        arith_operand = Forward()
        
        expresion = (arith_expresion | real | self.integer | ident) + self.exp_operator + self.integer
        expresion.setParseAction( lambda tokens: f'pow({tokens[0]},{tokens[2]})')
        arith_operand <<= self.exp_operator | real | self.integer | ident | arith_expresion

        self.alf = arith_operand

    def eval(self, num_string, parseAll=True):
        return self.alf.parseString(num_string, parseAll)

        

if __name__ == "__main__":
    nsp = MathParser()
    result = nsp.eval('1[m] + 1000[mm]')
    print(result)
    # 1001.0

    result = nsp.eval('sin(90*PI/180)')
    print(result)
    # 1.0

    result = nsp.eval('10*5*20')
    print(result)
    # 1000.0


