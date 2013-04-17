#!/usr/bin/python

import sys
import Graph

# python -m cProfile test.py numNodes numWins sizeWin

def main():
  if len(sys.argv) != 4:
    print "usage: python test.py numNodes, numWins, sizeWin"
    return
  
  # Call our initialize test function with 
  Graph.testInitialize(int(sys.argv[1]), \
                       int(sys.argv[2]), \
                       int(sys.argv[3]))

main()
