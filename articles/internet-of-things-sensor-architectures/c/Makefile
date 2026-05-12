CC = gcc
CFLAGS = -Wall -Wextra -O2

all: iot_endpoint_queue

iot_endpoint_queue: iot_endpoint_queue.c
	$(CC) $(CFLAGS) iot_endpoint_queue.c -o iot_endpoint_queue

clean:
	rm -f iot_endpoint_queue
