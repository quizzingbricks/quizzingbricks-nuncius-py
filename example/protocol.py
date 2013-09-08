# -*- coding: utf-8 -*-
"""
    Copyright (C) QuizzingBricks
"""

# protocol, simulate protobuf but using json while prototyping.

import json

class RpcGetUsernameRequest(object):
	def __init__(self, user_id=None):
		self.user_id = user_id

	def SerializeToString(self):
		return str(self.user_id)

	def ParseFromString(self, data):
		self.user_id = int(data)

class RpcGetUsernameResponse(object):
	def __init__(self, user_id=None, username=None):
		self.user_id = user_id
		self.username = username

	def SerializeToString(self):
		return json.dumps({
			"id": self.user_id,
			"username": self.username
		})

	def ParseFromString(self, data):
		fields = json.loads(data)
		self.user_id = fields.get("id")
		self.username = fields.get("username")

