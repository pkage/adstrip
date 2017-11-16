all: build


clean:
	rm -f ring test.dat

build: clean
	clang ring.c -o ring

run: build
	./ring test.dat 1m

test: build
	rm -f test2.mp4
	cat test.mp4 | ./ring test.dat 1m > test2.mp4

test2: build
	rm -f test2.txt
	cat smalltest.txt | ./ring test.dat 1m > test2.txt

streamtest: build
	cat /dev/urandom | ./ring test.dat 1m > /dev/null
