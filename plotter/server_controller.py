"""Random python program"""
import platform
import server.server  as serv

if __name__ == "__main__":
    print("Hello World!")
    print("Starting Server!")
    if platform.system() == "Windows":
        tile_server = serv.start(windows=True)
    else:
        tile_server = serv.start(windows=False)