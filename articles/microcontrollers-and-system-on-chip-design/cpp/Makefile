CXX ?= c++
CXXFLAGS ?= -Wall -Wextra -O2 -std=c++17

all: silicon_fit_evaluator

silicon_fit_evaluator: silicon_fit_evaluator.cpp
	$(CXX) $(CXXFLAGS) -o silicon_fit_evaluator silicon_fit_evaluator.cpp

clean:
	rm -f silicon_fit_evaluator
