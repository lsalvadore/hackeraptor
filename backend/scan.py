from socket import socket, SOCK_STREAM, SOCK_DGRAM

def scan(args):
    host = args.host
    ports = range(1024)
    for port in ports:
        try:
            s = socket(type=SOCK_STREAM)
            s.connect((host,port))
            print(f"Port {port} is open.")
        except:
            pass
