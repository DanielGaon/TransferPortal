import os
from flask import Flask, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
import subprocess

app = Flask("Transfer")

UPLOAD_FOLDER = 'uploads'
#SCANNED_FOLDER = 'scanned' - for futre use to scan the files
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'zip', 'xlsx', 'docx'}

# Ensures directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
#os.makedirs(SCANNED_FOLDER, exist_ok=True) for futre use to scan the files 

# Set config
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#Configures Favicon
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, 'static'),
        'favicon.ico',
        mimetype='image/vnd.microsoft.icon')

#Main page
@app.route("/")
def main_page():
    result = {'messege':"Welcome to Altshare-File Transfer Portal"}
    return result

#This function checks whether a given filename is allowed based on its file extension 
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#Uploads a file
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in request'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        return jsonify({'message': 'File uploaded (no scan)', 'filename': filename}), 200

    return jsonify({'error': 'File type not allowed'}), 400

#Gets the list of uploaded files
@app.route('/files', methods=['GET'])
def list_files():
    files = os.listdir(UPLOAD_FOLDER)
    return jsonify({'uploaded_files': files})

#Deletes a specific file
@app.route('/files/<name>', methods=['DELETE'])
def delete_file(name):
    filepath = os.path.join(UPLOAD_FOLDER, secure_filename(name))
    
    if os.path.exists(filepath):
        os.remove(filepath)
        return jsonify({'message': f'{name} deleted successfully'}), 200
    else:
        return jsonify({'error': 'File not found'}), 404
    
#Opens the file    
@app.route('/files/<name>', methods=['GET'])
def get_file(name):
    safe_name = secure_filename(name)
    filepath = os.path.join(UPLOAD_FOLDER, safe_name)

    if os.path.exists(filepath):
        return send_from_directory(UPLOAD_FOLDER, safe_name, as_attachment=False)
    else:
        return jsonify({'error': 'File not found'}), 404

app.run('0.0.0.0',8080)