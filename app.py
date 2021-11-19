# code written by Nicholas Rosato
# server.py
# EPICS magnifier flask server
# last updated 11/17/2021

from flask import Flask, jsonify
import os
import cv2
import base64

app = Flask(__name__)
app.config["CLIENT_IMAGES"] = "/home/pi/Desktop/server/"
image_name = "magnifier_image.png"

@app.route("/get_image")
def get_image():
	print("Getting Image from directory- " + app.config["CLIENT_IMAGES"])
	# invoke rpi to take image with usb camera
	# save usb image to img send_from_directory
	# encode image into base64 and send to device via the request
	try:
		print(app.config["CLIENT_IMAGES"] + image_name)
		image_file = open(app.config["CLIENT_IMAGES"] + image_name, "rb")
		encoded_string = base64.b64encode(image_file.read())
		response = jsonify(message=encoded_string)
		response.headers.add("Access-Control-Allow-Origin", "*") 
		return response
	except FileNotFoundError:
		response = jsonify(message="FILE_ERROR")
		response.headers.add("Access-Control-Allow-Origin", "*") 
		return response

@app.route("/capture_image")
def capture_image():
	print("Capturing image with usb camera at video0")
	cam = cv2.VideoCapture(0)
	ret,frame = cam.read()

	if not ret:
		print("Failed to capture frame")
		reponse = jsonify(message="CAPTURE_ERROR")
		response.headers.add("Access-Control-Allow-Origin", "*") 
		return response

	img_name = "magnifier_image.png"
	cv2.imwrite(img_name, frame)
	print("Image written as {}".format(img_name))

	cam.release() 
	response = jsonify(message="CAPTURE_SUCCESS")
	response.headers.add("Access-Control-Allow-Origin", "*") 
	return response

@app.route("/start_motion")
def start_motion():
	print("Starting motion video server...")
	os.system("sudo service motion start")
	response = jsonify(message="MOTION_START")
	response.headers.add("Access-Control-Allow-Origin", "*") 
	return response

@app.route("/stop_motion")
def stop_motion():
	print("Stopping motion video server...")
	os.system("sudo service motion stop")
	response = jsonify(message="MOTION_STOP")
	response.headers.add("Access-Control-Allow-Origin", "*") 
	return response


@app.route("/")
def index():
	response = jsonify(message="INDEX")
	response.headers.add("Access-Control-Allow-Origin", "*") 
	return response

