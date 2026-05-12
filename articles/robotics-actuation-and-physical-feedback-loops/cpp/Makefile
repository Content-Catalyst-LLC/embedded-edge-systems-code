CXX = g++
CXXFLAGS = -std=c++17 -Wall -Wextra -O2

all: robot_state_machine

robot_state_machine: robot_state_machine.cpp
	$(CXX) $(CXXFLAGS) robot_state_machine.cpp -o robot_state_machine

clean:
	rm -f robot_state_machine
