from bottle import static_file, run, template, request, Bottle
import os
from pathlib import Path

app = Bottle()
home:Path = Path.home()
safe_location = home.join("server", "temp_data")

@app.route('/')
@app.route('/hello')
def ind():
    return r'Nothing here :/'

@app.route('/hello/<name>')
def index(name):
    return template('<b>Hello {{name}}</b>!', name=name)

@app.get('/gps/simple')
def get_a_map():
    return None

@app.post('/gps/simple')
def give_a_route():
    return None

@app.get('/gps/detailed')
def get_a_detailed_map():
    return None

@app.post('/gps/detailed')
def give_a_detailed_route():
    return None

@app.route('/gps/<filename:path>')
def send_static(filename):
    return static_file(filename, root='/path/to/static/files')

@app.route('/upload', method='POST')
def do_upload():
    category   = request.forms.get('category')
    upload     = request.files.get('upload')
    name, ext = os.path.splitext(upload.filename)
    if ext not in ('.csv'):
        return 'File extension not allowed.'

    save_path = safe_location.join(name)
    upload.save(save_path) # appends upload.filename automatically
    return 'OK'

run(app, host='localhost', port=21812)