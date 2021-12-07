# code written by Nicholas Rosato
# color_filter.py
# Color filtering functions for the magnifier project
# last updated 11/23/2021

import cv2
import numpy as np

def filter(frame, option):
    # convert from BLUE GREEN RED (RGB) color space to HSV color space
    #hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    print ("Filtering color for frame...")
    
    result = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # THIS CODE IS FOR CONVERTING TO A SPECIFIC COLOR, FOR NOW WE JUST CONVERT TO GREYSCALE
    # threshold for color
    #lower = np.array([60, 35, 140])
    #upper = np.array([180, 255, 255])
    
    #print ("Lower bound: ", lower)
    #print ("Upper bound: ", upper)

    # create a mask
    #mask = cv2.inRange(hsv, lower, upper)

    # remove all non colored regions by ANDing with the mask
    #result = cv2.bitwise_and(frame, frame, mask = mask)

    return result
