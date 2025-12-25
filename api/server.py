from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from api.sensor_handler import create_sensor
# HTTP LAYER -> 
# start an HTTP server
# listens to the port (8080)
# read http requests
# sends http response
# """sent a POST request to /sensor"""

class SensorRequestHandler(BaseHTTPRequestHandler):

    def do_POST(self):
        if self.path!="/sensor":  #read request path = manual routing
            self.send_response(404)
            self.end_headers()
            return
        
        # read request 
        content_length = int(self.headers.get("Content-Length", 0))
        request_body=self.rfile.read(content_length).decode("utf-8")

        status_code, response=create_sensor(request_body)

        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.end_headers()

        self.wfile.write(json.dumps(response).encode("utf-8"))

    def log_message(self, format, *args):
        return
    
def run_server():
    server_address=("", 8000)
    httpd=HTTPServer(server_address, SensorRequestHandler)
    print("sensor API running on port 8000")
    httpd.serve_forever()

if __name__=="__main__":
    run_server()
    