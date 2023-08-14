import numpy as np
import cv2
from argparse import ArgumentParser

def shrink_reduce_color(img,height=40,depth=6):
    ratio = img.shape[1]/img.shape[0]
    width = int(height*ratio)
    grey = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    grey = imagem = cv2.bitwise_not(grey)

    grey[grey>=160] = 255

    grey_resized = cv2.resize(grey,(width,height))
    low_depth = grey_resized // (256//depth)

    return low_depth

def construct_svg(img, radius, height=512):
    ratio = img.shape[1]/img.shape[0]
    h = img.shape[0]*radius
    w = img.shape[1]*radius
    scale = height/h
    width = w*scale
    radius *= scale
    svg = f'<?xml version="1.0"?><svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}">'
    for i in range(len(img)):
        for j in range(len(img[0])):
            svg += f'<circle class="dot" cx="{j*radius}" cy="{i*radius}" r="{img[i][j]*scale}" fill="black" />\n'
    svg += '</svg>'
    return svg

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('path')
    parser.add_argument('-r','--rows',type=int, default=100)
    parser.add_argument('-d','--depth',type=int,default=12)
    parser.add_argument('-x','--xdim',type=int,default=512)
    parser.add_argument('-o','--out',type=str)
    args = parser.parse_args()
    
    img_path = args.path
    rows = args.rows
    depth = args.depth
    
    img = cv2.imread(img_path)
    shrunk_img = shrink_reduce_color(img,height=rows,depth=depth)
    svg_data = construct_svg(shrunk_img, depth*2 - 2,height=args.xdim)
    
    if args.out:
        with open(args.out,'w') as file:
            file.write(svg_data)
    else:
        sys.stdout.buffer.write(svg_data)