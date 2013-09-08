# -*- coding: utf-8 -*-
"""
    Copyright (C) QuizzingBricks
"""

import zmq.green as zmq
import json

import protocol

context = zmq.Context()

# or just write the digits as strings to avoid type conversion :)
proto_mapper = {
	0: protocol.RpcGetUsernameRequest,
	1: protocol.RpcGetUsernameResponse
}

proto_inverse_mapper = {v.__name__: k for k, v in proto_mapper.iteritems()}

def main(user_id):
	socket = context.socket(zmq.REQ)
	socket.connect('tcp://localhost:5556')

	req = protocol.RpcGetUsernameRequest(user_id)
	socket.send(json.dumps(["get_username", proto_inverse_mapper[req.__class__.__name__]]), zmq.SNDMORE)
	socket.send(req.SerializeToString())

	response_type = socket.recv()
	response = socket.recv()

	message = proto_mapper[int(response_type)]()
	message.ParseFromString(response)

	socket.close()
	return message.user_id, message.username

if __name__ == "__main__":
	for x in xrange(2000):
		print x, main(123), main(987)

