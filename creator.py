import pydicom
import cv2
import numpy as np
import pylibjpeg
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from PIL import ImageOps
import sys
import random
import os
import json
import string

filename = 'testDicom.dcm'

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

noTextImages = []
textImages = []

noTextImages.append(ImageOps.flip(image))
noTextImages.append(ImageOps.mirror(image))
noTextImages.append(ImageOps.mirror(ImageOps.flip(image)))


fonts = [ImageFont.truetype('Fonts/' + font, int(image.width/3)) for font in os.listdir('Fonts')]
colors = ['white', 'orange', 'gray', 'green', 'red']
textLocations = [
{'x': image.width/20, 'y': image.height/20, 'anchor': 'NW'},
{'x': image.width/20, 'y': image.height - image.height/20, 'anchor': 'SW'},
{'x': image.width - image.width/20, 'y': image.height/20, 'anchor': 'NE'},
{'x': image.width - image.width/20, 'y': image.height - image.height/20, 'anchor': 'SE'},
]
textOptions = {
'Patient Name: ': [True, '* *', '*, *'],
'Patient Sex: ': [True, 'Male', 'Female', 'M', 'F'],
'DateTime': [False, '||/||/||||', '||||/||/||', '* ||, ||||', '||/||/|||| ||:||:|| AM', '||/||/|||| ||:||:|| PM'],
'Comments: ': [True, None],
'ScanData': [False, None],
'Im: ': [True, '||/||'],
'Se: ': [True, '||'],
'WL: ': [True, '||| WW: ||||'],
'T: ': [True, '|.|mm L: ||.|mm'],
'FS: ': [True, '|.|'],
'TR: ': [True, '||||.| TE: |||.|']
}

for imageNum in range(3):
    new_img = image.copy().resize((image.width * 10, image.height * 10), Image.BILINEAR)
    draw = ImageDraw.Draw(new_img)
    data = []
    usedTextLocations = []
    font = fonts[random.randint(0, len(fonts) - 1)]
    color = colors[random.randint(0, len(colors) - 1)]
    for textSection in range(random.randint(1, 4)):
        textLocation = textLocations[random.randint(0, len(textLocations) - 1)]
        if not textLocation in usedTextLocations:
            usedTextLocations.append(textLocation)
            x = textLocation['x'] * 10
            y = textLocation['y'] * 10
            usedTextOptions = []
            text = ''
            for textLines in range(random.randint(1, 4)):
                textOption = list(textOptions)[random.randint(0, len(textOptions) - 1)]
                if not textOption in usedTextOptions:
                    usedTextOptions.append(textOption)
                    textOptionOption = textOptions[textOption][random.randint(1, len(textOptions[textOption]) - 1)]

                    if textOptions[textOption][0] == True:
                        text += textOption

                    if textOptionOption == None:
                        for word in range(random.randint(3, 5)):
                            for letter in range(random.randint(3, 7)):
                                text += random.choice(string.ascii_letters.lower())
                            text += ' '
                    else:
                        for char in textOptionOption:
                            if char == '|':
                                text += str(random.randint(0, 9))
                            elif char == '*':
                                for letter in range(random.randint(3, 7)):
                                    text += random.choice(string.ascii_letters.lower())
                            else:
                                text += char
                text += '\n'

            width, height = draw.multiline_textsize(text, font)
            if 'S' in textLocation['anchor']:
                y -= height

            if 'E' in textLocation['anchor']:
                x -= width

            draw.multiline_text((x, y), text, color, font)
            bbox = {'x0': x, 'y0': y, 'x1': x + width, 'y1': y + width}
            data.append({'bbox': bbox, 'text': text})

    textImages.append([new_img.resize((image.width, image.height), Image.BILINEAR), data])


for image in range(len(textImages)):
    try:
        os.mkdir('Output Images/' + str(image))
    except:
        print('New directory not created')

    textImages[image][0].save('Output Images/' + str(image) + '/finalImage.jpg')
    with open('Output Images/' + str(image) + '/data.json', 'w+') as file:
        json.dump(textImages[image][1], file)
