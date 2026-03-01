from flask import Flask, request, render_template
import socket

app = Flask(__name__)

HOST = 'localhost'
PORT = 5000

def request_file(pathname):
    """Reuses the same socket logic from client.py"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(pathname.encode())
        s.shutdown(socket.SHUT_WR)

        response = b''
        while True:
            chunk = s.recv(4096)
            if not chunk:
                break
            response += chunk

    if response.startswith(b'MATCH\n'):
        content = response[6:]
        return {
            'status': 'MATCH',
            'message': 'Both servers returned consistent replicas.',
            'file1': content.decode(errors='replace')
        }

    elif response.startswith(b'FOUND\n'):
        content = response[6:]
        return {
            'status': 'FOUND',
            'message': 'File retrieved from one server.',
            'file1': content.decode(errors='replace')
        }

    elif response == b'NOT_FOUND':
        return {
            'status': 'NOT_FOUND',
            'message': 'File not found on any server.',
            'file1': None
        }

    else:
        return {
            'status': 'ERROR',
            'message': 'Unknown response from SERVER1.',
            'file1': None
        }

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        pathname = request.form.get('pathname', '').strip()
        if pathname:
            result = request_file(pathname)
    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True, port=8000)