from scipy import misc
import imageio
import numpy
import os
from copy import deepcopy
import csv

track_thresh = 300
border = 5
image_path = '../images/gen/filled_tracks/'
point_path = '../data/gen/point_list/'
inner_color = 128
culling_denominator = 3

def main():	
	for filename in os.listdir(image_path):
		fit_splines(image_path, filename)

def fit_splines(path, name):
	print(path+name)
	f = imageio.imread(image_path+name, pilmode='L')
	#Cull the filetype from our name
	name = name[:-name.rfind('.')]
	#Open border paths
	paths = import_paths(point_path+name)

def import_paths(filepath):
	paths = set()
	for filename in os.listdir(filepath):
		with open(filepath+filename) as pts:
			reader = csv.writer(pts, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
if __name__ == '__main__':
	main()
