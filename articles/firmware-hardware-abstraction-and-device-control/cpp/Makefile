CXX ?= c++
CXXFLAGS ?= -Wall -Wextra -O2 -std=c++17

all: device_lifecycle_state_machine

device_lifecycle_state_machine: device_lifecycle_state_machine.cpp
	$(CXX) $(CXXFLAGS) -o device_lifecycle_state_machine device_lifecycle_state_machine.cpp

clean:
	rm -f device_lifecycle_state_machine
