from flask import Flask, render_template, request, send_from_directory
from face_match import match_faces
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
EVENT_PHOTOS_FOLDER = 'static'
MATCHED_FOLDER = 'matches'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(MATCHED_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    matched = []
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filepath = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(filepath)

            matched = match_faces(filepath, EVENT_PHOTOS_FOLDER, MATCHED_FOLDER)
    return render_template('index.html', matched=matched)

@app.route('/matches/<filename>')
def matched_file(filename):
    return send_from_directory(MATCHED_FOLDER, filename)

if __name__ == '__main__':
    app.run(debug=True)
