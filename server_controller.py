"""Random python program"""
import server.server  as serv

if __name__ == "__main__":
    print("Hello World!")
    print("Starting Server!")
    
    s = serv.server();
    s.start();