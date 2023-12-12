import html
import re
import urllib
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse

from old_crawler import scanAndSave


# Define the HTTP request handler class
class MyHandler(BaseHTTPRequestHandler):

    def do_POST(self):
        pass


    # Handle GET requests
    def do_GET(self):
        # https: // www.kleinanzeigen.de / s - preis: 20: / seite: 2 / l % C3 % B6tstation / k0
        url = "https://www.kleinanzeigen.de/s-preis:20:/l%C3%B6tstation/k0"
        if re.match(".*/check.*",self.requestline):
            query = urlparse(self.path).query
            query_components = dict(qc.split("=") for qc in query.split("&"))
            url = urllib.parse.unquote (query_components["lname"])
        scanAndSave(url)
        # Send response status code
        self.send_response(200)

        with open('cache/data.csv', 'r', encoding='utf8') as file:
            data_csv = file.read()

        # Send headers
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        # Send response content
        response = """
               <style>
                   .d_img {  float: left; }
                   .d_block {  float: left; }
                   img {
                      border: 1px solid #ddd;
                      border-radius: 4px;
                      padding: 5px;
                      width: 150px;
                      height: 100px;
                    }
                     a:link {
                              text-decoration: none;
                        }
                        
                        a:visited {
                              text-decoration: none;
                        }
                        
                        a:hover {
                              text-decoration: none;
                        }
                        
                        a:active {
                              text-decoration: none;
                        }

                </style>
          """ \
                   +  "<h1>Welcome to My Web Server!</h1>" \
                   + """
             <form action="/check" method="get">
             """ + ' <input type="text" id="lname2" name="lname" value="' + url + '" size="100"><br><br> ' + """
  <input type="submit" value="Submit">
</form> 
        """
        data_csvs = data_csv.split("\n")
        response += "<div class='d_block'>"
        for data_row in data_csvs:
            data_elem = data_row.split(" ")
            if len(data_elem) < 2:
                None
                # print(" SKIPP2")
            elif "" != data_elem[0]:
                response += "</div>"
                response += "<div class='d_block'>"
                # print( "<br>" + data_elem[0] + " " + data_elem[1] + "<br>" )
                response += "<br>" + data_elem[0] + " " + data_elem[1] + "<br>"
            elif "" != data_elem[2] :
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

# Define the server's IP address and port
server_address = ('', 8000)

# Create an HTTP server with the defined address and request handler
httpd = HTTPServer(server_address, MyHandler)

# Start the server
print("Server running on http://localhost:8000")
httpd.serve_forever()

