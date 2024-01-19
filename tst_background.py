# Define the HTTP request handler class
from http.server import BaseHTTPRequestHandler, HTTPServer

from tst_background2 import create_task


class MyHandler(BaseHTTPRequestHandler):

    @staticmethod
    def start():
        # Define the server's IP address and port
        server_address = ('', 8000)
        # Create an HTTP server with the defined address and request handler
        httpd = HTTPServer(server_address, MyHandler)
        # Start the server
        print("Server running on http://localhost:8000")
        httpd.serve_forever()

    # Function to process background operations

    def do_POST(self):
        pass

    # Handle GET requests
    def do_GET(self):
        # Send response status code
        if self.path == '/favicon.ico2':
            self.send_response(200)
            self.send_header('Content-Type', 'image/x-icon')
            self.send_header('Content-Length', 0)
            self.end_headers()
            return
        if self.path == '/favicon.ico':
            self.send_response(200)
            self.send_header('Content-Type', 'image/x-icon')
            self.end_headers()
            response = ""
            with open('static/favicon.ico', 'rb') as file:
                response = file.read()
            self.wfile.write(response)
            return

        # https: // www.kleinanzeigen.de / s - preis: 20: / seite: 2 / l % C3 % B6tstation / k0
        print("gui2  : ...")
        url = "https://www.kleinanzeigen.de/s-preis:20:/l%C3%B6tstation/k0"
        create_task(url,"")
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        print("gui2  : dummy")
        response = "running..."
        print("gui2  : DONE")
        return self.wfile.write(response.encode())


MyHandler.start()  # will stop here
