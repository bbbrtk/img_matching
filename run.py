import sys, os, time, argparse
import cv2
import pandas as pd

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
def match(imglist):
    
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