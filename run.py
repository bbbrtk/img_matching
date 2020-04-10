import sys, os, time, argparse
import cv2
import numpy as np
from scipy import ndimage
import matplotlib.pyplot as plt

def parser():
    """ Parse arguments """
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("path")
    parser.add_argument("N")

    return parser.parse_args()

"""
TODO
1. find approx right angles (2) -> abs(x-90)
2. find bottom base (long line)
3.  for whole_len of bottom_base: 
        find a black/white point above
        calculate length
        create sth like chart to check if its correct
"""

def generate_rectangle(contours):
    rect = cv2.minAreaRect(contours[0])
    # rotate_angle = rect[2]
    return rect

def draw_rectangle(rect, img):
    box = cv2.boxPoints(rect)
    box = np.int0(box)
    cv2.drawContours(img,[box],0,(0,0,255), 1)

def draw_contours(contours, img):
    cv2.drawContours(img, contours, -1, (255,255,255), 1)

def rotate(contours, img):
    rect = generate_rectangle(contours)
    angle = rect[2]
    img = ndimage.rotate(img, angle)
    height, width, _ = img.shape
    if height > width:
        img = ndimage.rotate(img, 90)
    return img

def print_plot(some_list):
    print(some_list)
    plt.plot(range(len(some_list)), some_list)
    plt.show()

def extract_top_bottom(img):
    bottom = []
    top = []
    for pixel in range(0, img.shape[1]-1, 1):
        white_points = np.where(img[:, pixel] == [255,255,255])[0]

        if len(white_points) > 0:
            min_white = min(white_points)
            max_white = max(white_points)

            if abs(min_white-max_white) > 10:
                bottom.append(max_white)
                top.append(min_white)
            else:
                bottom.append(0)
                top.append(0)
                
        else:
            bottom.append(0)
            top.append(0)

    return bottom, top

def match(imglist):
    img = imglist[0]
    
    # find first contours
    imggray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    contours, _ = cv2.findContours(imggray, 2, cv2.CHAIN_APPROX_SIMPLE)

    # rotate
    img = rotate(contours, img)

    # update contours and draw
    imggray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    contours, _ = cv2.findContours(imggray, 2, cv2.CHAIN_APPROX_NONE)
    img = img * 0
    draw_contours(contours, img)

    # get statistics
    bottom, top = extract_top_bottom(img)
    print_plot(top)
    print_plot(bottom)


    # tab = tab - min(tab)
    
    # save image
    cv2.imwrite('test_image.png',img)
    print(img.shape)








    matching_order = "1"
    return matching_order


def get_image(dirpath, imgname):
    path =  os.path.join(dirpath, str(imgname)+'.png')
    if os.path.exists(path): 
        return cv2.imread(path)
    else:
        sys.exit(f'ERROR: File {path} does not exist')


def main():
    args = parser()
    imglist = []

    for i in range(int(args.N)):
        imglist.append( get_image(args.path, i) )
    
    match(imglist)


if __name__ == "__main__":
    main()