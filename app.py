import os

from flask import Flask, render_template, request
from steganography import create_image, decode_image

UPLOAD_FOLDER = os.path.join('static/images')
ALLOWED_EXTENSIONS = {'png'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if os.path.exists(app.config['UPLOAD_FOLDER']) is False:
    os.mkdir(app.config['UPLOAD_FOLDER'])


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/encode', methods=['GET', 'POST'])
def encode():
    if request.method == 'POST':

        # LOADING AND SAVING IMAGE
        if 'image' not in request.files:
            return 'there is no image in form!'
        image = request.files['image']
        path = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)

        # delete cached file
        if os.path.isfile(path):
            os.remove(path)

        image.save(path)

        # STEGANOGRAPHY

        secret_message = request.form['secret_message']
        print('secret message:', secret_message)
        base_image_path = path
        create_image(secret_message, base_image_path)

        return render_template('result_encode.html', img_path=base_image_path)

    return render_template('encode.html')


@app.route('/decode', methods=['GET', 'POST'])
def decode():

    if request.method == 'POST':

        # LOADING AND SAVING IMAGE
        if 'image' not in request.files:
            return 'there is no image in form!'
        image = request.files['image']
        path = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
        image.save(path)

        # STEGANOGRAPHY

        secret = decode_image(path)
        return render_template('result_decode.html', secret=secret)

    return render_template('decode.html')


if __name__ == '__main__':
    app.run()
