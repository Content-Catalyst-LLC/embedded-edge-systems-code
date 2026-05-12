CC = gcc
CFLAGS = -Wall -Wextra -O2

all: embedded_pid_controller

embedded_pid_controller: embedded_pid_controller.c
	$(CC) $(CFLAGS) embedded_pid_controller.c -o embedded_pid_controller

clean:
	rm -f embedded_pid_controller
