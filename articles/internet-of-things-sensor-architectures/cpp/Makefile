CXX = g++
CXXFLAGS = -std=c++17 -Wall -Wextra -O2

all: iot_device_gateway_state_machine

iot_device_gateway_state_machine: iot_device_gateway_state_machine.cpp
	$(CXX) $(CXXFLAGS) iot_device_gateway_state_machine.cpp -o iot_device_gateway_state_machine

clean:
	rm -f iot_device_gateway_state_machine
