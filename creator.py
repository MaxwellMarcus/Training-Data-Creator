import pydicom
import cv2
import numpy as np
import pylibjpeg
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

filename = 'testDicom2.dcm'

#get pixel data from image
ds = pydicom.read_file(filename)
ds.PhotometricInterpretation = 'YBR_FULL'
image = ds.pixel_array

new_img = []
max_value = None
min_value = None

#get maximum and minimum pixel values
if (len(image.shape) == 2):
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
    cv2.imwrite('tempImage.jpg', new_img)

else:
    cv2.imwrite('tempImage.jpg', image[0])

image = Image.open('tempImage.jpg')
draw = ImageDraw.Draw(image)
font = ImageFont.truetype('Fonts/Arial.ttf', 150)
try:
    draw.text((0, 0), 'Test Text', (255, 255, 255), font=font)
except:
    draw.text((0, 0), 'Test Text', 255, font=font)

image.save('finalImage.jpg')
