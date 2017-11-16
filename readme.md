# adstrip

## Purpose

Consume a video stream (usually of a news feed) and automatically send a mute command to MPV when a specified pattern leaves the screen. Powered by OpenCV, ffmpeg, and hacked together in a weekend.

## Dependencies

__Required:__

Python: `youtube-dl, opencv-python, scikit-image`

C: `gcc/clang`

`ffmpeg` must also be on your `$PATH`

__Optional:__

Python: `matplotlib` (for running `recognitiontest.py`)

## Installation

```bash
$ git clone https://github.com/quadnix/adstrip
$ cd adstrip
$ virtualenv -p python3 env_adstrip
$ source env_adstrip/bin/activate
$ pip3 install -r requirements.txt
$ make
```

__On macOS with [Homebrew](https://brew.sh/):__

```
$ brew install mpv ffmpeg --verbose
```

This should make sure that these are on your `$PATH`.

__Windows:__

No windows support right now.

__Linux:__

Install `mpv` and `ffmpeg` with the package manager for your distro. You chose to run Linux, you're smart enough to figure this one out.

## Usage

```
usage: adstrip.py [-h] [-u URL] [-i] [-o] -p PATH [PATH ...]
                  [--ring-size RING_SIZE] [--ring-loc RING_LOC]
                  [--frame-loc FRAME_LOC] [--mpv-ipc-loc MPV_IPC_LOC]

automatically sift through an MP4 (or other) stream, detect advertising, and
issue mute commands to a player

optional arguments:
  -h, --help            show this help message and exit
  -u URL, --url URL     the source youtube url
  -i, --stdin           read from stdin, overrides -u
  -o, --stdout          dump output to stdout
  -p PATH [PATH ...], --patterns PATH [PATH ...]
                        patterns to use
  --ring-size RING_SIZE
                        ring buffer size, in MB or KB
  --ring-loc RING_LOC   ring buffer location on disk
  --frame-loc FRAME_LOC
                        extracted frame location
  --mpv-ipc-loc MPV_IPC_LOC
                        mpv ipc socket file location
```

### Examples

Use an existing file:

```
$ cat movie.mp4 | ./adstrip.py --stdin -p patterns/pat.png
```

Get a stream from youtube from stdin:

```
$ youtube-dl -f best -q -o - "https://youtube.com/watch?v=0123456789" | ./adstrip.py --stdin -p patterns/pat.png
```

Get a stream from youtube from adstrip internal:

```
$ ./adstrip.py -u "https://youtube.com/watch?v=0123456789" -p patterns/pat.png
```

Stream output to MPV separately:

```
$ ./adstrip.py -u "https://youtube.com/watch?v=0123456789" --stdout --mpv-ipc-loc /tmp/mpv_ipc -p patterns/pat.png | mpv --input-ipc-server /tmp/mpv_ipc -
```

