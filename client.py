import socket
import sys

HOST = 'localhost'
PORT = 5000

def request_file(pathname):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(pathname.encode())
        s.shutdown(socket.SHUT_WR)  # signal end of sending

        response = b''
        while True:
            chunk = s.recv(4096)
            if not chunk:
                break
            response += chunk

    # Parse response
    if response.startswith(b'MATCH\n'):
        content = response[6:]
        print("=== FILE RECEIVED (both servers matched) ===")
        print(content.decode(errors='replace'))

    elif response.startswith(b'DIFFER\n'):
        data = response[7:]
        s1_len = int.from_bytes(data[:4], 'big')
        s1_content = data[4:4 + s1_len]
        s2_content = data[4 + s1_len:]
        print("=== FILE FROM SERVER1 ===")
        print(s1_content.decode(errors='replace'))
        print("=== FILE FROM SERVER2 ===")
        print(s2_content.decode(errors='replace'))

    elif response.startswith(b'FOUND\n'):
        content = response[6:]
        print("=== FILE RECEIVED (from one server) ===")
        print(content.decode(errors='replace'))

    elif response == b'NOT_FOUND':
        print("File not found on any server.")

    else:
        print("Unknown response received.")

if __name__ == '__main__':
    pathname = input("Enter file pathname: ")
    request_file(pathname)