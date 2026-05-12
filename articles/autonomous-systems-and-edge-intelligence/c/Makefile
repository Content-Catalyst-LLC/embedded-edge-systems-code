CC = gcc
CFLAGS = -Wall -Wextra -O2

all: bounded_autonomy_controller

bounded_autonomy_controller: bounded_autonomy_controller.c
	$(CC) $(CFLAGS) bounded_autonomy_controller.c -o bounded_autonomy_controller

clean:
	rm -f bounded_autonomy_controller
