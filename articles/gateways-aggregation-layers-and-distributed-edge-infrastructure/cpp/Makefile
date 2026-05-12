CXX = g++
CXXFLAGS = -std=c++17 -Wall -Wextra -O2

all: gateway_runtime_state_machine

gateway_runtime_state_machine: gateway_runtime_state_machine.cpp
	$(CXX) $(CXXFLAGS) gateway_runtime_state_machine.cpp -o gateway_runtime_state_machine

clean:
	rm -f gateway_runtime_state_machine
