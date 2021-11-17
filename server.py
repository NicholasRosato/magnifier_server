# code written by Nicholas Rosato
# server.py
# EPICS magnifier flask server
# last updated 11/17/2021

from flask import Flask
import os
import cv2
import base64

app = Flask(__name__)

@app.route("/capture_picture")
def capture_picture():
    print("Capturing image with usb camera at video0")
    cam = cv2.VideoCapture(0)
    ret,frame = cam.read()

    if not ret:
        print("Failed to capture frame")
        exit()

    img_name = "magnifier_image.png"
    cv2.imwrite(img_name, frame)
    print("Image written as {}".format(img_name))

    cam.release()    

@app.route("/start_motion")
def start_motion():
    print("Starting motion video server...")
    os.system("sudo service motion start")
    return "MOTION_START"

@app.route("/stop_motion")
def stop_motion():
    print("Stopping motion video server...")
    os.system("sudo service motion stop")
    return "MOTION_STOP"

@app.route("/")
def index():
	return "INDEX"