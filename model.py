import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from variable import Variable

class Model:
	
	def __init__(self):
		self.var_names = set()
		self.vars = {}
		self.init_vars = {}
		self.dtvars = {}

	def new_var(self, name):
		if name in self.vars:
			raise Exception("variable {} already created".format(name))	
		else:
			self.var_names.add(name)
			variable = Variable(name)
			self.vars[variable] = None
			return variable

	def set_value(self, variable, value):
		self.init_vars[variable] = value

	def add_dt(self, variable, expr):
		if variable in self.dtvars:
			raise Exception("d/dt already prvodied for variable")
		else:
			self.dtvars[variable] = expr

	def run_steps(self):
		self.vars = self.init_vars.copy()
		while True:
			yield {var.name: v for var, v in self.vars.items()}
			new = self.vars.copy()
			for var in self.dtvars:
				new[var] += self.dtvars[var].evaluate(self)
			self.vars = new 

	def plot_curves(self, graph_axes, steps, vars):
		serieses = {v : [] for v in vars}
		times = []
		for t, m in zip(range(steps), self.run_steps()):
			times.append(t)	
			for v in vars:
				serieses[v].append(m[v.name])

		plt.axes(graph_axes)
		for v in serieses:
			plt.plot(times, serieses[v], label=v.name)
		plt.legend()

	def update_and_replot(self, fig, graph_axes, steps, vars, var, value):
		plt.axes(graph_axes)
		plt.cla()
		self.init_vars[var] = value
		self.plot_curves(graph_axes, steps, vars)
		fig.canvas.draw_idle()	

	def plot(self, steps, vars, nobs):
		fig = plt.figure(figsize=(8, 3))

		# create axes for graph
		curr_bottom = 0.2
		graph_axes = plt.axes([0.1, curr_bottom, 0.8, (1-curr_bottom-0.1)])
		curr_bottom -= 0.05
		margin = curr_bottom/(len(nobs)+1)
		height = 0.5*margin
		axes = {}
		for v in nobs:
			curr_bottom -= margin
			axes[v] = plt.axes([0.1, curr_bottom, 0.8, height])

		self.plot_curves(graph_axes, steps, vars)

		sliders = []
		for v in nobs:
			print(v.name)
			slider = Slider(ax=axes[v], label=v.name, valmin=v.min, valmax=v.max, valinit = self.init_vars[v])
			print(slider)
			def update(a, fig=fig, graph_axes=graph_axes, steps=steps, vars=vars, v=v):
				self.update_and_replot(fig, graph_axes, steps, vars, v, a)
			slider.on_changed(update)
			sliders.append(slider)

		plt.show()
		return sliders

def SIR_model():
	m = Model()
	s = m.new_var("S")
	i = m.new_var("I")
	r = m.new_var("R")
	b = m.new_var("B")
	b.max = 5
	b.min = 0
	g = m.new_var("G")
	g.max = 10
	g.min = 0
	n = m.new_var("N")
	
	m.add_dt(s, -(b*s*i)/n)
	m.add_dt(i, (b*s*i)/n - g*i)
	m.add_dt(r, g*i)
	
	m.set_value(s, 999)
	m.set_value(i, 1)
	m.set_value(r, 0)
	m.set_value(b, 0.25)
	m.set_value(g, 0.125)
	m.set_value(n, 1000)
	
	return m.plot(1000, [s, i, r], [b, g])

def Lotka_Volterra_model():
	m = Model()

	x = m.new_var("# of rabbits")
	y = m.new_var("# of foxes")
	a = m.new_var("rabbit growth rate")
	a.min = 0
	a.max = 2
	b = m.new_var("rabbit predation rate per wolf")
	b.min = 0
	b.max = 2
	c = m.new_var("fox death rate")
	c.min = 0
	c.max = 2
	d = m.new_var("fox growth rate per rabbit")
	d.min = 0
	d.max = 2

	m.add_dt(x, a*x-b*x*y)	
	m.add_dt(y, -c*y+d*x*y)	

	m.set_value(x, 0.9)
	m.set_value(y, 1.0)
	m.set_value(a, 2.0/3)
	m.set_value(b, 4.0/3)
	m.set_value(c, 1.0)
	m.set_value(d, 1.0)

	return m.plot(10, [x, y], [a, b, c, d])

r = Lotka_Volterra_model()
	
