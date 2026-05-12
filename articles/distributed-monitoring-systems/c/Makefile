CC = gcc
CFLAGS = -Wall -Wextra -O2

all: monitoring_node_status

monitoring_node_status: monitoring_node_status.c
	$(CC) $(CFLAGS) monitoring_node_status.c -o monitoring_node_status

clean:
	rm -f monitoring_node_status
