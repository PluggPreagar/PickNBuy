# Define the HTTP request handler class
import ast
import json
import re
import socketserver
import threading
import time
import urllib

from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
from multiprocessing import Queue
import coordinator

urls_processed = []
tasks = []
results = []
result_idx = 0

def background_operation(url, url_filter, result_queue):
    # Perform some time-consuming operation
    print("gui   : background_operation for \"" + url + "\"")
    data = coordinator.Coordinator().query(url, url_filter)
    print("gui   : background_operation ...")
    #time.sleep(2)
    #print("gui   : background_operation ...")
    #time.sleep(2)
    #print("gui   : background_operation ...")
    #time.sleep(2)
    #print("gui   : background_operation DONE")
    # Add result to the queue
    result_queue.put(data)


def create_task(url, url_filter):
    print("gui   : create_task for \"" + url + "\"")
    # Create a queue to store the result
    result_queue = Queue()
    # Start the background operation in a separate process
    process = threading.Thread(target=background_operation, args=(url, url_filter, result_queue))
    process.start()
    # Add the process and result queue to the tasks list
    tasks.append((process, url, result_queue))


def task_result():
    # Check each task in the tasks list
    for task in tasks:
        process, url, result_queue = task
        # Check if the background operation has finished
        if not process.is_alive():
            result = result_queue.get()  # Get the result from the queue
            results.append(result)  # Add the result to the results list
            tasks.remove(task)  # Remove the task from the tasks list
            urls_processed.append(url)
            process.terminate()  # Terminate the process


