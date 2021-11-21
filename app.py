# code written by Nicholas Rosato
# server.py
# EPICS magnifier flask server
# last updated 11/17/2021

from flask import Flask, jsonify
from flask_cors import CORS, cross_origin
from base64 import encodebytes
from PIL import Image
import os
import cv2
import io



app = Flask(__name__)
CORS(app)
app.config["CLIENT_IMAGES"] = "/home/pi/Desktop/server/"
app.config['CORS_HEADERS'] = 'Content-Type'
image_name = "magnifier_image.png"


def get_response_image(image_path):
	pil_img = Image.open(image_path, mode='r') # reads the PIL image
	byte_arr = io.BytesIO()
	pil_img.save(byte_arr, format='PNG') # convert the PIL image to byte array
	encoded_img = encodebytes(byte_arr.getvalue()).decode('ascii') # encode as base64
	return encoded_img

@app.route("/get_image")
@cross_origin()
def get_image():
	print("Getting Image from directory- " + app.config["CLIENT_IMAGES"])
	# invoke rpi to take image with usb camera
	# save usb image to img send_from_directory
	# encode image into base64 and send to device via the request
	try:
		print(app.config["CLIENT_IMAGES"] + image_name)
		encoded_img = get_response_image(image_name)
		return jsonify(response) # send the result to client
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

