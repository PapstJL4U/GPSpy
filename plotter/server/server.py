from bottle import static_file, run, template, request, Bottle
import os
import server_main as main
import pandas as pd

app = Bottle()
home = os.getcwd()
safe_location = os.path.join("server", "temp_data")

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
    upload.save(save_path) # appends upload.filename automatically
    process_gps_simple(save_path)

    return "OK"

def process_gps_simple(path_to_gps_file:str="/")->None:
    
    df = pd.read_csv(path_to_gps_file, sep=',')
    only_location = tuple(zip(df['lat'],df['lon']))
    unique_tiles = main.detailed_tiles(only_location, zoom=15)
    #download all tiles if not yet downloaded
    main.load_all_tiles(unique_tiles, zoom=15)
    
    #plot a path within a single tile
    #remove suffix to alter name later
    file = path_to_gps_file.removesuffix(".png")
    main.plot_my_path(file,only_location, df)


run(app, host='localhost', port=21812)