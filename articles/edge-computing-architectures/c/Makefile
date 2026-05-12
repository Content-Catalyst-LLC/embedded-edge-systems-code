CC = gcc
CFLAGS = -Wall -Wextra -O2

all: edge_watchdog_offline_state

edge_watchdog_offline_state: edge_watchdog_offline_state.c
	$(CC) $(CFLAGS) edge_watchdog_offline_state.c -o edge_watchdog_offline_state

clean:
	rm -f edge_watchdog_offline_state
