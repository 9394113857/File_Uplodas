import os
import logging
import datetime

from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB maximum file size
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'csv', 'py', 'java', 'ipynb', 'pkl', 'doc', 'docx', 'xlsx', 'ppt', 'mp3', 'mp4'}

logs_folder = 'logs'

class UploadForm(FlaskForm):
    files = FileField('Upload Files', validators=[FileRequired(), FileAllowed(app.config['ALLOWED_EXTENSIONS'])], render_kw={'multiple': True})

def create_upload_folder():
    today = datetime.date.today().strftime("%Y-%m-%d")
    folder_path = os.path.join(app.config['UPLOAD_FOLDER'], today)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    return folder_path

def create_logs_folder():
    today = datetime.date.today().strftime("%Y-%m-%d")
    logs_path = os.path.join(logs_folder, today)
    if not os.path.exists(logs_path):
        os.makedirs(logs_path)
    return logs_path

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def write_to_log(log_file, message):
    log_file = get_log_file_with_date(log_file)
    logging.basicConfig(filename=log_file, level=logging.INFO)
    logging.info(message)

def get_log_file_with_date(log_file):
    today = datetime.date.today().strftime("%Y-%m-%d")
    if not os.path.exists(log_file):
        log_file = log_file.replace('log.txt', f"log_{today}.txt")
    return log_file

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    form = UploadForm()
    if form.validate_on_submit():
        folder_path = create_upload_folder()
        logs_path = create_logs_folder()
        files = request.files.getlist('files')
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(folder_path, filename))
                log_file = os.path.join(logs_path, 'log.txt')
                log_message = f"Uploaded file: {filename}"
                write_to_log(log_file, log_message)
        return redirect(url_for('upload_success'))
    return render_template('upload_files_dates.html', form=form)

@app.route('/success')
def upload_success():
    return 'Files uploaded successfully!'

if __name__ == '__main__':
    app.run(debug=True)
