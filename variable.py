import operator
import math

log_op = lambda x: math.log(x)
exp_op = lambda x: math.exp(x)

def show_operator(op):
	if op == operator.add: return "+"
	if op == operator.mul: return "*"
	if op == operator.sub: return "-"
	if op == operator.neg: return "-"
	if op == operator.truediv: return "/"
	if op == operator.pow: return "^"
	if op == log_op: return "log"
	if op == exp_op: return "exp"
	raise Exception("unknown op {}".format(op))

class Expr:

	def __init__(self):
		pass

	def evaluate(self, model):
		pass

	def __radd__(self, other):
		if type(other) == int:
			other = Real(other)
		return self+other

	def __add__(self, other):
		return Binop(self, operator.add, other)

	def __rmul__(self, other):
		if type(other) == int:
			other = Real(other)
		return self*other

	def __mul__(self, other):
		if type(other) == int:
			other = Real(other)
		return Binop(self, operator.mul, other)

	def __sub__(self, other):
		if type(other) == int:
			other = Real(other)
		return Binop(self, operator.sub, other)

	def __truediv__(self, other):
		if type(other) == int:
			other = Real(other)
		return Binop(self, operator.truediv, other)

	def __neg__(self):
		return Uniop(operator.neg, self)

	def __pow__(self, other):
		return Binop(self, operator.pow, other)

class Real(Expr):

	def __init__(self, value):
		self.value = value 
		self.max = 0
		self.min = 1 

	def evaluate(self, model):
		return self.value
	
	def show(self):
		return self.value


class Variable(Expr):

	def __init__(self, name):
		self.name = name 
		self.max = 0
		self.min = 1 

	def evaluate(self, model):
		return model.vars[self]
	
	def show(self):
		return(self.name)

class Uniop(Expr):

	def __init__(self, operator, v):
		self.operator = operator
		self.v = v if type(v) != int else Real(v)

	def evaluate(self, model):
		return self.operator(self.v.evaluate(model))

	def show(self):
		return("{}({})".format(show_operator(self.operator), self.v.show()))

log = lambda v: Uniop(log_op, v)
exp = lambda v: Uniop(exp_op, v)

class Binop(Expr):

	def __init__(self, left, operator, right):
		self.left = left if type(left) != int else Real(left)
		self.operator = operator
		self.right = right if type(right) != int else Real(right)

	def evaluate(self, model):
		return self.operator(self.left.evaluate(model), self.right.evaluate(model))

	def show(self):
		return("({} {} {})".format(self.left.show(), show_operator(self.operator), self.right.show()))

