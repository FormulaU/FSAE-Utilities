from scipy import misc
import matplotlib.pyplot as plt
import imageio
import numpy
import os

track_thresh = 300
border = 5
base_path = '../images/gen/hollow_tracks/' 
inner_color = 128

def main():	
	for filename in os.listdir(base_path):
		path_track(base_path, filename)

def path_track(path, name):
	print(path+name)
	f = imageio.imread(path+name, pilmode='L')

	#Create the paths for the hollow tracks
	from skimage import measure
	contours = measure.find_contours(f, 0.5, fully_connected='high')

	
	from skimage.draw import ellipse
	from skimage.measure import find_contours, approximate_polygon, subdivide_polygon
	  
	contour = contours[0]
	new_s = contour.copy()
	appr_s = approximate_polygon(new_s, tolerance=0.8)
	    
	fig, (ax1, ax2) = plt.subplots(ncols=2, figsize=(9, 4))
	ax2.plot(contour[:, 0], contour[:, 1])
	ax1.plot(appr_s[:, 0], appr_s[:, 1])
	
	for n, contour in enumerate(contours):
		plt.plot(contour[:, 1], contour[:, 0], linewidth=2)
		
	plt.show()
if __name__ == '__main__':
	main()
