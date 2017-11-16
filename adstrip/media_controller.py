##
# a really simple mute/unmute for mpv
# @author Patrick Kage

import socket
import os
import json
import logging

def send_command(sfile, *args):
    s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    command = {
        "command": args
    }
    command = json.dumps(command)

    s.connect(sfile)
    s.send((command + '\n').encode('ascii'))
    data = s.recv(1024)
    s.close()

    logging.debug('sent {} on {} and got [{}]'.format(command, sfile, json.loads(data.decode('ascii'))))
