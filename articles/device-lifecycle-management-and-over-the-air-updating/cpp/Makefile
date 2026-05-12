CXX = g++
CXXFLAGS = -std=c++17 -Wall -Wextra -O2

all: staged_rollout_planner

staged_rollout_planner: staged_rollout_planner.cpp
	$(CXX) $(CXXFLAGS) staged_rollout_planner.cpp -o staged_rollout_planner

clean:
	rm -f staged_rollout_planner
