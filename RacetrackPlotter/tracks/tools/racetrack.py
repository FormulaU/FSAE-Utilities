class racetrack:
	def __init__(self):
		self.outer_path = None
		self.inner_paths = []
		self.bound_paths = []
class path_t:
	def __init__(self):
		self.t = []
		self.x = []
		self.y = []
		self.len = None
		self.x_cs = None
		self.y_cs = None

class binding_paths:
	def __init__(self):
		self.inner = None
		self.outer = None
		self.inner_t = []
		self.outer_t = []
