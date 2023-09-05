import numpy as np
import cv2
import sys
from argparse import ArgumentParser


def shrink_reduce_color(img, height=40, depth=6):
    ratio = img.shape[1]/img.shape[0]
    width = int(height*ratio)
    grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    grey = imagem = cv2.bitwise_not(grey)

    grey[grey >= 160] = 255

    grey_resized = cv2.resize(grey, (width, height))
    low_depth = grey_resized // (256//depth)

    return low_depth


def dot_svg(img, greyscale_depth, height=512, rad_control=1):
    ratio = img.shape[1]/img.shape[0]
    h = img.shape[0]*greyscale_depth
    w = img.shape[1]*greyscale_depth
    scale = height/h
    width = w*scale
    depth = greyscale_depth*scale
    radius = scale*rad_control*0.5
    svg = f'<?xml version="1.0"?><svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}">'
    for i in range(len(img)):
        for j in range(len(img[0])):
            svg += f'<circle class="dot" cx="{j*depth}" cy="{i*depth}" r="{img[i][j]*radius}" fill="black" />\n'
    svg += '</svg>'
    return svg


def line_svg(img, greyscale_depth, height=512, thickness=1):
    ratio = img.shape[1]/img.shape[0]
    h = img.shape[0]*greyscale_depth
    w = img.shape[1]*greyscale_depth
    scale = height/h
    width = w*scale
    depth = greyscale_depth*scale
    svg = f'<?xml version="1.0"?><svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}">'
    for row_num, row in enumerate(img):
        svg += f'\n<path d=\"M 0, {depth*row_num+1}'
        last = 0
        row = [i/16*thickness for i in row]
        diff = []
        for i in row:
            diff.append(i-last)
            last = i

        for i in diff:
            svg += f'c {depth/2},0 {depth/2},{i} {depth},{i}\n'

        svg += f'l 0,-{row[-1]*2+0.25}'

        for i in reversed(diff):
            svg += f'c -{depth/2},0 -{depth/2},{i} -{depth},{i}\n'

        svg += '\"/>'

    svg += '\n</svg>'
    return svg


STYLES = {0: dot_svg,
          1: line_svg}


def construct_svg(shrunk_img, greyscale_depth, height, control, style=0):
    return STYLES[style](shrunk_img, greyscale_depth, height, control)


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('path')
    parser.add_argument('-r', '--rows', type=int, default=100)
    parser.add_argument('-d', '--depth', type=int, default=12)
    parser.add_argument('-x', '--xdim', type=int, default=512)
    parser.add_argument('-s', '--style', type=int, default=0)
    parser.add_argument('-c', '--control', type=float, default=1.0)
    parser.add_argument('-o', '--out', type=str)
    args = parser.parse_args()

    img_path = args.path
    rows = args.rows
    depth = args.depth

    img = cv2.imread(img_path)
    shrunk_img = shrink_reduce_color(img, height=rows, depth=depth)
    svg_data = construct_svg(shrunk_img, depth*2 - 2,
                             args.xdim, args.control, style=args.style)

    if args.out:
        with open(args.out, 'w') as file:
            file.write(svg_data)
    else:
        sys.stdout.buffer.write(svg_data)
