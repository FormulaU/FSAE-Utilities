from scipy import misc
from scipy import spatial
from scipy.interpolate import CubicSpline
import matplotlib.pyplot as plt
import imageio
import numpy
import os
import csv

track_thresh = 300
border = 5
img_base_path = '../images/gen/filled_tracks/' 
pt_base_path = '../data/gen/point_list/'
inner_color = 128

num_quads = 100

class path_t:
	def __init__(self):
		self.t = []
		self.x = []
		self.y = []

def main():	
	for filename in os.listdir(img_base_path):
		pt_name = filename[:filename.rfind('.')]
		path_track(img_base_path, filename, pt_base_path, pt_name)

def path_track(img_path, img_name, pt_path, pt_name):
	print(img_path+img_name)
	f = imageio.imread(img_path+img_name, pilmode='L')
	#Build path lists.
	paths = []
	if len(os.listdir(pt_path+pt_name)) > 2:
		print("More than 2 paths. Skipping.")
		return

	for filename in os.listdir(pt_path+pt_name):
		paths += [path_t()]
#		print(paths)
		pt_set = filename_to_set(pt_path+pt_name+'/', filename)
		pts = floodfill_order(pt_set)
		for idx in range(len(pts)):
			paths[-1].x += [pts[idx][0]]
			paths[-1].y += [pts[idx][1]]


		decimate(paths[-1])

		paths[-1].x += [paths[-1].x[0]]
		paths[-1].y += [paths[-1].y[0]]
		paths[-1].len = len(paths[-1].x)
		paths[-1].t = numpy.linspace(0,1, paths[-1].len)
#		print(paths[-1].len)
#		print(len(paths[-1].x))
#		print(len(paths[-1].y))
#		print(len(paths[-1].t))

	#Interpolate
	for path in paths:
#		print(path.x)
		path.x_cs = CubicSpline(path.t, path.x, bc_type='periodic')
		path.y_cs = CubicSpline(path.t, path.y, bc_type='periodic')
		t = numpy.linspace(0,1, 10000)
#		print(path.x_cs(t))
#		plt.plot(t, path.x_cs(t))
#		plt.show()
#		plt.plot(t, path.y_cs(t))
#		plt.show()
		plt.plot(path.x_cs(t), path.y_cs(t))
#		plt.plot(t, path.x_cs(t))
#		plt.plot(t, path.y_cs(t))
		quad_t = numpy.linspace(0,1,num_quads)
		plt.plot(path.x_cs(quad_t), path.y_cs(quad_t), marker='o', linewidth=0, markersize=3, color="red")
	plt.imshow(numpy.flip(numpy.rot90(f, k=1), axis=0), cmap='Greys_r')
	plt.show()

def build_paths(pt_set):
	pt_list = []
	while len(pt_set) > 0:
		pt_list += [floodfill_order(pt_set)]
	print("Found " + str(len(paths)) + "paths")


def filename_to_set(pt_path, pt_name):
	ret = set()
	with open(pt_path+pt_name) as csvfile:
		reader = csv.reader(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
		for row in reader:
			ret.add((int(row[0]), int(row[1])))
	return ret

def decimate(path):
	decimation_const = 20
	path.x = path.x[::decimation_const]
	path.y = path.y[::decimation_const]

def floodfill_order(pt_set):
	ret = [pt_set.pop()]
	found_points = set(ret)
	while len(found_points) != len(pt_set):
		length = len(ret)
		for pix in get_neighbors(ret[-1]):
			if pix in pt_set: 
				if pix not in found_points:
					ret += [pix]
					found_points.add(pix)
		if length == len(ret):
			print("Path is self-intersecting")
			return get_convex_hull(pt_set)
#		print(str(len(found_points)) + ', ' + str(len(pt_set)))
#	print(ret)
	return ret

def get_convex_hull(pt_set):
	points = []
	for pt in pt_set:
		points += [[pt[0], pt[1]]]
	hull = spatial.ConvexHull(points)
	ret = []
	for idx in hull.vertices:
		ret += [points[idx]]
	print(ret)
	return ret

def get_neighbors(pixel):
	neighbors = []
#	neighbors += [(pixel[0]-1, pixel[1]+1)]
	neighbors += [(pixel[0]-1, pixel[1])]
#	neighbors += [(pixel[0]-1, pixel[1]-1)]
	neighbors += [(pixel[0], pixel[1]-1)]
#	neighbors += [(pixel[0]+1, pixel[1]-1)]
	neighbors += [(pixel[0]+1, pixel[1])]
#	neighbors += [(pixel[0]+1, pixel[1]+1)]
	neighbors += [(pixel[0], pixel[1]+1)]
	return neighbors

if __name__ == '__main__':
	main()
