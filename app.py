import os
from flask import Flask, request, render_template
from stegano import encode_spread_spectrum, decode_spread_spectrum
import cv2
import traceback

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024  # Maks 2MB
UPLOAD_FOLDER = 'static/uploads'
RESULT_FOLDER = 'static/results'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/encode', methods=['POST'])
def encode():
    try:
        image = request.files.get('image')
        message = request.form.get('message')

        if not image or not message:
            return "❌ Upload gambar dan pesan wajib diisi", 400

        image_path = os.path.join(UPLOAD_FOLDER, image.filename)
        image.save(image_path)

        print(f"📤 Gambar diterima: {image.filename}")
        encoded_image = encode_spread_spectrum(image_path, message)
        encoded_path = os.path.join(RESULT_FOLDER, 'encoded.png')
        cv2.imwrite(encoded_path, encoded_image)

        os.remove(image_path)

        return render_template('index.html', encoded_image=encoded_path)
    except Exception as e:
        traceback.print_exc()
        return "❌ Terjadi kesalahan saat encoding.", 500

@app.route('/decode', methods=['POST'])
def decode():
    try:
        original = request.files.get('original')
        stego = request.files.get('stego')
        length_raw = request.form.get('length')

        if not original or not stego or not length_raw:
            return "❌ Semua field harus diisi", 400
        if not length_raw.isdigit():
            return "❌ Panjang pesan harus berupa angka", 400

        length = int(length_raw)

        original_path = os.path.join(UPLOAD_FOLDER, original.filename)
        stego_path = os.path.join(UPLOAD_FOLDER, stego.filename)
        original.save(original_path)
        stego.save(stego_path)

        print(f"🧪 Decode dimulai: {original.filename} dan {stego.filename} dengan panjang {length}")
        message = decode_spread_spectrum(original_path, stego_path, length)

        os.remove(original_path)
        os.remove(stego_path)

        return render_template('index.html', decoded_message=message)
    except Exception as e:
        traceback.print_exc()
        return "❌ Terjadi kesalahan saat decoding.", 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
