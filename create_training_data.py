from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import random
import os
import string
from tqdm import tqdm

NUM_IMAGES = 10000
IMG_WIDTH = 64
IMG_HEIGHT = 32

out_dir = 'Training Data'

in_dir = os.path.join('C:\\','Users', 'Max Marcus', 'github', 'Training-Data-Creator', 'Output Images', 'No Text')

def get_images(in_dir, out_dir):
    for image_num in tqdm(range(NUM_IMAGES)):
        for i in range(10):
            try:
                image = Image.open(os.path.join(in_dir, os.listdir(in_dir)[image_num], 'finalImage.jpg')).convert('L')

                crop_x = random.randint(0, image.width - IMG_WIDTH * 2)
                crop_y = random.randint(0, image.height - IMG_WIDTH * 2)

                image = image.crop((crop_x, crop_y, crop_x + IMG_WIDTH * 2, crop_y + IMG_HEIGHT * 2))
                image.crop((IMG_WIDTH//2, IMG_HEIGHT//2, IMG_WIDTH + IMG_WIDTH//2, IMG_HEIGHT + IMG_HEIGHT//2)).save(os.path.join(out_dir, 'No Text', str(image_num + (i * NUM_IMAGES)) + '.jpg'))

                image_draw = ImageDraw.Draw(image)

                text = ''
                for letters in range(random.randint(3, 7)):
                    text += random.choice(string.ascii_letters.lower())

                x_pos = IMG_WIDTH//2 + random.randint(-IMG_WIDTH//5, IMG_WIDTH//5)
                y_pos = IMG_HEIGHT//2 + random.randint(-IMG_HEIGHT//5, IMG_HEIGHT//5)

                if x_pos > 20 and y_pos > 12:
                    font_size = random.randint(8, 45)
                else:
                    font_size = random.randint(12, 45)

                font = ImageFont.truetype(os.path.join('Fonts', random.choice(os.listdir('Fonts'))), font_size)

                image_draw.text((x_pos, y_pos), text, (random.randint(75, 190)), font)

                image = image.crop((IMG_WIDTH//2, IMG_HEIGHT//2, IMG_WIDTH + IMG_WIDTH//2, IMG_HEIGHT + IMG_HEIGHT//2))

                image.save(os.path.join(out_dir, 'Text', str(image_num + (i * NUM_IMAGES)) + '.jpg'))
            except Exception as e:
                print(e)



def get_notext_images(in_dir, out_dir):
    for image_num in tqdm(range(NUM_IMAGES)):
        for i in range(2):
            try:
                image = Image.open(os.path.join(in_dir, os.listdir(in_dir)[image_num], 'finalImage.jpg')).convert('L')

                crop_x = random.randint(0, image.width - IMG_WIDTH)
                crop_y = random.randint(0, image.height - IMG_WIDTH)

                image = image.crop((crop_x, crop_y, crop_x + IMG_WIDTH, crop_y + IMG_HEIGHT))

                image.save(os.path.join(out_dir, 'No Text', str(image_num) + '.jpg'))

            except:
                pass

get_images(in_dir, out_dir)
