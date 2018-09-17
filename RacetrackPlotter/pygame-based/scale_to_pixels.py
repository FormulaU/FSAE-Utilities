

def scale_pts(data, scale):
    scaled = []
    for lines in data:
        scaled = scaled + [[]]
        for point in lines:
            scaled[-1] = scaled[-1] + [[int(point[0]*scale[0]), int(point[1]*scale[1])]]

    return scaled
