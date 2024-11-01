# -*- coding: utf-8 -*-
from flask import Flask, request, redirect, url_for, send_from_directory, render_template
from flask_httpauth import HTTPBasicAuth
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 10240000 * 10240000  # 16 MB, kann angepasst werden
auth = HTTPBasicAuth()

# Beispiel-Benutzerdaten
USERS = {
    "user": "password",  # Du kannst diese Daten ändern oder aus einer sichereren Quelle laden
}

@auth.get_password
def get_pw(username):
    if username in USERS:
        return USERS.get(username)
    return None


app_env = os.getenv("test")
print(app_env
)
UPLOAD_FOLDER = 'uploads'

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
@auth.login_required
def index():
    files = os.listdir(UPLOAD_FOLDER)
    return render_template('index.html', files=files)

@app.route('/', methods=['POST'])
@auth.login_required
def upload_file():
    if 'files' not in request.files:
        return redirect(request.url)
    files = request.files.getlist('files')
    for file in files:
        if file.filename == '':
            continue
        filename = secure_filename(file.filename)
        file.save(os.path.join(UPLOAD_FOLDER, filename))
    return redirect(url_for('index'))

@app.route('/uploads/<filename>')
@auth.login_required
def download_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)

@app.route('/delete/<filename>', methods=['DELETE'])
@auth.login_required
def delete_file(filename):
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        return '', 204  # No Content status code
    return '', 404  # Not Found status code

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
