'''
Run command line file to generate wiggle lines
1. imports image
2. resizes image to number of lines
3. converst to grayscale
4. for each pixel row, find starting position (as mid point of pixel height)
5. for each pixel row, draw horizontal line from starting position to end of row
6. make each line a sine wave
7. change amplitude of sine wave based on pixel brightness for each pixel 
8. change frequency of sine wave based on pixel brightness for each pixel
        note that the step size is the same for each pixel, but the frequency is different
9. connect end of each line to start of next line
10. save image

'''

# imports
import numpy as np
import matplotlib.pyplot as plt
import cv2
import argparse
from svgpathtools import Path, Line, svg2paths, wsvg

# argument parser
parser = argparse.ArgumentParser()
parser.add_argument('-input', type=str, default='images/input.jpeg', help='path to input image')
parser.add_argument('-output', type=str, default='images/output.jpeg', help='path to output image')
parser.add_argument('-n', type=int, default=40, help='number of lines')

args = parser.parse_args()
input_path = args.input
output_path = args.output
n = args.n

# resize function
def resize(img, height):
    '''
    Resize image to height pixels
    '''
    h, w, c = img.shape
    ratio = height / h
    return cv2.resize(img, (int(w * ratio), height))

# import image
image = cv2.imread(input_path)
# get original image size
h, w, c = image.shape
# ratio of original image size to number of lines
ratio = h / n

# resize image to number of lines = height pixels
image = resize(image, n)

# convert to grayscale
image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# create path
path = Path()
# centre of each row lies at integer value of row index
for i in range(n):
    # draw horizontal line from left to right
    step = int(i*ratio)
    hor = Line(0 + 1j*step, w + 1j*step)  # A line beginning at (200, 300) and ending at (250, 350)
    path.append(hor)  # add the new line to the path    
    continue

# convert path to svg
wsvg(path, filename='images/path.svg')


# show image
plt.imshow(image, cmap='gray')
plt.show()



