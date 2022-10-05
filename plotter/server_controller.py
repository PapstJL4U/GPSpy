"""Random python program"""
import platform
import server.server  as serv

if __name__ == "__main__":
    print("Hello World!")
    print("Starting Server!")
    tile_server = serv.start(windows=True)
