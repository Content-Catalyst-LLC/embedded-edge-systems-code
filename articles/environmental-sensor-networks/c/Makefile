CC ?= cc
CFLAGS ?= -Wall -Wextra -O2

all: environmental_node_health

environmental_node_health: environmental_node_health.c
	$(CC) $(CFLAGS) -o environmental_node_health environmental_node_health.c

clean:
	rm -f environmental_node_health
