import operator
from variable import *

def derivative(variable, expr):
	if isinstance(expr, Real):
		return 0
	if isinstance(expr, Variable):
		if expr == variable:
			return 1
		else:
			return 0
	if isinstance(expr, Binop): 
		f = expr.left
		fp = derivative(variable, f)
		g = expr.right	
		gp = derivative(variable, g)
		if expr.operator == operator.add:
			return fp + gp
		if expr.operator == operator.mul:
			return f*gp + g*fp
		if expr.operator == operator.sub:
			return fp-gp
		if expr.operator == operator.pow:
			return (f**g)*(fp*g/f + gp*log(f))
	if isinstance(expr, Uniop):
		if expr.operator == operator.neg:
			return -derivative(variable, expr.v)

x = Variable("x")
cube = x**3
dcube = derivative(x, cube)
print(cube.show(), ">>", dcube.show())
