#  coding: utf-8 
import SocketServer
import os

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(SocketServer.BaseRequestHandler):
    
    def handle(self):
	http_200 = "HTTP/1.1 200 OK\r\n"
	http_404 = "HTTP/1.1 404 NOT FOUND\r\n\r\n<html><body><h1>HTTP/1.1 404 NOT FOUND</h1></body></html>\r\n\r\n"
	
	self.data = self.request.recv(1024).strip()
	print ("Got a request of: %s\n" % self.data)
        requestList = self.data.split('\n')
        filepath = requestList[0].split()[1]
	parent = ''
	try:
	    if (requestList[6].startswith('Referer:') and not requestList[6].endswith('/')):
		temp = requestList[6].split('/')
		parent = temp[-1].strip()
	except:
	    pass    
	    
	if (filepath.endswith('/')):
	    filepath += "index.html"
	    theType = "text/html"
	elif (filepath.endswith("deep")):
	    filepath += "/index.html"
	    theType = "text/html"
	elif (filepath.endswith(".html")):
	    theType = "text/html"
	elif (filepath.endswith(".css")):
	    theType = "text/css"
	    if (not parent.endswith(".html")):
		filepath = "/" + parent + filepath

	try:
	    theFile = open("www/" + filepath, 'r').read()	    
	    sendMessage = http_200 + "Content-Type: " + theType + "\r\nContent-Length: " + str(len(theFile)) + "\r\n\r\n" + theFile  + "\r\n\r\n"
	except:
	    sendMessage = http_404
	    
	self.request.sendall(sendMessage)
        self.request.close()
        
if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    SocketServer.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = SocketServer.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
