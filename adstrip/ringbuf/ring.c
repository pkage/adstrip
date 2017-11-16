/**
 * Small utility to create a (pseudo-)ring buffer
 * @author Patrick Kage
 */

#include <stdlib.h>
#include <fcntl.h>
#include <unistd.h>
#include <stdio.h>
#include <errno.h>
#include <string.h>
#include <stdbool.h>

int parse_opts(int argc, char** argv, size_t* size, char** fname, bool* quiet);

int main(int argc, char** argv) {
	char* ring_name;
	size_t ring_size = 0;
	bool quiet;

	if (parse_opts(argc, argv, &ring_size, &ring_name, &quiet) == -1) {
		return 1;
	}

	/* create the ring */
	uint8_t* ring = (uint8_t*)malloc(ring_size);
	unsigned int ring_pos = 0;

	int ch;
	while (1) {
		ch = getchar();
		if (ch == EOF) {
			break;
		}

		ring[ring_pos] = ch;
		ring_pos++;
		if (ring_pos == ring_size) {
			ring_pos = 0;

			/* dump output */
			FILE *dump = fopen(ring_name, "wb");
			fwrite(ring, ring_size, 1, dump);
			fclose(dump);

			if (!quiet) {
				fprintf(stderr, "\rwrote to %s\n", ring_name);
			}

		}

		putchar(ch);
	}

	/* i guess not strictly necessary */
	free(ring);
	return 0;
}


void usage(char** argv) {
		fprintf(stderr, "usage: %s [ringfile] [size in kb] (-q)\n", argv[0]);
}

int parse_opts(int argc, char** argv, size_t* size, char** fname, bool* quiet) {
	if (argc != 3 && argc != 4) {
		usage(argv);
		return -1;
	}

	/* set the output filename pointer */
	*fname = argv[1];

	/* try to convert the buffer size */
	/* first, strip off the ending k if it exists by null terminating */
	int len = strlen(argv[2]);
	int mult = 1;
	if (argv[2][len - 1] == 'k') {
		argv[2][len - 1] = '\0';
		mult = 1024;
	} else if (argv[2][len - 1] == 'm') {
		argv[2][len - 1] = '\0';
		mult = 1024 * 1024;
	}

	/* convert */
	int tmpsize = atoi(argv[2]);

	/* catch atoi failure */
	if (tmpsize <= 0) {
		fprintf(stderr, "invalid buffer size \"%s\"!", argv[2]);
		return -1;
	}

	*size = (tmpsize * mult);

	if (argc == 4 && strcmp("-q", argv[3]) != 0) {
		*quiet = true;
	} else if (argc == 4) {
		usage(argv);
		return -1;
	} else {
		*quiet = false;
	}

	return 0;
}
