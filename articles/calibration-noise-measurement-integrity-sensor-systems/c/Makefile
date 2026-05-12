CC = gcc
CFLAGS = -Wall -Wextra -O2

all: measurement_quality_flags

measurement_quality_flags: measurement_quality_flags.c
	$(CC) $(CFLAGS) measurement_quality_flags.c -o measurement_quality_flags

clean:
	rm -f measurement_quality_flags
