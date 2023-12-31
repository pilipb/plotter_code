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
parser.add_argument('-n', type=int, default=50, help='number of lines')

args = parser.parse_args()
input_path = args.input
output_path = args.output
n = args.n
res_init = 25 # steps per pixel
a_init = 10 # amplitude
f_init = 0.1 # frequency

# resize function
def resize(img, height):
    '''
    Resize image to height pixels
    '''
    h, w, c = img.shape
    ratio = height / h
    return cv2.resize(img, (int(w * ratio), height))

# sine wave generator
def sine_wave(last_x, amp, step_x, freq):
    '''
    Generate sine wave continously with amplitude modulated by pixel brightness
    '''
    return np.sin(freq * (last_x + step_x)/np.pi) * amp

# import image
image = cv2.imread(input_path)

# get original image size
h, w, c = image.shape # height, width, channels
# ratio of original image size to number of lines
ratio = h / n

# resize image to number of lines = height pixels
image = resize(image, n)

# convert to grayscale
image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) # only 1 channel
# invert image
# image = cv2.bitwise_not(image)

new_h, new_w = image.shape

# create path
line = Path()
# centre of each row lies at integer value of row index
# reverse direction of line every other row
cols = range(new_w)
last_point = complex(0, 0)

for row in range(new_h):
    # draw horizontal line from left to right
    height = (row*ratio)
    for col in cols:
        # get pixel value
        pix_val = image[row, col]
        width = (col*ratio)
        # change amplitude and frequency based on pixel brightness
        a = 255 * a_init / pix_val # invert image
        f = pix_val * f_init/ 255
        
        ress = range(res_init)
        # switch direction of line every other row
        if row % 2 == 1:
            ress = ress[::-1]

        # draw sine wave with resolution res
        for step in ress:

            # calculate sine wave
            x = width + step * ratio/res_init 
            # TODO: account for phase shift due to frequency modulation by scaling step size
            
            y = height + sine_wave(last_point.real, a, step*f, f)

            # add point to line
            new_point = complex(x, y)
            line.append(Line(last_point, new_point))
            last_point = new_point

    # at the end of each row, connect to start of next row (which is height + ratio)
    line_point = complex(last_point.real, last_point.imag + ratio)
    line.append(Line(complex(last_point.real, last_point.imag), line_point))
    # reverse direction of line every other row
    last_point = line_point
    cols = cols[::-1]

# convert path to svg
wsvg(line, filename='images/path.svg')
# preview svg as png
from cairosvg import svg2png
svg2png(url='images/path.svg', write_to='images/path.png')
plt.imshow(plt.imread('images/path.png'))
plt.show()
# plt.imshow(image, cmap='gray')
# plt.show()

