from scipy import misc
import imageio
import numpy
import os
from copy import deepcopy
import csv
from racetrack import racetrack
from racetrack import path_t
import pickle

base_path = '../images/gen/filled_tracks/'
target_path = '../data/gen/converted_tracks/'
WHITE=255
BLACK=0

def main():	
	for filename in os.listdir(base_path):
		vectorize(base_path, filename)

def vectorize(path, name):
	print(path+name)
	f = imageio.imread(path+name, pilmode='L')
	#Find border paths, save to file.
	track = build_track(f)
#	track.save(target_path+name)

def build_track(image):
	track = racetrack()
	#Scan through the image, looking for paths and painting them as we find them.
	loops = []
	for row in range(len(image)):
		for col in range(len(image[0])):
			pixel = (row,col)
			if color(image, pixel) == BLACK:
				loop = closed_loop(image, pixel)
				if loop != None:
					loops += [closed_loop(image, pixel)]
					paint(image, loop, WHITE)
	print(len(loops))
	return track

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
