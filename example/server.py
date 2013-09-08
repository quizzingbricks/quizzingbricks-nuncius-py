# -*- coding: utf-8 -*-
"""
    Copyright (C) QuizzingBricks
"""

import sys
sys.path.append("..")

from nincius import NinciusService, expose
import protocol

proto_mapper = {
    0: protocol.RpcGetUsernameRequest,
    1: protocol.RpcGetUsernameResponse
}

class RpcUserService(NinciusService):
    name = "UserService"
    protocol_mapper = proto_mapper

    usernames = {123: "mikael", 987: "guest"}

    def __init__(self, *args, **kwargs):
        super(RpcUserService, self).__init__(*args, **kwargs)

    @expose("get_username")
    def _get_username(self, request):
        return protocol.RpcGetUsernameResponse(user_id=request.user_id, 
            username=self.usernames.get(request.user_id, "Anonymous"))


if __name__ == "__main__":
    service = RpcUserService(uri="tcp://*:5556")
    service.run()

