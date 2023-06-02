from datetime import date

from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB maximum file size
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'csv', 'py', 'java', 'ipynb', 'pkl', 'doc', 'docx', 'xlsx', 'ppt', 'mp3', 'mp4'}

class UploadForm(FlaskForm):
    files = FileField('Upload Files', validators=[FileRequired(), FileAllowed(app.config['ALLOWED_EXTENSIONS'])], render_kw={'multiple': True})

def create_upload_folder():
    today = date.today().strftime("%Y-%m-%d")
    folder_path = os.path.join(app.config['UPLOAD_FOLDER'], today)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    return folder_path

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    form = UploadForm()
    if form.validate_on_submit():
        folder_path = create_upload_folder()
        files = request.files.getlist('files')
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(folder_path, filename))
        return redirect(url_for('upload_success'))
    return render_template('uploads_form.html', form=form)

@app.route('/success')
def upload_success():
    return 'Files uploaded successfully!'

if __name__ == '__main__':
    app.run(debug=True)
