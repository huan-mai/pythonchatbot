import os
from flask import flash, request, redirect, url_for

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in 'json'
def upload_file(request):
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            raise Exception('No file part')
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            raise Exception('No selected file')
        if file and allowed_file(file.filename):
            file.save(os.path.join('.', file.filename))
            return file.filename