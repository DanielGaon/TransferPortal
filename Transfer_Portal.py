import os
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import subprocess

app = Flask("Transfer")

UPLOAD_FOLDER = 'uploads'
SCANNED_FOLDER = 'scanned'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'zip', 'xlsx', 'docx'}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(SCANNED_FOLDER, exist_ok=True)

@app.route("/")
def main_error():
    result = {'msg':"root endpoint not supported"}
    return result

#This function checks whether a given filename is allowed based on its file extension 
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def scan_with_defender(file_path):
    defender_path = r"C:\ProgramData\Microsoft\Windows Defender\Platform\4.18.25060.7-0"
    latest_dir = sorted(os.listdir(defender_path))[-1]
    full_cmd = os.path.join(defender_path, latest_dir, "MpCmdRun.exe")
    command = [full_cmd, "-Scan", "-ScanType", "3", "-File", file_path]

    result = subprocess.run(command, capture_output=True, text=True)
    output = result.stdout
    return "Threats Detected" not in output, output

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

        clean, scan_output = scan_with_defender(filepath)

        if clean:
            os.rename(filepath, os.path.join(SCANNED_FOLDER, filename))
            return jsonify({'message': 'File uploaded and clean', 'filename': filename}), 200
        else:
            os.remove(filepath)
            return jsonify({'message': 'File infected and deleted', 'scan_result': scan_output}), 400

    return jsonify({'error': 'File type not allowed'}), 400

#Returns a list of filenames in that folder that have already been scanned and uploaded successfully
@app.route('/files', methods=['GET'])
def list_files():
    files = os.listdir(SCANNED_FOLDER)
    return jsonify({'scanned_files': files})

app.run('0.0.0.0',8080)