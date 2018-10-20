#from scipy import misc
import imageio
import numpy
import os
import csv
from racetrack import racetrack
from racetrack import path_t
import pickle
from scipy.interpolate import CubicSpline
import matplotlib.pyplot as plt

base_path = '../images/gen/filled_tracks/'
target_path = '../data/gen/converted_tracks/'
PLOT_PATH = '../images/gen/vector_plot_tracks/'

WHITE=255
BLACK=0
DECIMATION_CONST=15
PATH_LEN_THRESH=5
PLOT=True

def main():	
	for filename in os.listdir(base_path):
		vectorize(base_path, filename)

def vectorize(path, name):
	f = imageio.imread(path+name, pilmode='L')
	#Find border paths, save to file.
	track = build_track(f, path, name)
	#Replace .png in the string with .p
	name = name.replace(".png", ".p")
	pickle.dump(track, open(target_path+name, "wb"))

def build_track(image, path, name):
	track = racetrack()
	track.filepath = path+name
	print(track.filepath)
	#Scan through the image, looking for paths and painting them as we find them.
	loops = []
	outer_path = None
	for row in range(len(image)):
		for col in range(len(image[0])):
			pixel = (row,col)
			if color(image, pixel) == BLACK:
				loop = closed_loop(image, pixel)
				if loop != None:
					if outer_path==None:
						outer_path = loop
					else:
						loops += [loop]
					paint(image, loop, WHITE)
	# Interpolate the outer path.
	outer_path = convert_to_path_t(outer_path)

	#Process the points (mostly just decimate them)
	outer_path = process_pts(outer_path)

	#Interpolate
	outer_path.x_cs = CubicSpline(outer_path.t, outer_path.x, bc_type='periodic')
	outer_path.y_cs = CubicSpline(outer_path.t, outer_path.y, bc_type='periodic')

	paths = []
	#Repeat the process for all other paths.
	for loop in loops:
		# Interpolate the outer path.
		path = convert_to_path_t(loop)

		#Process the points (mostly just decimate them)
		path = process_pts(path)

		#If we have enough of a path left to bother
		if path.len > PATH_LEN_THRESH:
			#Interpolate
			path.x_cs = CubicSpline(path.t, path.x, bc_type='periodic')
			path.y_cs = CubicSpline(path.t, path.y, bc_type='periodic')
			#Add to our paths list	
			paths += [path]
	if PLOT:
		plot(image, paths + [outer_path], name)
	
	track.outer_path = outer_path
	track.inner_paths = paths

	return track

#Plots the paths on the image passed.
def plot(image, paths, name):
	t = numpy.linspace(0,1,10000)
	for path in paths:
		plt.plot(path.x_cs(t), path.y_cs(t))
	plt.imshow(numpy.flip(numpy.rot90(image, k=1), axis=0), cmap='Greys_r')
	plt.savefig(PLOT_PATH+name)
	plt.clf()
#	plt.show()

#Processes the points so that they're fit for interpolation (decimates, etc)
def process_pts(path):
	path.x = path.x[::DECIMATION_CONST]
	path.y = path.y[::DECIMATION_CONST]
	#Make path periodic if needed, remake t
	if not (path.x[0] == path.x[-1] and path.y[0] == path.y[-1]):
		path.x += [path.x[0]]
		path.y += [path.y[0]]
	path.len = len(path.x)
	path.t = numpy.linspace(0,1,path.len)
	return path

#Converts a list of point tuples into a path object.
def convert_to_path_t(pt_list):
	path = path_t()
	# Take the tuple and split it into arrays
	for pt in pt_list:
		path.x += [pt[0]]
		path.y += [pt[1]]
	# Make the arrays start and end at the same place (imply periodic)
	path.x += [path.x[0]]
	path.y += [path.y[0]]
	path.len= len(pt_list)
	path.t = numpy.linspace(0,1, path.len)
	return path

#Using the passed image and starting at the specified point, try to form the shortest closed loop of black pixels, starting at the specified point.
def closed_loop(image, start):
	#If the pixel isn't black, abort
	if color(image, start) != BLACK:
		return None
	#If the pixel doesn't have exactly two neighbors, then abort.
	path_negh = get_path_neighbors(image, start)
	if len(path_negh) != 2:
		return None

	#Potential paths.
	potential_paths = [[start, path_negh[0]]]
	#Start off on one side of the pixel, target the pixel on the other side.
	target = path_negh[1]
	#Set up our path, and visit the starting pixel so we have to take the long way around.
	visited = set()
	visited.add(start)
#	print(potential_paths)
	while len(potential_paths) > 0:
		path = potential_paths.pop()
#		print(potential_paths)
		if path[-1] not in visited:
			#If the path ends at our target, return it.
			if path[-1] == target:
				return path
			#Add the node to our visited set.
			visited.add(path[-1])
			#For every path neighbor we haven't visited, make a path with that neighbor and add it to our queue.
			path_negh = get_path_neighbors(image, path[-1])
			for pix in path_negh:
				if pix not in visited:
					newpath = [path + [pix]]
					#print("Adding: " + str(newpath))
					potential_paths += [path + [pix]]
		
#Returns all the black pixels neighboring this pixel (manhattan neighboring)
def get_path_neighbors(image, pixel):
	neighbors = []
	tmp = (pixel[0]-1, pixel[1])

	if color(image, tmp) == BLACK:
		neighbors += [tmp]
	tmp = (pixel[0], pixel[1]-1)
	if color(image, tmp) == BLACK:
		neighbors += [tmp]
	tmp = (pixel[0]+1, pixel[1])
	if color(image, tmp) == BLACK:
		neighbors += [tmp]
	tmp = (pixel[0], pixel[1]+1)
	if color(image, tmp) == BLACK:
		neighbors += [tmp]
	return neighbors

def color(image, pixel):
	return image[pixel[0]][pixel[1]]

def paint(image, path, color):
	for pix in path:
		image[pix[0]][pix[1]] = color

if __name__ == '__main__':
	main()
