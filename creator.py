import pydicom
import cv2
import numpy as np

filename = 'testDicom.dcm'

ds = pydicom.read_file(filename, force=True)
image = ds.pixel_array

new_img = []
max_value = None
min_value = None

for i in image:
    for l in i:
        if max_value:
            if l > max_value:
                max_value = l
        else:
            max_value = l

        if min_value:
            if l < min_value:
                min_value = l
        else:
            min_value = l

for i in image:
    row = []
    for pixel in i:
        row.append((pixel - min_value) / (max_value / 255.0))
    new_img.append(row)

new_img = np.array(new_img)

cv2.imwrite(filename.replace('.dcm', '.jpg'), new_img)
