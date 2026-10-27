import webview
import threading
import http.server
import socketserver
import os
import sys
import time

def resource_path(rel_path):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, rel_path)
    return os.path.join(os.path.abspath("."), rel_path)

class ReusableServer(socketserver.TCPServer):
    allow_reuse_address = True

def find_free_port():
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("127.0.0.1", 0))
    port = s.getsockname()[1]
    s.close()
    return port

def start_server(port):
    os.chdir(resource_path("."))
    handler = http.server.SimpleHTTPRequestHandler
    with ReusableServer(("127.0.0.1", port), handler) as httpd:
        httpd.serve_forever()

if __name__ == "__main__":
    PORT = find_free_port()
    t = threading.Thread(target=start_server, args=(PORT,), daemon=True)
    t.start()
    time.sleep(0.5)

    cache_bust = int(time.time())
    window = webview.create_window(
        "Location Tracker",
        f"http://127.0.0.1:{PORT}/app.html?v={cache_bust}",
        width=460,
        height=840,
        resizable=True,
        background_color="#070712"
    )
    webview.start()
