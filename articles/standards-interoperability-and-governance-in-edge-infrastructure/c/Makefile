CC = gcc
CFLAGS = -Wall -Wextra -O2

all: conformance_watchdog

conformance_watchdog: conformance_watchdog.c
	$(CC) $(CFLAGS) conformance_watchdog.c -o conformance_watchdog

clean:
	rm -f conformance_watchdog
