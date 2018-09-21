from scipy import misc
import matplotlib.pyplot as plt
import imageio
import numpy
import os
from math import floor
from math import ceil
import cv2

scale_factor = 2
min_side_width = 800

base_path = '../images/gen/tracks/'
target_path = '../images/gen/upscaled/'

def main():	
	for filename in os.listdir(base_path):
		upscaled = upscale_track(base_path, filename)	

		upscaled = cv2.convertScaleAbs(upscaled)
		imageio.imsave(target_path + filename, upscaled)

def upscale_track(path, name):
	print(path+name)
	f = imageio.imread(path+name, pilmode='L')

	#We want to upscale to the correct side length.
	if min(len(f), len(f[0])) > min_side_width:
		return f
	
#	scale_factor = 0
#	if len(f) < len(f[0]):
#		scale_factor = int(ceil(min_side_width/len(f)))
#	else:	
#		scale_factor = int(ceil(min_side_width/len(f[0])))

	upscaled = numpy.full((scale_factor*len(f),scale_factor*len(f[0])), 255)
	for row in range(len(upscaled)):
		for col in range(len(upscaled[0])):
			upscaled[row][col] = f[floor(row/scale_factor)][floor(col/scale_factor)]
#			if upscaled[row][col] != 255:
#				print("Pixel at ("+str(row)+","+str(col)+") is: " + str(upscaled[row][col]))
	
	return upscaled

if __name__ == '__main__':
	main()
