# code written by Nicholas Rosato
# server.py
# EPICS magnifier flask server
# last updated 11/17/2021

from flask import Flask
import os
import cv2
import base64

app = Flask(__name__)
app.config["CLIENT_IMAGES"] = "/home/pi/Desktop/server/"

@app.route("/get_image")
def get_image():
	print("Getting Image from directory- " + app.config["CLIENT_IMAGES"])
	# invoke rpi to take image with usb camera
	# save usb image to img send_from_directory
	# encode image into base64 and send to device via the request
	try:
		print(app.config["CLIENT_IMAGES"] + "magnifier_image.png")
		image_file = open(app.config["CLIENT_IMAGES"] + image_name, "rb")
		encoded_string = base64.b64encode(image_file.read())
		return encoded_string
	except FileNotFoundError:
		return "FILE_ERROR"

@app.route("/capture_image")
def capture_image():
	print("Capturing image with usb camera at video0")
	cam = cv2.VideoCapture(0)
	ret,frame = cam.read()

	if not ret:
		print("Failed to capture frame")
		return "CAPTURE_ERROR"

	img_name = "magnifier_image.png"
	cv2.imwrite(img_name, frame)
	print("Image written as {}".format(img_name))

	cam.release() 
	return "CAPTURE_SUCCESS"

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
