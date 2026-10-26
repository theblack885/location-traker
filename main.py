import webview
import threading
import http.server
import socketserver
import os
import sys

def resource_path(rel_path):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, rel_path)
    return os.path.join(os.path.abspath("."), rel_path)

def start_server(port):
    os.chdir(resource_path("."))
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("127.0.0.1", port), handler) as httpd:
        httpd.serve_forever()

if __name__ == "__main__":
    PORT = 8743
    t = threading.Thread(target=start_server, args=(PORT,), daemon=True)
    t.start()

    window = webview.create_window(
        "Location Tracker - Viewer",
        f"http://127.0.0.1:{PORT}/viewer.html",
        width=480,
        height=820,
        resizable=True,
        background_color="#070712"
    )
    webview.start()
