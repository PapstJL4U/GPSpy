from bottle import static_file, run, template, request, Bottle
import os, logging
if __name__ == '__main__':
    import server_logic as sl
else:
    import server.server_logic as sl

app = Bottle()
home:str = os.getcwd()
safe_location:str = os.path.join(home,"plotter", "server", "temp_data")
logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.INFO)
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

@app.route('/gps/<filename:path>')
def send_static(filename):
    return static_file(filename, root= os.path.join(safe_location, filename))


@app.route('/gps/simple', method='POST')
def do_upload():
    upload     = request.files.get('upload')
    name, ext = os.path.splitext(upload.filename)
    if ext != '.csv':
        return 'File extension not allowed.'
    #save_path = safe_location.joinpath(name).resolve().stem
    save_path = os.path.join(safe_location,name+'.csv')
    print(os.getcwd(), save_path)
    logger.info("OS: "+os.getcwd())
    logger.info("Save path: "+save_path)
    upload.save(save_path) # appends upload.filename automatically
    process_gps_simple(save_path)

    return "OK"

def process_gps_simple(path_to_gps_file:str="/")->None:
    
    #plot a path within a single tile
    #remove suffix to alter name later
    file = path_to_gps_file.removesuffix(".png")
    image = sl.single_tile_gps(path_to_gps_file)

def start():
    run(app, host='localhost', port=21812)

if __name__ == '__main__':
    start()