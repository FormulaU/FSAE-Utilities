from scipy import misc
import imageio
import numpy
import os
from copy import deepcopy
import csv

track_thresh = 300
border = 5
base_path = '../images/gen/filled_tracks/'
target_path = '../data/gen/point_list/'
inner_color = 128

def main():	
	for filename in os.listdir(base_path):
		turn_to_points(base_path, filename)

def turn_to_points(path, name):
	print(path+name)
	f = imageio.imread(path+name, pilmode='L')
	#Find border paths, save to file.
	fill_obj = point_fill(f)
	fill_obj.save_pts(target_path+name)
	
class point_fill:
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
				if self.color(pixel) == self.BLACK and pixel not in self.all_pixels:
					self.add_fill(pixel)
			
	def save(self, name):
		#Save
		imageio.imsave(name, self.image)

	def save_pts(self, path):
		#Remove the filetype from the path.
		path = path[:path.rfind('.')]
		try:
			os.mkdir(path)
		except OSError:
			pass
		cnt = 0
		for fill in self.fills:
			self.save_fill(path+'/'+str(cnt), fill)
			cnt += 1

	def save_fill(self, path, fill):
		with open(path, 'w') as csvfile:
			writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
			for pixel in fill.pixels:
				writer.writerow([pixel[0], pixel[1]])
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

	def minimize(self, fill):
		fill_copy = deepcopy(fill)
		for pixel in fill_copy.pixels:
			#Test to make sure the pixel is required. Find the neighbors for this pixel. If this pixel has more than one neighbor, it is required. If it doesn't, it isn't, and should be turned white.
			neighbors = self.find_pixel_neighbors(pixel, fill)
			if len(neighbors) == 1:
				print("Whiting out " + str(pixel))
				self.image[pixel[0]][pixel[1]] = 255
				fill.pixels.remove(pixel)
				neighbors.pop().add(pixel)
	
	def find_pixel_neighbors(self, pixel, fill=None,):
		if fill is None:
			fill = self.find_fill(pixel)
		neighbors = set()
		for n in self.get_neighbors(pixel):
			if n not in fill.pixels:
				neighbors.add(self.find_fill(n))
		return neighbors
	
	def color(self, pixel):
		return self.image[pixel[0]][pixel[1]]
		
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
