CC ?= cc
CFLAGS ?= -Wall -Wextra -O2

all: platform_capability_contract

platform_capability_contract: platform_capability_contract.c
	$(CC) $(CFLAGS) -o platform_capability_contract platform_capability_contract.c

clean:
	rm -f platform_capability_contract
