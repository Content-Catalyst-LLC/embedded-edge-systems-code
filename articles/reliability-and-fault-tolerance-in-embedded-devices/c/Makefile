CC ?= cc
CFLAGS ?= -Wall -Wextra -O2

all: watchdog_health_policy

watchdog_health_policy: watchdog_health_policy.c
	$(CC) $(CFLAGS) -o watchdog_health_policy watchdog_health_policy.c

clean:
	rm -f watchdog_health_policy
