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
import numpy as np
import matplotlib.pyplot as plt
import cv2
import argparse
from svgpathtools import Path, Line, wsvg
from cairosvg import svg2png

# resize function
def resize(img, height):
    h, w, _ = img.shape
    ratio = height / h
    return cv2.resize(img, (int(w * ratio), height))

# sine wave generator
def sine_wave(phase, amp):
    return np.sin(phase) * amp

# main function
if __name__ == '__main__':

    # argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument('-input', type=str, default='images/input.jpeg', help='path to input image')
    parser.add_argument('-output', type=str, default='images/output.jpeg', help='path to output image')
    parser.add_argument('-n', type=int, default=30, help='number of lines')
    args = parser.parse_args()

    input_path = args.input
    output_path = args.output
    n = args.n

    # import image
    image = cv2.imread(input_path)
    h, w, _ = image.shape
    ratio = h / n

    # resize, grayscale, invert
    image = resize(image, n)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    new_h, new_w = image.shape
    image = 255 - image

    # define parameters
    res_init = 15  # steps per pixel
    a_init = ratio * 0.7 # max amplitude is 70% of pixel height
    f_init = np.pi

    # create path
    line = Path()
    cols = range(new_w)
    last_point = complex(0, 0)

    # for each row, draw horizontal line
    for row in range(new_h):
        height = row * ratio
        for col in cols:
            # get pixel value
            pix_val = image[row, col]
            width = col * ratio
            # change amplitude and frequency based on pixel value
            a = a_init * pix_val/255
            f = f_init * pix_val/255
            ress = range(res_init)
            if row % 2 == 1:
                ress = ress[::-1]

            # draw sine wave
            phase = 0
            for step in ress:
                x = width + step * ratio / res_init
                phase += f * 2 * np.pi / res_init  # account for phase shift due to frequency modulation
                y = height + sine_wave(phase, a)
                # add line to path
                new_point = complex(x, y)
                line.append(Line(last_point, new_point))
                last_point = new_point

        # connect end of line to start of next line
        line_point = complex(last_point.real, last_point.imag + ratio)
        line.append(Line(complex(last_point.real, last_point.imag), line_point))
        last_point = line_point
        cols = cols[::-1]

    # convert path to svg
    wsvg(line, filename='images/path.svg')

    # preview svg as png
    svg2png(url='images/path.svg', write_to='images/path.png')

    # Display images side by side
    plt.figure(figsize=(12, 6)) 
    # display the first image (sine wave)
    plt.subplot(1, 2, 1)
    plt.imshow(plt.imread('images/path.png'))
    plt.title('Sine Wave Image')
    # display the second image (original grayscale image)
    plt.subplot(1, 2, 2)
    plt.imshow(image, cmap='gray')
    plt.title('Original Grayscale Image')
    plt.show()