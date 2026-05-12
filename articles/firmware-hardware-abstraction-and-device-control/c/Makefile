CC ?= cc
CFLAGS ?= -Wall -Wextra -O2

all: hal_driver_contract

hal_driver_contract: hal_driver_contract.c
	$(CC) $(CFLAGS) -o hal_driver_contract hal_driver_contract.c

clean:
	rm -f hal_driver_contract
