CC ?= cc
CFLAGS ?= -Wall -Wextra -O2

all: acquisition_quality_monitor

acquisition_quality_monitor: acquisition_quality_monitor.c
	$(CC) $(CFLAGS) -o acquisition_quality_monitor acquisition_quality_monitor.c

clean:
	rm -f acquisition_quality_monitor
