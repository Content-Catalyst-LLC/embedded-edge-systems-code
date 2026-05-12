CC = gcc
CFLAGS = -Wall -Wextra -O2

all: cps_firmware_interface

cps_firmware_interface: cps_firmware_interface.c
	$(CC) $(CFLAGS) cps_firmware_interface.c -o cps_firmware_interface

clean:
	rm -f cps_firmware_interface
