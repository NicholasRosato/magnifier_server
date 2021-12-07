# code written by Nicholas Rosato
# color_filter.py
# Color filtering functions for the magnifier project
# last updated 11/23/2021

import cv2
import numpy as np

def filter(frame, option):    
    print ("Filtering color for frame...")
       
    # convert image to grayscale
    gray_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # filter the color with binary threashold to make it black and white
    (thresh, bw_image) = cv2.threshold(gray_image, 127, 255, cv2.THRESH_BINARY)

    # THIS CODE IS FOR CONVERTING TO A SPECIFIC COLOR, FOR NOW WE JUST CONVERT TO GREYSCALE
    # This uses a mask operation to do so, leaving it in here for someone who wants to experiment with it
    # threshold for color
    # convert from BLUE GREEN RED (RGB) color space to HSV color space
    #hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    #lower = np.array([60, 35, 140])
    #upper = np.array([180, 255, 255])
    
    #print ("Lower bound: ", lower)
    #print ("Upper bound: ", upper)

    # create a mask
    #mask = cv2.inRange(hsv, lower, upper)

    # remove all non colored regions by ANDing with the mask
    #result = cv2.bitwise_and(frame, frame, mask = mask)

    return bw_image
