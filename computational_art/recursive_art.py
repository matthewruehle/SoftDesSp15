""" 
Generates semi-random image files.
Matt Ruehle, Feb 2015
"""

import random
from random import choice
import datetime
import math
from math import pi
from PIL import Image


def build_random_function(min_depth, max_depth):
    """ Builds a random function of depth at least min_depth and depth
        at most max_depth (see assignment writeup for definition of depth
        in this context)

        min_depth: the minimum depth of the random function
        max_depth: the maximum depth of the random function
        returns: the randomly generated function represented as a nested list
                 (see assignment writeup for details on the representation of
                 these functions)

        Note: Assuming that the inputs are integers. Could probably add a coerce or something, but shouldn't be necessary.
    
        Also, in my opinion -- abs and neg_abs are aesthetically unpleasant. They work for the requirements, but Imma figure out a different operation because they make everything a bit gray-er.
    """
    function_options = ["prod","cos_pi","sin_pi", "avg"]
    #other functions which can be used in this list: abs, neg_abs, wrap_shift, cos_2pi, sin_2pi
    depth = random.randint(min_depth, max_depth)
    if depth == 1:
        return [choice(["x","y"])]
    else:
        new_recurse = [choice(function_options)]
        if new_recurse[0] in ["prod","avg"]:
            new_recurse.append(build_random_function(depth-1, depth-1))
            new_recurse.append(build_random_function(depth-1, depth-1))
        else:
            new_recurse.append(build_random_function(depth-1, depth-1))
        return new_recurse

def evaluate_random_function(f, x, y,t = 0):
    """ Evaluate the random function f with inputs x,y
        Representation of the function f is defined in the assignment writeup

        f: the function to evaluate
        x: the value of x to be used to evaluate the function
        y: the value of y to be used to evaluate the function
        returns: the function value

        >>> evaluate_random_function(["x"],-0.5, 0.75)
        -0.5
        >>> evaluate_random_function(["y"],0.1,0.02)
        0.02
    """
    if f[0] == 'x':
        return x
    elif f[0] == 'y':
        return y
    elif f[0] == 't':
        return t
    elif f[0] == 'sin_pi':
        return math.sin(pi * evaluate_random_function(f[1],x,y,t))
    elif f[0] == 'cos_pi':
        return math.cos(pi * evaluate_random_function(f[1],x,y,t))
    elif f[0] == 'sin_2pi':
        return math.sin(2*pi * evaluate_random_function(f[1],x,y,t))
    elif f[0] == 'cos_2pi':
        return math.cos(2*pi * evaluate_random_function(f[1],x,y,t))    
    elif f[0] == 'abs':
        return math.fabs(evaluate_random_function(f[1],x,y,t))
    elif f[0] == 'neg_abs':
        return -1 * math.fabs(evaluate_random_function(f[1],x,y,t))
    elif f[0] == 'prod':
        return evaluate_random_function(f[1],x,y,t) * evaluate_random_function(f[2],x,y,t)
    elif f[0] == 'avg':
        return (evaluate_random_function(f[1],x,y,t) + evaluate_random_function(f[2],x,y,t)) * 0.5
    elif f[0] == 'wrap_shift':
        shifted = evaluate_random_function(f[1],x,y,t) + 1
        if shifted > 1:
            return shifted - 2
        else:
            return shifted
    else:
        print("ERROR: ERF passed something wrong.")

def remap_interval(val, input_interval_start, input_interval_end, output_interval_start, output_interval_end):
    """ Given an input value in the interval [input_interval_start,
        input_interval_end], return an output value scaled to fall within
        the output interval [output_interval_start, output_interval_end].

        val: the value to remap
        input_interval_start: the start of the interval that contains all
                              possible values for val
        input_interval_end: the end of the interval that contains all possible
                            values for val
        output_interval_start: the start of the interval that contains all
                               possible output values
        output_inteval_end: the end of the interval that contains all possible
                            output values
        returns: the value remapped from the input to the output interval
        >>> remap_interval(0.5, 0, 1, 0, 10)
        5.0
        >>> remap_interval(5, 4, 6, 0, 2)
        1.0
        >>> remap_interval(5, 4, 6, 1, 2)
        1.5
    """
    if val < input_interval_start or val > input_interval_end:
        print("Input out of bounds.")
    else:
        portion_of_input = (val - float(input_interval_start)) / (input_interval_end - input_interval_start)
        amount_of_output = portion_of_input * (output_interval_end - output_interval_start)
        result = output_interval_start + amount_of_output
        return result

