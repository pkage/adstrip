##
# frame ripper + openCV image parser
# @author Patrick Kage

import os
from subprocess import Popen, PIPE, DEVNULL
import shlex
import logging
from .recognition import TemplateRecognizer
from .media_controller import send_command

def create_frame(buf, out):
    # create the ffmpeg command
    cfm_c = 'ffmpeg -i {} -vf "select=\'eq(n,0)\'" -vframes 1 {}'.format(buf, out)
    cfm_c = shlex.split(cfm_c)

    # make sure we have a buffer to work with
    if not os.path.exists(buf):
        logging.warning('buffer {} is missing!'.format(buf))

    # check if the frame exists, and remove if it does
    if os.path.exists(out):
        os.remove(out)

    # launch ffmpeg against the ring buffer
    with Popen(cfm_c, stdout=DEVNULL, stderr=DEVNULL) as cfm:
        # wait for processing to finish
        cfm.wait()

        # did we get a usable frame?
        if os.path.exists(out):
            logging.debug('successfully got a frame into {}'.format(out))
            return True
        else:
            logging.warning('failed to extract a usable frame!')
            return False


def extractor(in_q, pats, cfg):
    runonce = False
    tf = TemplateRecognizer()
    while True:
        _ = in_q.get()
        logging.debug('beginning frame extraction from ring...')

        if create_frame(cfg.ring_loc, cfg.frame_loc):
            outs = []
            for pat in pats:
                outs.append(tf.detect(cfg.frame_loc, pat))
            if sum(outs) > (len(pats) * 0.3):
                logging.info('probably not a commercial')
                send_command(cfg.mpv_ipc_loc, 'set_property', 'ao-volume', 100)
            else:
                logging.info('probably a commercial')
                send_command(cfg.mpv_ipc_loc, 'set_property', 'ao-volume', 0)

            logging.debug(outs)
