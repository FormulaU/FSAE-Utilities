from scipy import misc
import imageio
import numpy

f = imageio.imread('racetracks.jpg')
f_threshold = numpy.zeros((len(f), len(f[0])))

print(str(len(f[0])))

#Threshold the image
row = 0
for row in range(len(f)):
    col = 0
    for col in range(len(f[0])):
        if f[row][col][0] > 128:
            f_threshold[row][col] = 255
        else:
            f_threshold[row][col] = 0
    print(row)


imageio.imsave('racetrack_thresh.png', f_threshold)

import matplotlib.pyplot as plt
plt.imshow(f_threshold)
plt.show()
