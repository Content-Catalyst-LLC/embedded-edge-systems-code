CC = gcc
CFLAGS = -Wall -Wextra -O2
LDFLAGS = -lm

all: edge_ai_feature_inference

edge_ai_feature_inference: edge_ai_feature_inference.c
	$(CC) $(CFLAGS) edge_ai_feature_inference.c -o edge_ai_feature_inference $(LDFLAGS)

clean:
	rm -f edge_ai_feature_inference
