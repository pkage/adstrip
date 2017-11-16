import logging
from queue import Queue
import sys
from argparse import ArgumentParser

from .argthread import ArgThread
from . import streamer
from . import frame_extract

from .recognition import TemplateRecognizer

logging.basicConfig(level=logging.DEBUG,
                    format='[%(levelname)s] (%(threadName)-10s) %(message)s')


def main():
    ap = ArgumentParser(description='automatically sift through an MP4 (or other) stream, detect advertising, and issue mute commands to a player')
    ap.add_argument('-u', '--url', help='the source youtube url', nargs=1, required=False)
    ap.add_argument('-i', '--stdin', help='read from stdin, overrides -u', action='store_true')
    ap.add_argument('-o', '--stdout', help='dump output to stdout', action='store_true')
    ap.add_argument('-p', '--patterns', help='patterns to use', nargs='+', metavar='PATH', required=True)

    # debuggy args
    ap.add_argument('--ring-size', help='ring buffer size, in MB or KB', default='1m')
    ap.add_argument('--ring-loc', help='ring buffer location on disk', default='buffer.mp4')
    ap.add_argument('--frame-loc', help='extracted frame location', default='frame.jpeg')
    ap.add_argument('--mpv-ipc-loc', help='mpv ipc socket file location', default='mpv_ipc_soc')
    args = ap.parse_args()

    logging.debug(args)

    msg_q = Queue()
    s = ArgThread(target=streamer.videostream, name='stream', args=(None if args.stdin else args.url[0],msg_q, args))
    p = ArgThread(target=frame_extract.extractor, name='extractor', args=(msg_q,args.patterns,args))
    s.start()
    p.start()

    s.join()
    p.join()


