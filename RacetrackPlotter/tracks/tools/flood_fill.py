from scipy import misc
import imageio
import numpy

track_thresh = 300
border = 5
def main():
	f = imageio.imread('../images/racetracks_thresh.png', pilmode='L')
	

	#Look for racetrack pixels. When we find one, run flood fill on it.
	track_cnt = 0
	for row in range(len(f)):
		col = 0
		for col in range(len(f[0])):
			if f[row][col] == 0:
				fill_obj = fill((row,col),f)
				if len(fill_obj.pixels) > track_thresh:
					fill_obj.save('../images/gen/tracks/'+str(track_cnt)+'.png')
					track_cnt += 1
		print(row)

#	imageio.imsave('racetrack_thresh.png', f_threshold)

class fill:
	def __init__(self, pixel, image):
		self.image = image
		#initialize our set, and call flood_fill_rec on our pixel.
		self.pixels = set()
		self.min = (numpy.inf, numpy.inf)
		self.max = (-1,-1)
		self.flood_fill_rec(pixel)
		#Once this returns, we ought to have the whole contiguous shape. While we're at it, we also found the min and max points for bounds.
		print("Created fill with " + str(len(self.pixels)) + " pixels.")
	
	def save(self, name):
		x_dim = self.max[0] - self.min[0] + 1 + 2*border #Plus one, max is on the line.
		y_dim = self.max[1] - self.min[1] + 1 + 2*border
		exp_image = numpy.full((x_dim,y_dim), 255)

		for pixel in self.pixels:
			exp_image[pixel[0]-self.min[0]+border][pixel[1]-self.min[1]+border] = 0
		#Save
		imageio.imsave(name, exp_image)

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
			
			#White our our pixel so we don't overcount it.
			self.image[pixel[0]][pixel[1]] = 255
			#Call add our neighbors
			n_neigh = get_neighbors(pixel)
			for n in n_neigh:
				neighbors.add(n)

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
