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
#from scipy.optimize import minimize_scalar
from scipy.optimize import basinhopping

base_path = '../data/gen/converted_tracks/'
target_path = '../data/gen/sectionized_tracks/'
PLOT_PATH = '../images/gen/sectionized_track_plots/'

PLOT=True

def main():	
	for filename in os.listdir(base_path):
		sectionize(base_path, filename)

def sectionize(base_path, filename):
	print(base_path+filename)
	track = pickle.load(open(base_path+filename, "rb"))
	sectionized = racetrack()
	sectionized.filepath = track.filepath
	sectionized.outer_path = track.outer_path
	sectionized.inner_paths += [path_t()]
	#For each point in the outer track, find the closest point on any of the inner tracks. Use these points to build one track.
	for idx in range(track.outer_path.len):
		out_x = track.outer_path.x[idx]
		out_y = track.outer_path.y[idx]
		out_t = track.outer_path.t[idx]
		#Best values
		best_sqdist = numpy.inf
		best_t = None
		best_track = None
		if len(track.inner_paths) == 0:
			#If we don't have an inner track, abort.
			return None
		for inner_track in track.inner_paths:
			optimize = lambda t: (inner_track.x_cs(t)-out_x)**2+(inner_track.y_cs(t)-out_y)**2
			#Function is periodic, use constrained optimization.
#			res = minimize_scalar(optimize, bounds=(0,1))
			res = basinhopping(optimize, out_t, niter=40, minimizer_kwargs={"method" : "L-BFGS-B", "bounds" : [(0,1)]})
#			print("Found sol: " + str(res.x))
#			print("Dist: " + str(optimize(res.x)))
#			if not res.success:
#				print("ERROR: Failed to find optimal inner point.")
			if optimize(res.x) < best_sqdist:
				best_t = res.x
				best_sqdist = optimize(best_t)
				best_track = inner_track
#			print(best_sqdist)
		#Generate one inner course with every best value.
		sectionized.inner_paths[0].x += [best_track.x_cs(best_t)]
		sectionized.inner_paths[0].y += [best_track.y_cs(best_t)]
	sectionized.inner_paths[0].t = track.outer_path.t
	#Overwrite the final points with the original points. They should be the same anyway, but just make sure.
	sectionized.inner_paths[0].x[-1] = sectionized.inner_paths[0].x[0]
	sectionized.inner_paths[0].y[-1] = sectionized.inner_paths[0].y[0]
	#Interpolate
	sectionized.inner_paths[0].x_cs = CubicSpline(sectionized.inner_paths[0].t, sectionized.inner_paths[0].x, bc_type='periodic')
	sectionized.inner_paths[0].y_cs = CubicSpline(sectionized.inner_paths[0].t, sectionized.inner_paths[0].y, bc_type='periodic')

	#Attempt to plot the data:
	if PLOT:
		plot(sectionized, filename)
	pickle.dump(track, open(target_path+filename, "wb"))

#Plots the track passed.
def plot(track, name):  
	image = imageio.imread(track.filepath, pilmode='L')
	t = numpy.linspace(0,1,10000)
	paths = [track.outer_path] + track.inner_paths
	for path in paths:
		plt.plot(path.x_cs(t), path.y_cs(t))
	plt.imshow(numpy.flip(numpy.rot90(image, k=1), axis=0), cmap='Greys_r')
	plt.savefig(PLOT_PATH+name+"ng")
#	plt.show()
	plt.clf()
if __name__ == '__main__':
	main()
