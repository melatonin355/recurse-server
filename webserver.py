from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs


memory = {}

# http://localhost:4000/set?somekey=somevalue it should store the passed key and value in memory.
# http://localhost:4000/get?key=somekey it should return the value stored at somekey.


class RequestHandler(BaseHTTPRequestHandler):
    def write_file(self):
        # Write the response into a file
        pass

    def do_GET(self):

        parsed_url = urlparse(self.path)
        query = parse_qs(parsed_url.query)

        if parsed_url.path == "/set":
            self.set_key(query)

        elif parsed_url.path == "/get":
            self.get_value(query)
        else:
            self.send_error(404, "Invalid URL")

    def set_key(self, query):
        try:
            key, value = "", ""
            # Update in memory key value pair
            for k, v in query.items():
                key += k
                value += v[0]
                memory[key] = value

            # Success response
            self.send_response(200)
            self.send_header("content-type", "text/html")
            self.end_headers()
            output = f"<html> SET key,value : {key} : {value} in memory.</html>"
            self.wfile.write(output.encode())
        except KeyError:
            self.send_error(400, "Missing or invalid query parameter")

    def get_value(self, query):
        # Get the key from the query string
        try:

            key = query["key"][0]

            if key in memory:
                value = memory[key]
                self.send_response(200)
                self.send_header("content-type", "text/html")
                self.end_headers()
                output = f"<html> The value for key {key} is : {value} </html>"
                self.wfile.write(output.encode())
            else:
                self.send_error(404, "key not found")
        except KeyError:
            self.send_error(404, "Missing or invalid query parameter")


if __name__ == "__main__":
    # Start the HTTP server on port 4000
    server_address = ("", 4000)
    server = HTTPServer(server_address, RequestHandler)
    print("Server started on http://localhost:4000")
    server.serve_forever()
