CXX ?= c++
CXXFLAGS ?= -Wall -Wextra -O2 -std=c++17

all: fixed_priority_scheduler

fixed_priority_scheduler: fixed_priority_scheduler.cpp
	$(CXX) $(CXXFLAGS) -o fixed_priority_scheduler fixed_priority_scheduler.cpp

clean:
	rm -f fixed_priority_scheduler
