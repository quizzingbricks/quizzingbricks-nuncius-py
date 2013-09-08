# -*- coding: utf-8 -*-
"""
    Copyright (C) QuizzingBricks
"""

import json
import zmq.green as zmq

import functools

#def _expose(f):
#   def wrapper_func(self, *args, **kwargs):
#       return f(self, *args, **kwargs)
#   wrapper_func.exposed = True
#   #wrapper_func.exposed_name = name
#   return functools.update_wrapper(wrapper_func, f)

def expose(name=None):
    def _expose(func):
        def _decorator(*args, **kwargs):
            return func(*args, **kwargs)
        func.exposed = True
        func.exposed_name = name or func.__name__
        return functools.wraps(func)(_decorator)
    #_expose.exposed = True
    return _expose

class NinciusService(object):
    name = None # implemented in subclass

    def __init__(self, uri):
        self._uri = uri
        self._methods = {}
        self._context = zmq.Context()
        self._socket = self._context.socket(zmq.REP)

        self._protocol_map = {} # implemented in subclass, map between digit and protobuf message
        self._inverse_protocol_map = {}

        # TODO: remove the setter
        if self.protocol_mapper:
            self.protocol_map = self.protocol_mapper

        self.expose_methods()

    def expose_methods(self):
        methods = [method for method in dir(self) if callable(getattr(self, method)) 
            and hasattr(getattr(self, method), "exposed")]
        
        for method in methods:
            method_callable = getattr(self, method)
            self._methods[getattr(method_callable, "exposed_name", method_callable.__name__)] = method_callable

    @property
    def protocol_map(self):
        return self._protocol_map

    @protocol_map.setter
    def protocol_map(self, mapper):
        if not isinstance(mapper, dict):
            raise ValueError("mapper requires to be a dict")
        self._protocol_map = mapper
        self._inverse_protocol_map = {v.__name__: k for k, v in mapper.iteritems()}

    def run(self):
        self._socket.bind(self._uri)

        while True:
            _method, message_type = json.loads(self._socket.recv())
            body = self._socket.recv()
            message_cls = self._protocol_map[message_type]() # assume the type is in the dict
            message_cls.ParseFromString(body) # TODO: deserialize the protobuf message

            method = _method.split("/")[-1]
            if not method in self._methods:
                # todo: reply with an error message
                print "Method %s does not exists" % method
            response = self._methods[method](message_cls) # call the method and passing the message

            # reply with message type followed by the acutal message
            # TODO: don't assume we always have a message instance
            self._socket.send(str(self._inverse_protocol_map[response.__class__.__name__]), zmq.SNDMORE)
            self._socket.send(response.SerializeToString())
