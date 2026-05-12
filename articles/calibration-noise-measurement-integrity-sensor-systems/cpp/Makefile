CXX = g++
CXXFLAGS = -std=c++17 -Wall -Wextra -O2

all: measurement_state_machine

measurement_state_machine: measurement_state_machine.cpp
	$(CXX) $(CXXFLAGS) measurement_state_machine.cpp -o measurement_state_machine

clean:
	rm -f measurement_state_machine
