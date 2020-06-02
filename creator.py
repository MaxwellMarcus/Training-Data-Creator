import pydicom
import cv2
import numpy as np

filename = 'testDicom.dcm'

#get pixel data from image
ds = pydicom.read_file(filename, force=True)
image = ds.pixel_array

new_img = []
max_value = None
min_value = None

#get maximum and minimum pixel values
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

#use maximum and minimum pixel values to map pixel values between 0 and 255
for i in image:
    row = []
    for pixel in i:
        row.append((pixel - min_value) / (max_value / 255.0))
    new_img.append(row)

#convert to numpy array
new_img = np.array(new_img)

#save image
cv2.imwrite(filename.replace('.dcm', '.jpg'), new_img)
