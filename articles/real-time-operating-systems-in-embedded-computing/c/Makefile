CC ?= cc
CFLAGS ?= -Wall -Wextra -O2

all: rtos_task_contract

rtos_task_contract: rtos_task_contract.c
	$(CC) $(CFLAGS) -o rtos_task_contract rtos_task_contract.c

clean:
	rm -f rtos_task_contract
