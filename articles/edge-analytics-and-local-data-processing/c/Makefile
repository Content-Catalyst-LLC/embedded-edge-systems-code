CC = gcc
CFLAGS = -Wall -Wextra -O2
LDFLAGS = -lm

all: edge_analytics_window_features

edge_analytics_window_features: edge_analytics_window_features.c
	$(CC) $(CFLAGS) edge_analytics_window_features.c -o edge_analytics_window_features $(LDFLAGS)

clean:
	rm -f edge_analytics_window_features
