import imageio.v3 as iio
from PIL import Image
import numpy as np

def resize_image(image, size):
    return image.resize(size, Image.LANCZOS)

filenames = ['chicklet1.png', 'chicklet2.png', 'chicklet3.png','chicklet4.png']
images = []

first_image = Image.open(filenames[0]).convert('RGB')
image_size = first_image.size

for filename in filenames:
    img = Image.open(filename).convert('RGB') 
    img_resized = resize_image(img, image_size)
    images.append(np.array(img_resized))

shapes = [img.shape for img in images]
print("Image shapes:", shapes) 

if len(set(shapes)) > 1:
    raise ValueError("Not all images have the same shape")

iio.imwrite('chicklet.gif', images, duration=0.5, loop=0)
