# Define the HTTP request handler class
import re
import urllib
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse

import coordinator


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

    def do_POST(self):
        pass

    # Handle GET requests
    def do_GET(self):
        # Send response status code
        self.send_response(200)

        # Send headers
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        # https: // www.kleinanzeigen.de / s - preis: 20: / seite: 2 / l % C3 % B6tstation / k0
        url = "https://www.kleinanzeigen.de/s-preis:20:/l%C3%B6tstation/k0"
        if re.match(".*/check.*", self.requestline):
            query = urlparse(self.path).query
            query_components = dict(qc.split("=") for qc in query.split("&"))
            self.do_check(urllib.parse.unquote(query_components["lname"]))
        else:
            with open("templates/index.html", 'r') as file:
                response = file.read()
            return self.wfile.write(response.encode())

    def do_check(self, param_url):

        with open("templates/index.html", 'r') as file:
            response = file.read()

        response += "<div class='d_block'>"
        data = coordinator.Coordinator().process(param_url, "")
        for data_row in data.split("\n"):
            data_elem = data_row.split(" ")
            if len(data_elem) < 2:
                None
                # print(" SKIPP2")
            elif "" != data_elem[0]:
                response += "</div>"
                response += "<div class='d_block'><br>" + data_elem[0] + " " + data_elem[1] + "<br>"
            elif "" != data_elem[2]:
                price = data_elem[2]
                img = data_elem[3]
                lnk = data_elem[4]
                itm_div = '<!--' + price + ' ---><div class="d_img"><a href="' + lnk + '"><img src="' + img + '"/><div class="d_price">' + price + '</div></a></div>'
                # print(" " + itm_div)
                response += itm_div + '\n'
            else:
                None
                # print (" SKIPP")
            # print(" -")
        response += "</div>"
        # print(" --")
        self.wfile.write(response.encode())
        # print(" ---")
