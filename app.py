# code written by Nicholas Rosato
# server.py
# EPICS magnifier flask server
# last updated 11/17/2021

from flask import Flask, jsonify, send_file
from flask_cors import CORS, cross_origin
from PIL import Image
import os
import cv2
import io
import base64
import color_filter


app = Flask(__name__)
CORS(app)
app.config["CLIENT_IMAGES"] = "/home/pi/Desktop/server/"
app.config['CORS_HEADERS'] = 'Content-Type'
image_name = "magnifier_image.png"

def capture_frame():
	# TODO: Fix error handling for all cases
    print("Capturing image with usb camera at video0")
    cam = cv2.VideoCapture(0)
    ret,frame = cam.read()
    cam.release()
    if not ret:
        print("Failed to capture frame")
		# TODO: return a failed to capture stock image
    
    return frame

    
@app.route("/get_image/<cf_option>/")
@cross_origin()
def get_image(cf_option):
    frame = capture_frame()	    
    
    if (cf_option != "none"):
        frame = color_filter.filter(frame, cf_option)
    
    img_name = "magnifier_image.png"
    cv2.imwrite(img_name, frame)
    print("Image written as {}".format(img_name))

    print("Sending image from directory- " + app.config["CLIENT_IMAGES"])
    return send_file(image_name)
		

@app.route("/start_motion")
@cross_origin()
def start_motion():
	print("Starting motion video server...")
	os.system("sudo service motion start")
	response = jsonify(message="MOTION_START") 
	return response

@app.route("/stop_motion")
@cross_origin()
def stop_motion():
	print("Stopping motion video server...")
	os.system("sudo service motion stop")
	response = jsonify(message="MOTION_STOP")
	return response


@app.route("/")
@cross_origin()
def index():
	response = jsonify(message="INDEX")
	return response

