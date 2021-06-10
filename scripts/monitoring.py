import zmq
import time

context = zmq.Context()

#  Socket to talk to server
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5556")

while 1:
	action=[1,2]
	socket.send_string("REQ")
	message = socket.recv()
	print(message)
	time.sleep(1)


