CC = gcc
CFLAGS = -Wall -Wextra -O2

all: pid_control_loop

pid_control_loop: pid_control_loop.c
	$(CC) $(CFLAGS) pid_control_loop.c -o pid_control_loop

clean:
	rm -f pid_control_loop
