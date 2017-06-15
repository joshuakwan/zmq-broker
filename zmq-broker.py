#!/usr/bin/python
# Author: Jun Guan/China/IBM
#
# A message broker for zeromq
# See http://zguide.zeromq.org/py:all#Shared-Queue-DEALER-and-ROUTER-sockets
#
# usage: zmq-broker.py <frontend addr> <frontend port> <backend addr> <backend port>
#
# sammple:
#    ./zmq-broker.py "*" 15554 "*" 15555


import zmq
import datetime
import sys


def now():
    return datetime.datetime.now().isoformat()


def with_color(string, fg, bg=49):
    '''Given foreground/background ANSI color codes, return a string that,
    when printed, will format the supplied string using the supplied colors.
    '''
    return "\x1b[%dm\x1b[%dm%s\x1b[39m\x1b[49m" % (fg, bg, string)


def g(string): return with_color(string, 32)  # Green
def m(string): return with_color(string, 35)  # Magenta
def w(string): return with_color(string, 37)  # White
def y(string): return with_color(string, 33)  # Yellow

# Prepare our context and sockets
context = zmq.Context()
frontend = context.socket(zmq.ROUTER)
backend = context.socket(zmq.DEALER)

frontend_host = "tcp://%s:%s" % (sys.argv[1], sys.argv[2])
backend_host = "tcp://%s:%s" % (sys.argv[3], sys.argv[4])

print now() +  m(" [FRONTEND] ") + "launch frontend queue at %s" % frontend_host
frontend.bind(frontend_host)
print now() +  m(" [BACKEND] ") + "launch backend queue at %s" % backend_host
backend.bind(backend_host)

# Initialize poll set
poller = zmq.Poller()
poller.register(frontend, zmq.POLLIN)
poller.register(backend, zmq.POLLIN)

# Switch messages between sockets
while True:
    socks = dict(poller.poll())

    if socks.get(frontend) == zmq.POLLIN:
        message = frontend.recv_multipart()
        print now() + g(" [FRONTEND] ") + w(message)
        backend.send_multipart(message)

    if socks.get(backend) == zmq.POLLIN:
        message = backend.recv_multipart()
        print now() + y(" [BACKEND] ") + w(message)
        frontend.send_multipart(message)
