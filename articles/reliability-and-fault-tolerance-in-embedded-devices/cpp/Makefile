CXX ?= c++
CXXFLAGS ?= -Wall -Wextra -O2 -std=c++17

all: reliability_state_machine

reliability_state_machine: reliability_state_machine.cpp
	$(CXX) $(CXXFLAGS) -o reliability_state_machine reliability_state_machine.cpp

clean:
	rm -f reliability_state_machine
