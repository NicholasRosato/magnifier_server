# code written by Nicholas Rosato
# server.py
# EPICS magnifier flask server
# last updated 11/17/2021

from flask import Flask, jsonify
import os
import cv2
import base64
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)
app.config["CLIENT_IMAGES"] = "/home/pi/Desktop/server/"
app.config['CORS_HEADERS'] = 'Content-Type'
image_name = "magnifier_image.png"

@app.route("/get_image")
@cross_origin()
def get_image():
	print("Getting Image from directory- " + app.config["CLIENT_IMAGES"])
	# invoke rpi to take image with usb camera
	# save usb image to img send_from_directory
	# encode image into base64 and send to device via the request
	try:
		print(app.config["CLIENT_IMAGES"] + image_name)
		image_binary = read_image(image_name)
		response = make_response(image_binary)
		response.headers.set('Content-Type', 'image/jpeg')
    		response.headers.set('Content-Disposition', 'attachment', filename=image_name)
		jsonify(response)
   		return response
		
	except FileNotFoundError:
		response = jsonify(message="FILE_ERROR")
		return response

@app.route("/capture_image")
@cross_origin()
def capture_image():
	print("Capturing image with usb camera at video0")
	cam = cv2.VideoCapture(0)
	ret,frame = cam.read()

	if not ret:
		print("Failed to capture frame")
		reponse = jsonify(message="CAPTURE_ERROR")
		return response

	img_name = "magnifier_image.png"
	cv2.imwrite(img_name, frame)
	print("Image written as {}".format(img_name))

	cam.release() 
	response = jsonify(message="CAPTURE_SUCCESS")
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

