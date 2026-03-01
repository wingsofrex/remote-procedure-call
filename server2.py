import socket
import os

HOST = 'localhost'
PORT = 6000
FILE_DIR = 'server2_files'

def handle_request(conn):
    pathname = conn.recv(1024).decode()
    filepath = os.path.join(FILE_DIR, pathname)

    if os.path.exists(filepath):
        with open(filepath, 'rb') as f:
            content = f.read()
        conn.sendall(b'FOUND\n' + content)
    else:
        conn.sendall(b'NOT_FOUND')

    conn.close()

def start():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"SERVER2 listening on port {PORT}...")
        while True:
            conn, addr = s.accept()
            handle_request(conn)

if __name__ == '__main__':
    start()