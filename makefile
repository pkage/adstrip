PATTERNS = patterns/cnn_live.png patterns/cnn_live_inverse.png

all: clean build-ring

build-ring:
	cd adstrip/ringbuf && make build

clean: 
	rm -f frame.jpeg buffer.mp4

run: clean
	./adstrip.py `cat stream.txt`

run-live-pipe: clean
	youtube-dl -q -o - -f best `cat stream.txt` | ./adstrip.py --stdin -p ${PATTERNS}

run-live:
	./adstrip.py -u `cat stream.txt` -p ${PATTERNS}

run-canned: clean
	cat test.mp4 | ./adstrip.py --stdin -p ${PATTERNS}
