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

base_path = '../data/gen/normalized_tracks/'
target_path = '../data/gen/sectionized_tracks/'
PLOT_PATH = '../images/gen/sectionized_track_plots/'

PLOT=True

def main():	
	for filename in os.listdir(base_path):
		sectionize(base_path, filename)

def sectionize(base_path, filename):
	print(base_path+filename)
	track = pickle.load(open(base_path+filename, "rb"))
	sectionized = sectioned_track(track)

	#Simple sections for now: One section per t
	for idx  in range(len(sectionized.outer_path.t) - 1):
		start = [(sectionized.inner_paths[0].x[idx], 
			  sectionized.inner_paths[0].y[idx]), 
			  (sectionized.outer_path.x[idx],
			  sectionized.outer_path.y[idx])]
		end = [(sectionized.inner_paths[0].x[idx+1], 
			  sectionized.inner_paths[0].y[idx+1]), 
			  (sectionized.outer_path.x[idx+1],
			  sectionized.outer_path.y[idx+1])]
		sectionized.sections += [section(start, end)]
	#Add the last section(loops to start)
	start = [(sectionized.inner_paths[0].x[-1], 
		  sectionized.inner_paths[0].y[-1]), 
		  (sectionized.outer_path.x[-1],
		  sectionized.outer_path.y[-1])]
	end = [(sectionized.inner_paths[0].x[0], 
		  sectionized.inner_paths[0].y[0]), 
		  (sectionized.outer_path.x[0],
		  sectionized.outer_path.y[0])]
	sectionized.sections += [section(start, end)]

	#Attempt to plot the data:
	if PLOT:
		plot(sectionized, filename)
	pickle.dump(sectionized, open(target_path+filename, "wb"))

#Plots the track passed.
def plot(track, name):  
	image = imageio.imread(track.filepath, pilmode='L')
	t = numpy.linspace(0,1,10000)
	paths = [track.outer_path] + track.inner_paths
	for path in paths:
		plt.plot(path.x_cs(t), path.y_cs(t))
	plt.imshow(numpy.flip(numpy.rot90(image, k=1), axis=0), cmap='Greys_r')
	#Plot the sections. Build a collection of lines, plot them on the chart.
	line_col = []
	for section in track.sections:
		line_col += [section.start]
	lc = mc.LineCollection(line_col, color='r', linewidths=2)
	plt.gca().add_collection(lc)
	
	plt.savefig(PLOT_PATH+name+"ng")
#	plt.show()

	plt.clf()
if __name__ == '__main__':
	main()
