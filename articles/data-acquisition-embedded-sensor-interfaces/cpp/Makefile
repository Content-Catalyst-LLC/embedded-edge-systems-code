CXX ?= c++
CXXFLAGS ?= -Wall -Wextra -O2 -std=c++17

all: acquisition_state_machine

acquisition_state_machine: acquisition_state_machine.cpp
	$(CXX) $(CXXFLAGS) -o acquisition_state_machine acquisition_state_machine.cpp

clean:
	rm -f acquisition_state_machine
