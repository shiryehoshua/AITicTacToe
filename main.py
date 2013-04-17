#!/usr/bin/python

import sys
import Graph

def main():
  if (len(sys.argv) != 2):
    print "usage: python main.py [filename]"
    return

  fp = open (sys.argv[1], 'r')
  numNodes = int(fp.readline().strip())
  winningSet = []
  for line in fp:
    winningSet.append(line.split())
  fp.close()

  # Create a game
  game = Graph.TicTacToeGame(numNodes, winningSet)
  
  print "Initializing...(this could take a while with >10 nodes)"
  # Run the algorithm once, effectively setting up the graph.
  game.getMaxConfiguration(game.curConf)

  print "Let's play! You'll be 'O', and I'll be 'X'. I'll go first."

  while (not game.isDone()):
    # Print the board
    print "Current board:"
    print str(game)

    # Determine who's turn it is and act accordingly
    if (game.nextPlayer() == Graph.COMPUTER):
      if not game.playBestMove():
        break

    else:
      print "It's your turn!"
      print game.labeledBoardString()
      box = raw_input("Enter which box you'd like to play, or type W to see wins: ")
      if box == 'W':
        for winS in game.winningBoardsStrings():
          print winS
      else:
        valid = game.userPlayed(box.strip()) 
        if not valid:
          print "Woops, please enter 'W' or a number 1 through " + str(game.numNodes) + "!"
          print "Why don't you try again."

  print str(game)
  winner = game.getWinner()
  if winner == Graph.NOBODY:
    print "Cat's game!"
  elif winner == Graph.COMPUTER:
    print "I win!"
  elif winner == Graph.USER:
    print "You win!"
  else:
    print "The winner is..." + Graph.getPlayerString(winner)

main()
