CXX ?= c++
CXXFLAGS ?= -Wall -Wextra -O2 -std=c++17

all: power_state_machine

power_state_machine: power_state_machine.cpp
	$(CXX) $(CXXFLAGS) -o power_state_machine power_state_machine.cpp

clean:
	rm -f power_state_machine