class MyHandler(BaseHTTPRequestHandler):



    def __init__(self, request: bytes, client_address: tuple[str, int], server: socketserver.BaseServer):
        super().__init__(request, client_address, server)
        self.result_idx = 1

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

    def do_get_data_json(self, data_idx):
        new_data = f"New Data at {int(time.time())}"
        # Send the new data as a JSON response
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        new_data="{'reifen', 'https://static.kleinanzeigen.de/static/img/common/illustrations/connection-issue.vfwgydoqmp1t.svg', 'https://www.kleinanzeigen.de/s-preis:20:/seite:1/reifen', 'Sehr geehrte Kunden, Herzlich Willkommen bei HolzBM GmbH! Ihr Einzel- und Großhändler für...', ' 380', None }"
        new_data='{"data": ["reifen", "https://static.kleinanzeigen.de/static/img/common/illustrations/connection-issue.vfwgydoqmp1t.svg", "https://www.kleinanzeigen.de/s-preis:20:/seite:1/reifen", "Sehr geehrte Kunden, Herzlich Willkommen bei HolzBM GmbH! Ihr Einzel- und Großhändler für...", " 380", None ]}'
        new_data='["reifen", "https://static.kleinanzeigen.de/static/img/common/illustrations/connection-issue.vfwgydoqmp1t.svg", "https://www.kleinanzeigen.de/s-preis:20:/seite:1/reifen", "Sehr geehrte Kunden, Herzlich Willkommen bei HolzBM GmbH! Ihr Einzel- und Großhändler für...", " 380", "None" ]'
        new_data='["1988775235-87-16235", "https://img.kleinanzeigen.de/api/v1/prod-ads/images/05/05e538c8-1942-479d-b7d1-ee62a7df66c9?rule=$_2.JPG", "https://www.kleinanzeigen.de/s-anzeige/kaminholz-heinsberg-pellets-holzbriketts-brandhout-brennholz-/1988775235-87-16235", "Sehr geehrte Kunden, Herzlich Willkommen bei HolzBM GmbH! Ihr Einzel- und Großhändler für...", " 380", "f374ad747602e41ca1fe4dddd1268341"]'
        #
        #

        new_data = coordinator.Coordinator().cache.read("https://www.kleinanzeigen.de/s-preis:20:/seite:9/l%C3%B6tstation/k0" + ".query")
        #new_data = coordinator.Coordinator().cache.read("https://www.kleinanzeigen.de/s-preis:20:/seite:9/l%C3%B6tstation/k0" + ".csv")
        data = ast.literal_eval(new_data)
        json_data = json.dumps( data )
        json_data = json.dumps( data['2621952793-168-807'])
        if int(data_idx) < len(data):
            key = list(data)[int(data_idx)]
            print("result_idx >>" + data_idx + " >> " + key)
            data[key].append(data_idx)  # just add index as dummy val
            json_data = json.dumps(data[key])

            #
            self.wfile.write(json_data.encode())
        else:
            print("result_idx >>" + data_idx + " EOF (" + str(len(data)) + ")" )
        self.wfile.write("".encode())
        # id img_lnk descr price hash


    def do_get_data_jsonNamed(self, data_idx, data_qry, data_refresh_flag):
        data_idx_range = data_idx.split("..")
        new_data = f"New Data at {int(time.time())}"
        # Send the new data as a JSON response
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        #
        param_url = urllib.parse.unquote(data_qry)
        new_data = coordinator.Coordinator().cache.read(param_url + ".query")
        if new_data is None or data_refresh_flag :
            print("gui::jsonName:  data_qry=\"" + param_url + "\"")
            create_task(param_url, "" + ( "refresh" if data_refresh_flag else ""  ) )
        #new_data = coordinator.Coordinator().cache.read("https://www.kleinanzeigen.de/s-preis:20:/seite:9/l%C3%B6tstation/k0" + ".csv")
        # json_data = json.dumps( data )
        # json_data = json.dumps( data['2621952793-168-807'])
        if new_data is None:
            print("gui::jsonName: result_idx >>" + " loading ... ")
        else:
            # data = ast.literal_eval(new_data) #
            # data = json.load(new_data)  # AttributeError: 'str' object has no attribute 'read'
            data = json.loads(new_data)
            if 1 == len(data_idx_range) and int(data_idx) < len(data):
                key = list(data)[int(data_idx)]
                print("gui::jsonName: result_idx >>" + data_idx + " >> " + key)
                # data[key].append(data_idx)  # just add index as dummy val
                # data_ = dict(zip( ["key", "img", "img_lnk", "descr", "price","img_hash", "idx"] , data[key]))
                # json_data = json.dumps(data_)
                json_data = data[key]
                json_data["idx"] = data_idx # blend in current index for loading ...
                #
                # self.wfile.write(json_data.encode())   # AttributeError: 'dict' object has no attribute 'encode'
                self.wfile.write( json.dumps( json_data ).encode() ) #TypeError: a bytes-like object is required, not 'str'
                print("gui::jsonName: result_idx >>" + data_idx + " ... ")
            elif 2 == len(data_idx_range) and int(data_idx_range[0]) < len(data) and int(data_idx_range[0]) < int(data_idx_range[1]):
                j_str = ""
                json_array=[]
                data_idx=int(data_idx_range[0])
                keys = list(data)[int(data_idx_range[0]):int(data_idx_range[1])]
                for key in keys:
                    print("gui::jsonName: result_idx >>" + str(data_idx) + " >> " + key)
                    # print("gui::jsonName: result_idx >>" + str(data) )
                    json_data = {}
                    json_data = data[key]
                    json_data["idx"] = data_idx  # blend in current index for loading ...
                    json_array.append( json_data )
                    data_idx += 1
                # self.wfile.write(json_data.encode())   # AttributeError: 'dict' object has no attribute 'encode'
                self.wfile.write( json.dumps( json_array ).encode() ) #TypeError: a bytes-like object is required, not 'str'
                print("gui::jsonName: result_idx >>" + data_idx_range[0] + " ... " + data_idx_range[1] )

            else:
                print("gui::jsonName: result_idx >>" + data_idx + " EOF (" + str(len(data)) + ")" )
        self.wfile.write("".encode())
        # id img_lnk descr price hash

    def do_get_data(self):
        new_data = f"New Data at {int(time.time())}"
        # Send the new data as a JSON response
        self.send_response(400)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(new_data.encode())

    # Handle GET requests
    def do_GET(self):
        # Send response status code
        urlElems = urlparse(self.path)
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
        if self.path == '/style.css':
            self.send_response(200)
            self.send_header('Content-Type', 'text/css')
            self.end_headers()
            response = ""
            with open('static/style.css', 'rb') as file:
                response = file.read()
            self.wfile.write(response)
            return
        if self.path == '/util.js' or self.path == '/util_load.js' or self.path == '/util_gui.js' :
            self.send_response(200)
            self.send_header('Content-Type', 'text')
            self.end_headers()
            response = ""
            with open('static/' + self.path, 'rb') as file:
                response = file.read()
            self.wfile.write(response)
            return


        # https: // www.kleinanzeigen.de / s - preis: 20: / seite: 2 / l % C3 % B6tstation / k0
        url = "https://www.kleinanzeigen.de/s-preis:20:/l%C3%B6tstation/k0"
        if re.match(".*/check.*", self.requestline):
            print("gui   : check \"" + url + "\"")
            query = urlparse(self.path).query
            query_components = dict(qc.split("=") for qc in query.split("&"))
            lname = query_components["lname"]
            print("gui   :    lname=\"" + lname + "\"")
            self.do_check(urllib.parse.unquote(lname))
        elif self.path == '/data' or urlElems.path == '/data':
            print("gui   : data \"" + "" + "\"")
            # self.do_get_data()
            query = urlparse(self.path).query
            query_components = dict(qc.split("=") for qc in query.split("&")) if query.count("=") > 0 else {}
            self.do_get_data_jsonNamed( query_components["idx"] )
        elif self.path == '/json' or urlElems.path == '/json':
            print("gui   : json \"" + "" + "\"")
            # self.do_get_data()
            query = urlparse(self.path).query
            query_components = dict(qc.split("=") for qc in query.split("&")) if query.count("=") > 0 else {}
            self.do_get_data_jsonNamed( query_components["idx"], query_components["qry"], (("refresh" in query_components) and ("1"==query_components["refresh"]))  )
        else:
            print("gui   : ELSE \"" + url + "\"")
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open("templates/index.html", 'r') as file:
                response = file.read()
            response = response.replace("param_url", url)
            return self.wfile.write(response.encode())

    def do_check(self, param_url):

        create_task(param_url, "")

        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        with open("templates/index.html", 'r') as file:
            response = file.read()
        response = response.replace("param_url", param_url)
        return self.wfile.write(response.encode())
        # print(" ---")
        print("gui  : DONE")
