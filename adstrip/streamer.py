##
# MP4 stream passthrough/creation
# @author Patrick Kage

import sys
import shlex
import logging
from subprocess import Popen, PIPE

def videostream(url, out_q, cfg):
    # prepare the url reader
    if url is not None:
        ytdl_c = 'youtube-dl -q -o - "{}" -f best'.format(url)
    else:
        ytdl_c = 'cat'
    ytdl_c = shlex.split(ytdl_c)

    # load in our C extension (jankily)
    ring_c = 'adstrip/ringbuf/ring {} {}'.format(cfg.ring_loc, cfg.ring_size.lower())
    ring_c = shlex.split(ring_c)

    # create the player or passthrough
    if not cfg.stdout:
        play_c = 'mpv --input-ipc-server {} -'.format(cfg.mpv_ipc_loc)
    else:
        play_c = 'cat'
    play_c = shlex.split(play_c)

    logging.debug('running...\n')
    with Popen(ytdl_c, stdin=sys.stdin, stdout=PIPE) as instream, Popen(ring_c, stdin=instream.stdout, stdout=PIPE, stderr=PIPE) as ring, Popen(play_c, stdin=ring.stdout) as player:
        # close the correct pipes
        instream.stdout.close()
        ring.stdout.close()

        try:
            for line in ring.stderr:
                logging.debug('intercepted write from ring')
                # write an arbitrary byte
                out_q.put(1)
        except KeyboardInterrupt:
            logging.debug('stopping...')
            instream.kill()
