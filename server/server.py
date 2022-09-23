import logging
from bottle import static_file, run, template, request, Bottle
import os
from pathlib import Path

app = Bottle()
home:Path = Path.home()
safe_location = home.joinpath("server", "temp_data")

@app.route('/')
@app.route('/hello')
def ind():
    return r'Nothing here :/'

@app.route('/hello/<name>')
def index(name):
    return template('<b>Hello {{name}}</b>!', name=name)

@app.route('/gps/simple', method='GET')
def get_a_map():
    return """<form action="/gps/simple" method="post" enctype="multipart/form-data">
                Select a file: <input type="file" name="upload" />
                <input type="submit" value="Start upload" />
                </form>"""

@app.route('/gps/<filename:path>')
def send_static(filename):
    return static_file(filename, root='/path/to/static/files')


@app.route('/gps/simple', method='POST')
def do_upload():
    upload     = request.files.get('upload')
    name, ext = os.path.splitext(upload.filename)
    if ext != '.csv':
        return 'File extension not allowed.'
    save_path = safe_location.joinpath(name).resolve().as_uri
    upload.save(save_path) # appends upload.filename automatically
    test = safe_location.resolve().as_uri
    return "OK"

run(app, host='localhost', port=21812)