import http.server
import socketserver
import os

PORT = 10800
keyframeloc = "./preproc_fallDown/keyframes"

Handler = http.server.SimpleHTTPRequestHandler
httpd = socketserver.TCPServer(("", PORT), Handler)
httpd.serve_forever()
