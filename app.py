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



app = Flask(__name__)
CORS(app)
app.config["CLIENT_IMAGES"] = "/home/pi/Desktop/server/"
app.config['CORS_HEADERS'] = 'Content-Type'
image_name = "magnifier_image.png"

@app.route("/get_image")
@cross_origin()
def get_image():
	print("Getting Image from directory- " + app.config["CLIENT_IMAGES"])
	
	# TODO: Fix error handling for all cases
	try:
		print("Capturing image with usb camera at video0")
		cam = cv2.VideoCapture(0)
		ret,frame = cam.read()

		if not ret:
			print("Failed to capture frame")
			# TODO: return a failed to capture stock image

		img_name = "magnifier_image.png"
		cv2.imwrite(img_name, frame)
		print("Image written as {}".format(img_name))

		cam.release() 
		return send_file(image_name)
		
	except FileNotFoundError:
		response = jsonify(message="FILE_ERROR")
		return response

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

