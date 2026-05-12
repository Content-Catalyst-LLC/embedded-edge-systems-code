CXX ?= c++
CXXFLAGS ?= -Wall -Wextra -O2 -std=c++17

all: network_node_state_machine

network_node_state_machine: network_node_state_machine.cpp
	$(CXX) $(CXXFLAGS) -o network_node_state_machine network_node_state_machine.cpp

clean:
	rm -f network_node_state_machine
