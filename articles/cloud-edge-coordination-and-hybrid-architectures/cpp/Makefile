CXX = g++
CXXFLAGS = -std=c++17 -Wall -Wextra -O2

all: gateway_sync_state_machine

gateway_sync_state_machine: gateway_sync_state_machine.cpp
	$(CXX) $(CXXFLAGS) gateway_sync_state_machine.cpp -o gateway_sync_state_machine

clean:
	rm -f gateway_sync_state_machine
