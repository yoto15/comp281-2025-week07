# import ส่วนของ flask framework
from flask import Flask, render_template, request, jsonify
import cv2 # OpenCV module
import base64 # base64 ใช้ในการแปลงรหัสกลุ่ม BASE64 string
import numpy as np # numpy ใช้เรื่องโครงสร้างข้อมูลขั้นสูงและทางคณิตศาสตร์

# module ที่เขียนเอง ไฟล์ imgcvt.py
from imgcvt import base64_cvimage, cvimage_base64

# สร้าง Flask app (Flask framework object)
app = Flask(__name__)

# route /
@app.route('/')
def index():
	return render_template('index.html')

# route /workshop01
@app.route('/workshop01')
def workshop01():
	return render_template('workshop01.html')

# route /workshop02
@app.route('/workshop02')
def workshop02():
	return render_template('workshop02.html')

# route /workshop03
@app.route('/workshop03')
def workshop03():
	return render_template('workshop03.html')

########## WORKSHOP01 Image Transfer ##########
# route /wp1_backend
@app.route('/wp1_backend', methods=['POST'])
def wp1_backend():
	"""
	Endpoint to receive image data from the frontend and process it.
	{ imageBASE64, type, width, height }
	"""
	try:
		# รับข้อมูลจาก frontend request
		data = request.get_json()
		if not data:
			return jsonify({'error': 'No data provided'}), 400

		########## รับข้อมูลจาก frontend (request) แล้วแปลงเป็น OpenCV Image ##########
		# แปลงข้อมูล BASE64 ให้เป็น Bytes data เราเรียกว่า RAW Bytes
		img_data = base64.b64decode(data['imageBASE64']) # decode base64 string to image data
		# จัดการ RAW Bytes ให้เป็นโครงสร้าง Byte Array ด้วย numpy
		np_arr = np.frombuffer(img_data, np.uint8) # convert to numpy array (byte array)
		# ให้ OpenCV อ่านข้อมูล Byte Array เป็นภาพ ด้วยคำสั่ง imdecode()
		image_src = cv2.imdecode(np_arr, cv2.IMREAD_COLOR) # decode image data to OpenCV format channel in B G R order

		########## ส่งข้อมูล OpenCV Image กลับไปยัง frontend (response) ##########
		# แปลงข้อมูลภาพตามโครงสร้างของ OpenCV เป็น RAW Bytes ตามตัวอย่างคือ png image format
		_, buffer = cv2.imencode('.png', image_src) # encode the processed image to PNG format
		# แปลง RAW Bytes เป็น BASE64 string
		image_base64 = base64.b64encode(buffer).decode('utf-8') # encode to base64 string

		# สร้าง python dictionary สำหรับ response กลับไปยัง frontend
		output = {
			'message': '',
			'image': {
				"imageBASE64": image_base64,
				"type": 'image/png',
				"width": data["width"],
				"height": data["height"],
			}
		}
		return jsonify(output), 200
	except Exception as e:
		return jsonify({'error': str(e)}), 500

########## WORKSHOP02 Color Space Conversion ##########
# route /wp2_backend
@app.route('/wp2_backend', methods=['POST'])
def wp2_backend():
	"""
	Endpoint to receive image data from the frontend and process it.
	{ imageBASE64, type, width, height }
	"""
	try:
		# รับข้อมูลจาก frontend request
		data = request.get_json()
		if not data:
			return jsonify({'error': 'No data provided'}), 400

		########## รับข้อมูลจาก frontend (request) แล้วแปลงเป็น OpenCV Image ##########
		image_src = base64_cvimage(data['imageBASE64'])

		########## Convert Color-space ##########
		image_output = cv2.cvtColor(image_src, cv2.COLOR_BGR2GRAY)

		########## ส่งข้อมูล OpenCV Image กลับไปยัง frontend (response) ##########
		image_base64 = cvimage_base64(image_output)

		# สร้าง python dictionary สำหรับ response กลับไปยัง frontend
		output = {
			'message': '',
			'image': {
				"imageBASE64": image_base64,
				"type": 'image/png',
				"width": data["width"],
				"height": data["height"],
			}
		}
		return jsonify(output), 200
	except Exception as e:
		return jsonify({'error': str(e)}), 500

########## WORKSHOP03 Image Filtering ##########
# route /wp3_backend
@app.route('/wp3_backend', methods=['POST'])
def wp3_backend():
	"""
	Endpoint to receive image data from the frontend and process it.
	{ imageBASE64, type, width, height }
	"""
	try:
		# รับข้อมูลจาก frontend request
		data = request.get_json()
		if not data:
			return jsonify({'error': 'No data provided'}), 400

		########## รับข้อมูลจาก frontend (request) แล้วแปลงเป็น OpenCV Image ##########
		image_src = base64_cvimage(data['imageBASE64'])

		########## image filtering sample ##########
		# 3 Color channels filter
		# Blur
		#image_output = cv2.blur(image_src, (5,5))
		# Gaussian Blur
		#image_output = cv2.GaussianBlur(image_src, (5, 5), 0)

		# 1 Color channel filter
		# convert to gray
		image_output = cv2.cvtColor(image_src, cv2.COLOR_BGR2GRAY)
		# canny
		#image_output = cv2.Canny(image_output, 150, 110)
		# threshold
		_, image_output = cv2.threshold(image_output, 150, 160, cv2.THRESH_BINARY)

		########## ส่งข้อมูล OpenCV Image กลับไปยัง frontend (response) ##########
		image_base64 = cvimage_base64(image_output)

		# สร้าง python dictionary สำหรับ response กลับไปยัง frontend
		output = {
			'message': '',
			'image': {
				"imageBASE64": image_base64,
				"type": 'image/png',
				"width": data["width"],
				"height": data["height"],
			}
		}
		return jsonify(output), 200
	except Exception as e:
		return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
	app.run(host="0.0.0.0", port=5000, debug=True)