from flask import Flask, abort, render_template, redirect, url_for, flash, jsonify, request
from flask_bootstrap import Bootstrap5
import numpy as np
from PIL import Image
from werkzeug.utils import secure_filename
import os

extensions = ['JPEG', 'PNG', 'GIF', 'BMP', 'JPG', 'WEBP']
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('FLASK_KEY')
app.config['UPLOAD_FOLDER'] = 'static'


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].upper() in extensions


def find_image(file_name, path):
    for root, dirs, files in os.walk(path):
        if file_name in files:
            return os.path.join(root, file_name)


def find_colors(image):
    colors = []
    unqc, c = np.unique(image.reshape(-1, image.shape[-1]), axis=0, return_counts=True)
    top10 = np.argpartition(c, -10)[-10:]
    for color in unqc[top10]:
        new_color = f"rgb({color[0]},{color[1]},{color[2]})"
        colors.append(new_color)
    return colors


@app.route('/', methods=['POST', 'GET'])
def main_page():
    if request.method == 'POST':
        file = request.files['file']
        if file.filename == '':
            flash('No file')
            return render_template('index.html', show=False)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            image = Image.open(f'static/{filename}')
            image_array = np.array(image)
            return render_template('index.html', file=filename, show=True, colors=find_colors(image_array))
        else:
            flash('Wrong file extension')
            return render_template('index.html', show=False)
    return render_template('index.html', show=False)


if __name__ == '__main__':
    app.run(debug=True)
