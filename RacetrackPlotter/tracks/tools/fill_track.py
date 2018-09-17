from scipy import misc
import imageio
import numpy
import os

track_thresh = 300
border = 5
base_path = '../images/gen/hollow_tracks/' 
inner_color = 128

def main():	
	for filename in os.listdir(base_path):
		fill_track(base_path, filename)

def fill_track(path, name):
	print(path+name)
	f = imageio.imread(path+name, pilmode='L')
	#Find border paths, find whitespace. Inside of track is whitespace that touches every border path.
	fill_obj = track_fill(f)
	fill_obj.save('../images/gen/filled_tracks/'+name)
	
class track_fill:
	WHITE = 255
	BLACK = 0
	def __init__(self, image):
		self.image = image
		#initialize our sets
		self.all_pixels = set()
		self.fills = []
		
		#Iterate through all the pixels. If we haven't flood filled it, grab it.
		for row in range(len(image)):
			for col in range(len(image[0])):
				pixel = (row,col)
				if pixel not in self.all_pixels:
					self.add_fill(pixel)

		#Find the only whitespace fill with more than one neighbor. That's the inside of the track. 
		for fill in self.fills:
			pixel = fill.pixels.pop()
			fill.add(pixel)
#			print(pixel)
			print("Color: " + str(self.image[pixel[0]][pixel[1]]))
			print("Fill Size: " + str(len(fill.pixels)))
			print("Neighbors: " + str(fill.count_neighbors()))
			if self.image[pixel[0]][pixel[1]] == self.WHITE:
				if fill.count_neighbors() > 1:
					print("Fond inside of track. Filling.")
					self.fill_area(fill, inner_color)
					break
	
	def save(self, name):
		#Save
		imageio.imsave(name, self.image)

	def add_fill(self, pixel):
		#Add a new fill
		self.fills += [fill()]
		#Call our flood fill algorithm.
		self.flood_fill(pixel, self.image[pixel[0]][pixel[1]])

	def flood_fill(self, pixel, color):
		neighbors = set()
		neighbors.add(pixel)
		while len(neighbors) > 0:
			pixel = neighbors.pop()

			#Add the pixel to our set of pixels, and the global set of pixels.
			self.fills[-1].add(pixel)
			self.all_pixels.add(pixel)

			#Call add our neighbors
			n_neigh = self.get_neighbors(pixel)
			for n in n_neigh:
				if n not in self.fills[-1].pixels:
					#Check the color of the new pixel. Try to add the neighbor if they arent' already one.
					if self.image[n[0]][n[1]] != color:
						if n in self.all_pixels and not self.fills[-1].in_neighbors(n):
							self.fills[-1].add_neighbor(self.find_fill(n))
					else:
						neighbors.add(n)

	def is_border_pixel(self, pixel):
		n_neigh = get_neighbors(pixel)
		for n in n_neigh:
			#If we have a neighbor that's white, we're on the border.
			if self.image[n[0]][n[1]] == 255:
				return True
		return False
	def find_fill(self, pixel):
		for fill in self.fills:
			if pixel in fill.pixels:
				return fill

	def get_neighbors(self, pixel):
		neighbors = []
		neighbors += [(pixel[0]-1, pixel[1]+1)]
		neighbors += [(pixel[0]-1, pixel[1])]
		neighbors += [(pixel[0]-1, pixel[1]-1)]
		neighbors += [(pixel[0], pixel[1]-1)]
		neighbors += [(pixel[0]+1, pixel[1]-1)]
		neighbors += [(pixel[0]+1, pixel[1])]
		neighbors += [(pixel[0]+1, pixel[1]+1)]
		neighbors += [(pixel[0], pixel[1]+1)]
		
		#Clamp neighbors to the bounds of the image
		ret = []
		for n in neighbors:
			if 0 <= n[0] < len(self.image) and 0 <= n[1] < len(self.image[0]):
				ret += [n]
		return ret
	
	def fill_area(self, fill, color):
		for n in fill.pixels:
			self.image[n[0]][n[1]] = color

class fill:
	def __init__(self):
		self.pixels = set()
		self.neighbors = set()
		self.neighbor_pixels = set()
	
	def add(self, pixel):
		self.pixels.add(pixel)
	
	def add_neighbor(self, neighbor):
		self.neighbors.add(neighbor)
		self.neighbor_pixels |= neighbor.pixels
		neighbor.neighbors.add(self)
		neighbor.neighbor_pixels |= self.pixels
	
	def in_neighbors(self, pixel):
		return pixel in self.neighbor_pixels

	def count_neighbors(self):
		return len(self.neighbors)


if __name__ == '__main__':
	main()
