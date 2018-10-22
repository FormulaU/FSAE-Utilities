class racetrack:
	def __init__(self):
		self.filepath = None
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

class sectioned_track(racetrack): 
	def __init__(self, pure_racetrack):
		self.filepath = pure_racetrack.filepath
		self.outer_path = pure_racetrack.outer_path
		self.inner_paths = pure_racetrack.inner_paths
		self.bound_paths = pure_racetrack.bound_paths
		#Sections (for our 'sectionized' part)
		self.sections = []
	
	def shortest_path_len_sq(self, weights):
		sq_len = 0
		prev = self.sections[0].map_scalar_pt(weights[0])
		for idx in range(1, len(self.sections)-1):
			cur = self.sections[idx].map_scalar_pt(weights[idx])
			sq_len += (cur[0]-prev[0])**2 + (cur[1]-prev[1])**2
			prev = cur
		#Finish up with the last element.
		cur = self.sections[0].map_scalar_pt(weights[0])
		sq_len += (cur[0]-prev[0])**2 + (cur[1]-prev[1])**2
		return sq_len

class section:
	# Start and end in the form of arrays of size 2, containing tuples with coordinates.
	# E.G: start=[(0,0),(0,1)], end=[(1,0),(1,1)]
	def __init__(self, start, end):
		self.start = start
		self.end = end
		self.shortest_pt = None
		self.MCP_pt = None
		# Vectorized version of start pts (for map_scalar_pt)
		self.s_vector = [(start[1][0] - start[0][0]),
				 (start[1][1] - start[0][1])]

	def map_scalar_pt(self, pt):
		return (self.s_vector[0] * pt + self.start[0][0], self.s_vector[1] * pt + self.start[0][1])
