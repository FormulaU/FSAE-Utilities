from scipy import misc
import imageio
import numpy
import os

track_thresh = 300
border = 5
base_path = '../images/gen/upscaled/' 
def main():	
	for filename in os.listdir(base_path):
		hollow_track(base_path, filename)

def hollow_track(path, name):
	print(path+name)
	f = imageio.imread(path+name, pilmode='L')
	#Look for black pixels. When we find one, flood fill, recording every pixel, and turning non-border pixels white..
	for row in range(len(f)):
		col = 0
		for col in range(len(f[0])):
			if f[row][col] == 0:
				fill_obj = hollow_fill((row,col),f)
				fill_obj.save('../images/gen/hollow_tracks/'+name)
				return #We don't have to look for more than one racetrack.

	
class hollow_fill:
	def __init__(self, pixel, image):
		self.image = image
		#initialize our set, and call flood_fill_rec on our pixel.
		self.pixels = set()
		self.inside_pixels = set()
		self.min = (numpy.inf, numpy.inf)
		self.max = (-1,-1)
		self.flood_fill_rec(pixel)
		#Once this returns, we ought to have the whole contiguous shape, with a set of non-border pixels.
		#White out the inside pixels.
		for inside_pixel in self.inside_pixels:
			image[inside_pixel[0]][inside_pixel[1]] = 255
		print("Created fill with " + str(len(self.pixels)) + " pixels.")

	
	def save(self, name):
		#Save
		imageio.imsave(name, self.image)

	def flood_fill_rec(self, pixel):
		neighbors = set()
		neighbors.add(pixel)
		while len(neighbors) > 0:
			pixel = neighbors.pop()
			#Make sure the pixel is actually black.
			if self.image[pixel[0]][pixel[1]] != 0:
				continue

			#Add the pixel to our set of pixels
			self.pixels.add(pixel)
			
			#Check min/max: If we're smaller or larger, update.
			if pixel[0] < self.min[0]:
				self.min = (pixel[0], self.min[1])
			if pixel[1] < self.min[1]:
				self.min = (self.min[0], pixel[1])

			if pixel[0] > self.max[0]:
				self.max = (pixel[0], self.max[1])
			if pixel[1] > self.max[1]:
				self.max = (self.max[0], pixel[1])
			
			#If our pixel isn't a border pixel, add it to our inside pixels set
			if not self.is_border_pixel(pixel):
				self.inside_pixels.add(pixel)
			#Call add our neighbors
			n_neigh = get_neighbors(pixel)
			for n in n_neigh:
				if n not in self.pixels:
					neighbors.add(n)
	def is_border_pixel(self, pixel):
		n_neigh = get_neighbors(pixel)
		for n in n_neigh:
			#If we have a neighbor that's white, we're on the border.
			if self.image[n[0]][n[1]] == 255:
				return True
		return False

def get_neighbors(pixel):
	neighbors = []
	neighbors += [(pixel[0]-1, pixel[1]+1)]
	neighbors += [(pixel[0]-1, pixel[1])]
	neighbors += [(pixel[0]-1, pixel[1]-1)]
	neighbors += [(pixel[0], pixel[1]-1)]
	neighbors += [(pixel[0]+1, pixel[1]-1)]
	neighbors += [(pixel[0]+1, pixel[1])]
	neighbors += [(pixel[0]+1, pixel[1]+1)]
	neighbors += [(pixel[0], pixel[1]+1)]
	return neighbors

if __name__ == '__main__':
	main()
