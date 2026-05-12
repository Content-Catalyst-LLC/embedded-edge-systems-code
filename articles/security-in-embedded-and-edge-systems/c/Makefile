CC = gcc
CFLAGS = -Wall -Wextra -O2

all: trust_state_check

trust_state_check: trust_state_check.c
	$(CC) $(CFLAGS) trust_state_check.c -o trust_state_check

clean:
	rm -f trust_state_check
