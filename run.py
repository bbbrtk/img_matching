import sys, os, time, argparse
import cv2
import numpy as np
from scipy import ndimage
import matplotlib.pyplot as plt
import collections

def parser():
    """ Parse arguments """
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("path")
    parser.add_argument("N")

    return parser.parse_args()

def switch(a, b):
    return b, a

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

def print_plot(slist, name, type):
    # print(slist)
    plt.plot(range(len(slist)), slist)
    # plt.savefig(f'matches/{name}{type}.png')
    # plt.clf()
    plt.show()

def extract_top_bottom(img, direction):
    bottom = []
    top = []

    if direction == 'to_right':   img_width = range(0, img.shape[1]-1, 1)
    elif direction == 'to_left':  img_width = range(img.shape[1]-1, 0, -1)

    for pixel in img_width:
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

def calculate_st_dev(slist):
    slist = list(filter(lambda a: a != 0, slist))
    slist.remove(max(slist))
    slist.remove(min(slist))
    stdev = np.std(slist)
    return stdev

def get_top_coords(img, direction):
    switched = False
    # extract
    bottom, top = extract_top_bottom(img, direction)
    # rotate upside-down if necessary
    stdev_bottom = calculate_st_dev(bottom)
    stdev_top = calculate_st_dev(top)
    if stdev_bottom > stdev_top:
        switched = True
        top, bottom = switch(top, bottom)

    return top, switched

def matching_pair(img):
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

    # save
    # cv2.imwrite('test_image.png',img)
    # cv2.imshow('ImageWindow', img)
    # cv2.waitKey()

    # get coords of upper part of a possible pair-image
    img_pair = img
    top_pair, switched_pair = get_top_coords(img_pair, 'to_left')

    # get coords of upper part of this image
    img_me = cv2.flip(img, -1)
    top_me, switched_me = get_top_coords(img_me, 'to_left')

    # if top-bottom were switched
    if switched_pair:
        top_me, top_pair = switch(top_me, top_pair)

    # print_plot(top_pair, 'TEST','pair')
    # print_plot(top_me, 'TEST', 'me')

    return top_me, top_pair

def squeez(slist):
    slist = list(filter(lambda a: a != 0, slist))
    slist.remove(max(slist))
    slist = np.array_split(slist, 50)
    mean_slist = []
    for e in slist: mean_slist.append(np.mean(e))
    return mean_slist

def match(imglist):
    images = []
    pairs = []
    for i in range(len(imglist)):
        top_me, top_pair = matching_pair(imglist[i])
        
        mean_me = squeez(top_me)
        mean_pair = squeez(top_pair)

        # print_plot(mean_me, i, 'me')
        # print_plot(mean_pair, i, 'pair')

        images.append(mean_me)
        pairs.append(mean_pair)

    for img in images:
        all_matches = {}
        for p in range(len(pairs)):
            val = np.std(np.subtract(img, pairs[p]))
            all_matches[p] = val
        all_sorted = sorted(all_matches.items(), key=lambda kv: kv[1])
        sorted_dict = collections.OrderedDict(all_sorted)
        print(*list(sorted_dict.keys()))
        
    

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