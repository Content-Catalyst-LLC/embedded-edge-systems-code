CC = gcc
CFLAGS = -Wall -Wextra -O2

all: local_redaction_filter

local_redaction_filter: local_redaction_filter.c
	$(CC) $(CFLAGS) local_redaction_filter.c -o local_redaction_filter

clean:
	rm -f local_redaction_filter
