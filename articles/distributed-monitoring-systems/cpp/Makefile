CXX = g++
CXXFLAGS = -std=c++17 -Wall -Wextra -O2

all: distributed_monitoring_state_machine

distributed_monitoring_state_machine: distributed_monitoring_state_machine.cpp
	$(CXX) $(CXXFLAGS) distributed_monitoring_state_machine.cpp -o distributed_monitoring_state_machine

clean:
	rm -f distributed_monitoring_state_machine
