CXX      = g++
CXXFLAGS = -std=c++17 -O2 -Wall

all: mochila_pd mochila_bt mochila_bb

mochila_pd: mochila_pd.cpp
	$(CXX) $(CXXFLAGS) -o $@ $<

mochila_bt: mochila_bt.cpp
	$(CXX) $(CXXFLAGS) -o $@ $<

mochila_bb: mochila_bb.cpp
	$(CXX) $(CXXFLAGS) -o $@ $<

clean:
	rm -f mochila_pd mochila_bt mochila_bb

.PHONY: all clean
