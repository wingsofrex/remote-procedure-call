import socket
import os

HOST = 'localhost'
PORT = 5000
FILE_DIR = 'server1_files'

SERVER2_HOST = 'localhost'
SERVER2_PORT = 6000

def query_server2(pathname):
    """Ask SERVER2 for a file. Returns content (bytes) or None."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((SERVER2_HOST, SERVER2_PORT))
        s.sendall(pathname.encode())
        response = b''
        while True:
            chunk = s.recv(4096)
            if not chunk:
                break
            response += chunk

    if response.startswith(b'FOUND\n'):
        return response[6:]  # strip the 'FOUND\n' prefix
    return None

def handle_client(conn):
    pathname = conn.recv(1024).decode().strip()
    print(f"SERVER1 received request for: {pathname}")

    filepath = os.path.join(FILE_DIR, pathname)

    # Check SERVER1's own files
    s1_content = None
    if os.path.exists(filepath):
        with open(filepath, 'rb') as f:
            s1_content = f.read()

    # Check SERVER2
    s2_content = query_server2(pathname)

    # Decision logic
    if s1_content is not None and s2_content is not None:
        if s1_content == s2_content:
            print("Files match. Sending one copy to CLIENT.")
            conn.sendall(b'MATCH\n' + s1_content)
        else:
            print("Files differ. Sending both to CLIENT.")
            s1_len = len(s1_content).to_bytes(4, 'big')
            conn.sendall(b'DIFFER\n' + s1_len + s1_content + s2_content)

    elif s1_content is not None:
        print("File only on SERVER1. Sending to CLIENT.")
        conn.sendall(b'FOUND\n' + s1_content)

    elif s2_content is not None:
        print("File only on SERVER2. Sending to CLIENT.")
        conn.sendall(b'FOUND\n' + s2_content)

    else:
        print("File not found on either server.")
        conn.sendall(b'NOT_FOUND')

    conn.close()

def start():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"SERVER1 listening on port {PORT}...")
        while True:
            conn, addr = s.accept()
            handle_client(conn)

if __name__ == '__main__':
    start()