#from scipy import misc
import imageio
import numpy
import os
import csv
from racetrack import racetrack
from racetrack import path_t
from racetrack import sectioned_track
from racetrack import section
import pickle
from scipy.interpolate import CubicSpline
import matplotlib.pyplot as plt
from matplotlib import collections  as mc
#from scipy.optimize import minimize_scalar
from scipy.optimize import basinhopping

base_path = '../data/gen/sectionized_tracks/'
target_path = '../data/gen/shortest_path_tracks/'
PLOT_PATH = '../images/gen/shortest_path_plots/'

PLOT=True

def main():	
	for filename in os.listdir(base_path):
		find_shortest_path(base_path, filename)

def find_shortest_path(base_path, filename):
	print(base_path+filename)
	track = pickle.load(open(base_path+filename, "rb"))

	bounds = [(0,1)] * len(track.outer_path.t)
	guess = [0]*len(track.outer_path.t)
	#Find the set of weights that correspond to the shortest path.
	optimize = lambda x: track.shortest_path_len_sq(x)
	res = basinhopping(optimize, guess, niter=1, minimizer_kwargs={"method" : "L-BFGS-B", "bounds" : bounds})
	for idx in range(len(res.x)):
		track.sections[idx].shortest_pt = res.x[idx]
	#Attempt to plot the data:
	if PLOT:
		plot(track, filename)
	pickle.dump(track,open(target_path+filename, "wb"))

#Plots the track passed.
def plot(track, name):  
#	fig, ax = plt.subplots()
	image = imageio.imread(track.filepath, pilmode='L')
	t = numpy.linspace(0,1,10000)
	paths = [track.outer_path] + track.inner_paths
	#for path in paths:
	#	plt.plot(path.x_cs(t), path.y_cs(t))
	plt.imshow(numpy.flip(numpy.rot90(image, k=1), axis=0), cmap='Greys_r')

	#Plot the sections and shortest path. Build a collection of lines, plot them on the chart.
	line_col = []
	short_x = []
	short_y = []
	for section in track.sections:
		line_col += [section.start]
		short_x += [section.map_scalar_pt(section.shortest_pt)[0]]
		short_y += [section.map_scalar_pt(section.shortest_pt)[1]]
	lc = mc.LineCollection(line_col, color='r', linewidths=2)
	#plt.gca().add_collection(lc)
	
	#Plot the shortest path:
	plt.plot(short_x, short_y, linewidth=3)
	
	#Save and show
	plt.savefig(PLOT_PATH+name+"ng")
	plt.show()

	plt.clf()
if __name__ == '__main__':
	main()
