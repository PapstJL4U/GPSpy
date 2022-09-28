from bottle import static_file, run, template, request, Bottle
import os, logging
if __name__ == '__main__':
    import server_logic as sl
else:
    import server.server_logic as sl

app = Bottle()
home:str = os.getcwd()
safe_location:str = os.path.join(home,"plotter", "server", "temp_data")
logging.basicConfig(filename='server.log', encoding='utf-8', level=logging.INFO)
logger = logging.getLogger(name="server")

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

@app.route('/gps/complex', method='GET')
def get_a_map():
    return """<form action="/gps/complex" method="post" enctype="multipart/form-data">
                Select a file: <input type="file" name="upload" />
                <input type="submit" value="Start upload" />
                </form>"""

@app.route('/static/<filename:path>')
def send_static(filename):
    return static_file(filename, root=safe_location)


@app.route('/gps/simple', method='POST')
def do_upload():
    logger.debug("Processing gps for simple map")
    upload     = request.files.get('upload')
    name, ext = os.path.splitext(upload.filename)
    if ext != '.csv':
        return 'File extension not allowed.'

    save_path = os.path.join(safe_location,name+'.csv')

    logger.info("File uploaded: "+save_path)
    upload.save(save_path, overwrite=True) # appends upload.filename automatically
    image:str = process_gps(save_path, simple=True)
    
    file = image.split("/")[-1]
    logger.info("Returned file: "+file)
    return send_static(file)

@app.route('/gps/complex', method='POST')
def do_upload():
    logger.debug("Processing gps for complex map")
    upload     = request.files.get('upload')
    name, ext = os.path.splitext(upload.filename)
    if ext != '.csv':
        return 'File extension not allowed.'

    save_path = os.path.join(safe_location,name+'.csv')

    logger.info("File uploaded: "+save_path)
    upload.save(save_path, overwrite=True) # appends upload.filename automatically
    image:str = process_gps(save_path, simple=False)
    
    file = image.split("\\")[-1]
    logger.info("Returned file: "+file)
    cleanup()
    return send_static(file)

def process_gps(path_to_gps_file:str="/", simple:bool=True)->str:
    #remove suffix to alter name later
    file = path_to_gps_file.removesuffix(".csv")

    if simple:
        image:str = sl.single_tile_gps(file)
    else:
        image.str = sl.multi_tile_gps(file)
    
    return image

def cleanup():
    logger.info("Deleting unneeded files...")
    for file in os.listdir(safe_location):
        if file.endswith('.csv'):
            os.remove(file)
        if file.endswith('.png') and "final" not in file:
            os.remove(file)

def start():
    run(app, host='localhost', port=21812)
    logger.info("Current Working Directory: "+os.getcwd())

if __name__ == '__main__':
    start()