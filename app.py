import os
from flask import Flask, request, render_template, send_file
from stegano import encode_spread_spectrum, decode_spread_spectrum
import cv2

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
RESULT_FOLDER = 'static/results'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/encode', methods=['POST'])
def encode():
    image = request.files['image']
    message = request.form['message']
    image_path = os.path.join(UPLOAD_FOLDER, image.filename)
    image.save(image_path)

    encoded_image = encode_spread_spectrum(image_path, message)
    encoded_path = os.path.join(RESULT_FOLDER, 'encoded.png')
    cv2.imwrite(encoded_path, encoded_image)

    return render_template('index.html', encoded_image=encoded_path)

@app.route('/decode', methods=['POST'])
def decode():
    original = request.files['original']
    stego = request.files['stego']
    length = int(request.form['length'])

    original_path = os.path.join(UPLOAD_FOLDER, original.filename)
    stego_path = os.path.join(UPLOAD_FOLDER, stego.filename)
    original.save(original_path)
    stego.save(stego_path)

    message = decode_spread_spectrum(original_path, stego_path, length)

    return render_template('index.html', decoded_message=message)

if __name__ == '__main__':
    app.run(debug=True)