def color_map(val):
    """ Maps input value between -1 and 1 to an integer 0-255, suitable for
        use as an RGB color code.

        val: value to remap, must be a float in the interval [-1, 1]
        returns: integer in the interval [0,255]

        >>> color_map(-1.0)
        0
        >>> color_map(1.0)
        255
        >>> color_map(0.0)
        127
        >>> color_map(0.5)
        191
    """
    color_code = remap_interval(val, -1, 1, 0, 255)
    return int(color_code)

def test_image(filename, x_size=350, y_size=350):
    """ Generate test image with random pixels and save as an image file.

        filename: string filename for image (should be .png)
        x_size, y_size: optional args to set image dimensions (default: 350)
    """
    im = Image.new("RGB", (x_size, y_size))
    pixels = im.load()
    for i in range(x_size):
        for j in range(y_size):
            x = remap_interval(i, 0, x_size, -1, 1)
            y = remap_interval(j, 0, y_size, -1, 1)
            pixels[i, j] = (random.randint(0, 255),  # Red channel
                            random.randint(0, 255),  # Green channel
                            random.randint(0, 255))  # Blue channel

    im.save(filename)

def generate_art(filename, x_size=350, y_size=350, t_number=100):
    """ Generate computational art and save as an image file.

        filename: string filename for image (should be .png)
        x_size, y_size: optional args to set image dimensions (default: 350)
    """
    # Functions for red, green, and blue channels - where the magic happens!
    red_function = build_random_function(7,9)
    green_function = build_random_function(7,9)
    blue_function = build_random_function(7,9)

    # Create image and loop over all pixels
    im = Image.new("RGB", (x_size, y_size))
    pixels = im.load()
    for i in range(x_size):
        for j in range(y_size):
            x = remap_interval(i, 0, x_size, -1, 1)
            y = remap_interval(j, 0, y_size, -1, 1)
            pixels[i, j] = (
                    color_map(evaluate_random_function(red_function, x, y)),
                    color_map(evaluate_random_function(green_function, x, y)),
                    color_map(evaluate_random_function(blue_function, x, y))
                    )

    im.save(filename)

def generate_animation(filename, x_size=350, y_size=350, t_number=100):
    """ Generate computational art and save as an image file.

        filename: string filename for image (should be .png)
        x_size, y_size: optional args to set image dimensions (default: 350)
        t_number: number of frames to do
    """
    # Functions for red, green, and blue channels - where the magic happens!
    red_function = build_random_function(7,9)
    green_function = build_random_function(7,9)
    blue_function = build_random_function(7,9)

    # Create image and loop over all pixels
    im = Image.new("RGB", (x_size, y_size))
    pixels = im.load()
    for k in range(t_number):
        for i in range(x_size):
            for j in range(y_size):
                x = remap_interval(i, 0, x_size, -1, 1)
                y = remap_interval(j, 0, y_size, -1, 1)
                t = remap_interval(k, 0, t_number, -1, 1)
                pixels[i, j] = (
                        color_map(evaluate_random_function(red_function, x, y, t)),
                        color_map(evaluate_random_function(green_function, x, y, t)),
                        color_map(evaluate_random_function(blue_function, x, y, t)))
        im.save("%03d_" + filename) % k+1
        im.save(str(t_number*2 - k) + "_" + filename)

def make_animation():
    generate_animation("my_animation.png",600,600,100)

def make_pretty_picture():
    now = datetime.datetime.now()
    generate_art("myart_" + str("-".join(str(i) for i in [now.month,now.day,now.hour,now.minute])) + ".png",1920,1080,1)



if __name__ == '__main__':
    # import doctest
    # doctest.testmod()
make_pretty_picture()
# make_animation()