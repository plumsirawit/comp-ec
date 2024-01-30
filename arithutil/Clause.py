class Atom:
    def __init__(self, name):
        self.name = name

class Term:
    def __init__(self, op, args):
        self.op = op
        self.args = args

    def __add__(self, other):
        return Term('ADD', (self, other))
    
    def __sub__(self, other):
        return Term('SUB', (self, other))
    
    def __mul__(self, other):
        return Term('MUL', (self, other))
    
    def __truediv__(self, other):
        return Term('DIV', (self, other))