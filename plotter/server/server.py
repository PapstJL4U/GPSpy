from bottle import static_file, run, template, request, Bottle
import os, shutil, logging

if __name__ == "__main__":
    import server_logic as sl
else:
    import server.server_logic as sl

app = Bottle()
home: str = os.getcwd()
save_location: str = os.path.join(home, "temp_data")

logging.basicConfig(filename="server.log", encoding="utf-8", level=logging.INFO)
logger = logging.getLogger(name="server")
logger.info("CWD: " + home)
logger.info("SL:" + save_location)


@app.route("/")
@app.route("/hello")
def ind():
    return r"Nothing here :/"


@app.route("/hello/<name>")
def index(name):
    return template("<b>Hello {{name}}</b>!", name=name)


@app.route("/gps/simple", method="GET")
def get_a_map():
    """This is the upload form for the simple gps map"""
    # delete all previous files to avoid copy and redundancy conflicts
    cleanup(all=True)
    return """<form action="/gps/simple" method="post" enctype="multipart/form-data">
                Select a file: <input type="file" name="upload" />
                <input type="submit" value="Start upload" />
                </form>"""


@app.route("/gps/complex", method="GET")
def get_a_map():
    """This is the form for the more complex gps map"""
    # delete all previous files to avoid copy and redundancy conflicts
    cleanup(all=True)
    return """<form action="/gps/complex" method="post" enctype="multipart/form-data">
                Select a file: <input type="file" name="upload" />
                <input type="submit" value="Start upload" />
                </form>"""


@app.route("/static/<filename:path>")
def send_static(filename):
    """Return the final gps map with a download request."""
    return static_file(filename, root=save_location)


@app.route("/gps/simple", method="POST")
def do_upload():
    """The method used to display gps data in a single tile map."""
    logger.info("Processing gps for simple map")

    # retrieves exact file path to gps file
    save_path = all_upload()
    # get final image
    image: str = process_gps(save_path, simple=True)

    #
    file = os.path.basename(image)
    logger.info("Returned file: " + file)
    # delete intermediate files
    cleanup(all=False)
    return send_static(file)


@app.route("/gps/complex", method="POST")
def do_upload():
    """The method used to display gps data with the maximum zoom level on multiple tiles"""
    logger.info("Processing gps for complex map")

    # retrieves exact file path to gps file
    save_path = all_upload()
    # get final image
    image: str = process_gps(save_path, simple=False)

    # move image from subfolder to parent folder, so we can delete subfilder
    file = os.path.basename(shutil.copy(image, (save_location)))
    logger.info("Returned file: " + file)
    # delete subfolder with tiles and intermediate images
    cleanup(all=False)
    return send_static(file)


def all_upload():
    """This method handles all logic, that complex and simple gps have in common."""
    # requests the users uploaded file
    upload = request.files.get("upload")
    name, ext = os.path.splitext(upload.filename)
    if ext != ".csv":
        return "File extension not allowed."

    # find path to file
    save_path = os.path.join(save_location, name + ".csv")
    # make a directory if we need it for complex gps
    os.makedirs(os.path.join(save_location, name), exist_ok=True)

    logger.info("File uploaded: " + save_path)
    logger.info("Directoy created: " + os.path.join(save_location, name))

    # safes the uploaded file to local
    upload.save(save_path, overwrite=True)

    return save_path


def process_gps(path_to_gps_file: str = "/", simple: bool = True) -> str:
    # remove suffix to alter name later
    file = path_to_gps_file.removesuffix(".csv")

    if simple:
        image: str = sl.single_tile_gps(file)
    else:
        image: str = sl.multi_tile_gps(file)

    return image


def cleanup(all=False):
    logger.info("Deleting unneeded files...")
    with os.scandir(save_location) as it:
        for file in it:
            # If we want to return the final image of the gps
            # we only delete unneeded files
            if not all:
                if file.name.endswith(".csv"):
                    # We don't need the gps anymore.
                    logger.info("Deleting file: " + file.name)
                    os.remove(file)
                elif file.name.endswith(".png") and "final" not in file.name:
                    # delete all images, that are not the final version
                    logger.info("Deleting file: " + file.name)
                    os.remove(file)
                else:
                    if file.is_dir():
                        # delete all subfolders, because the final image is always
                        # at the top directory
                        logger.info("Deleting folder: " + file.name)
                        shutil.rmtree(file)
            else:
                # remove everything for a clean space
                logger.info("Deleting: " + file.name)
                os.remove(file)


def start(windows: bool = False):

    if windows:
        run(app, host="localhost", port=21812)
    else:
        # We guess we are in a docker container
        run(app, host="0.0.0.0", port=21812)

    logger.info("Current Working Directory: " + os.getcwd())
    logger.info("Save Location: " + save_location)
