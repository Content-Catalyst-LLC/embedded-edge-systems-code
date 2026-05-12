CC = gcc
CFLAGS = -Wall -Wextra -O2

all: gateway_telemetry_packet

gateway_telemetry_packet: gateway_telemetry_packet.c
	$(CC) $(CFLAGS) gateway_telemetry_packet.c -o gateway_telemetry_packet

clean:
	rm -f gateway_telemetry_packet
