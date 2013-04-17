#!/usr/bin/python

import sys
import math
import copy
from random import randint

# These are ranked according to worst possible:
#   It is the absolute worst to lose,
#   then to tie,
#   Then to win.
COMPUTER = 1
USER = -1 
NOBODY = 0
MIN = 'min'
MAX = 'max'

# Helper methods (mostly for debugging)
def getPlayerString(player):
  if player == COMPUTER:
    return "X"
  elif player == USER:
    return "O"
  elif player == NOBODY:
    return "-"
  else:
    return str(player)

def getConfigDictString(config, nextPlayer):
  numNodes = len(config)
  dimBoard = int(math.ceil(math.sqrt(numNodes)))

  s = ""
  if nextPlayer != NOBODY:
    s += "next player: " + getPlayerString(nextPlayer) + "\n"
  for i in range(1, numNodes + 1):
    if i % dimBoard == 0:
      s += getPlayerString(config[str(i)]) + "\n"
    else:
      s += getPlayerString(config[str(i)]) + " | "
  if s[-1] != '\n':
    s += "\n"
  return s 

# A BoardConfiguration contains information about the following:
#   - The configuration of the board:
#       - Each board is made up of boxes, and each box is either
#           0 (nobody has played yet)
#           1 (the computer has played here)
#           2 (the user has played here)
#       - Each board has a nextPlayer variable
#   - The name of the configuration (mostly for debugging purposes.)
class BoardConfiguration:
  def __init__(self, nextPlayer, configuration):
    # Every node has a game configuration which we initialize
    # to a board full of NOBODYs. The computer plays with the value 
    # COMPUTER, and the user plays with the value USER.
    # We set the board so that each box is labeled with a string
    # of the integers 1..numNodes
    self.board = configuration

    # We calculate whether or not this is a terminal board later
    # and store that result here.
    self.terminal = None

    # We use this field to keep track of all outgoing edges. The
    # key is the vertex object itself, while the value associated
    # with each vertex is that particular edge's weight.
    self.neighbors = {}

    # We use this to keep track of whose turn it is next
    self.nextPlayer = nextPlayer

    # We initialize the winner to no one, and fill this later
    self.winner = None

  def __str__(self):
    return getConfigDictString(self.board, self.nextPlayer)

  def __getitem__(self, item):
    return self.board[item]

  def playerAfterNext(self):
    if self.nextPlayer == COMPUTER:
      return USER
    else:
      return COMPUTER

  # A configuartion of the game is a winning game if
  # all the elements of a winning set are held
  # by the same person.
  def isWin(self, winningSet):
    # We cache our results to make life easier
    if self.winner != None:
      return self.winner != NOBODY

    # Iterate through all possible configurations of wins
    for win in winningSet:
      # In the first iteration, set the potential winner
      winner = self.board[win[0]]

      # Check that the boxes are occupied by the same player
      for box in win:
        if winner != self.board[box]:
          winner = NOBODY
      
      # At this point the winner is either a player, or nobody. If
      # it is a specific player, then we don't need to search anymore.
      if winner != NOBODY:
        self.winner = winner
        break
    
    # If the winner variable was filled, we have found a winner!
    if self.winner != None:
      return self.winner != NOBODY

  # A vertex or configuration of the game is terminal when
  # all of the boxes have been filled, or the configuration is a
  # winning configuration.
  def isTerminal(self, winningSet):
    # Cache our results
    if self.terminal != None:
      return self.terminal

    # If it is a win, the game is done.
    if self.isWin(winningSet):
      self.terminal = True
      return self.terminal

    # Otherwise, we keep going until all the boxes are filled.
    for box in self.board:
      if self.board[box] == NOBODY:
        self.terminal = False
        return self.terminal

    # If we have made it this far it is because the board is
    # filled and it's a Cat's game.
    self.winner = NOBODY
    self.terminal = True
    return self.terminal

  # Orchestrates a "play", where the given player plays
  # in the given box.
  # Returns None if:
  #   - The player is not the next player
  #   - The given box is already taken
  # Returns the next configuration if the two checks
  # above pass.
  def play(self, player, box):
    # Check that the player is valid, and that the box is not taken.
    if player != self.nextPlayer or self.board[box] != NOBODY:
      return None

    # Create a new configuration where the box given has
    # been played by the player, and the next player is 
    # properly set.
    newConfig = self.board
    newConfig[box] = player
    nextConfig = BoardConfiguration(\
                   str(str(player) + " played on " + str(box)),\
                   COMPUTER if player == USER else USER, 
                   self.newConfig)

    return nextConfig

  def getPlayerInBox(self, box):
    return self[str(box)]


class TicTacToeGame:
  def __init__(self, numNodes, winningSet):
    # Setting the root to be an empty board, with the
    # computer as the next player.
    initConfig = {}
    for i in range(1, numNodes + 1):
      initConfig[str(i)] = NOBODY
    self.root = BoardConfiguration(COMPUTER, initConfig)

    # Remembering the number of nodes to make things faster
    # later
    self.numNodes = numNodes

    # Set our winning set
    self.winningSet = winningSet

    # The current configuration
    self.curConf = self.root
    self.lastConf = None
    self.lastLastConf = None


    # Keep track of all the configurations
    self.configurations = {}
    self.configurations[str(self.root)] = self.root

    # For caching later on
    self.minMaxVals = {}

  # Returns a list of neighbors. Returns an empty list if the
  # vertex has no neighbors
  def getNeighbors(self, config):
    if not (config.neighbors or len(config.neighbors) != 0):
      self.generateNeighbors(config)
    return config.neighbors.values()

  # Generates all possible "next" moves
  def generateNeighbors(self, config):
    for box in config.board:
      if config.board[box] == NOBODY:
        self.addNeighbor(config, box)

  # Add a neighbor with a certain box filled out
  def addNeighbor(self, config, box):
    if config.isTerminal(self.winningSet):
      return

    # Create the new configuration dict
    newConf = copy.deepcopy(config.board)
    newConf[box] = config.nextPlayer
    newNextPlayer = config.playerAfterNext()

    # See if this configuration is already in our graph
    key = getConfigDictString(newConf, newNextPlayer)
    if key in self.configurations:
      newBoardConf = self.configurations[key]

    # If the configuration is not in the graph, create one
    else:
      newBoardConf = \
        BoardConfiguration(newNextPlayer, \
                           newConf) 
      self.configurations[key] = newBoardConf

    # Set the connections
    config.neighbors[config.nextPlayer, box] = newBoardConf

  def __str__(self):
    return str(self.curConf)

  def winningBoardsStrings(self):
    winningStrings = []
    for win in self.winningSet:
      configDict = {}
      for i in range(1, self.numNodes + 1):
        if str(i) in win:
          configDict[str(i)] = 'W'
        else:
          configDict[str(i)] = NOBODY

      winningStrings.append(getConfigDictString(configDict, NOBODY))

    return winningStrings

  def labeledBoardString(self):
    labeledBoard = {}
    for i in range(1, self.numNodes+1):
      labeledBoard[str(i)] = str(i)
    return getConfigDictString(labeledBoard, \
                               NOBODY)

  def isDone(self):
    if self.curConf.isTerminal(self.winningSet):
      return True

    else:
      return False

  def nextPlayer(self):
    return self.curConf.nextPlayer

  # Orchestrates a "play", where the player plays in the
  # given box. 
  # Returns True if the play was succesful, False otherwise
  def playMove(self, player, box):
    if (player, box) in self.curConf.neighbors:
      nextConfiguration = self.curConf.neighbors[player , box]
      return self.play(nextConfiguration)
    else:
      return False

  # Attempts to play the given next configuration
  # Returns True if the play was succesful, False otherwise
  def play(self, nextConfiguration):
    # Make sure the move was valid
    if nextConfiguration not in self.curConf.neighbors.values():
      return False

    # If the move was valid, move the game forward
    self.lastLastConf = self.lastConf
    self.lastConf = self.curConf
    self.curConf = nextConfiguration

    return True

  def minMaxInternal(self, configuration):
    # Cache the values for speed
    if configuration in self.minMaxVals:
      return self.minMaxVals[configuration]

    if configuration.isTerminal(self.winningSet):
      return int(configuration.winner)

    alpha = -configuration.nextPlayer * 10000000000

    for n in self.getNeighbors(configuration):
      score = self.minMaxInternal(n)
       
      alpha = int(configuration.nextPlayer==1 and max(alpha,score) or min(alpha, score))
    self.minMaxVals[configuration] = alpha
    return alpha

  def getMaxConfiguration(self, configuration):
    bestConfig = None
    bestScore = -100
    for n in self.getNeighbors(configuration):
      score = self.minMaxInternal(n)
      if score > bestScore:
        bestConfig = n
        bestScore = score

    return bestConfig

  def playBestMove(self):
    bestNextConfiguration = None
    
    # Since it is the computer's turn, we are looking to
    # maximize.
    bestNextConfiguration = self.getMaxConfiguration(self.curConf)

    if not self.play(bestNextConfiguration):
      print "OH NO! I'm afraid something has gone wrong..."
      return False
    return True

  def userPlayed(self, box):
    nextConf = None
    if (USER, box) in self.curConf.neighbors:
      nextConf = self.curConf.neighbors[USER, box]
    if nextConf:
      self.curConf = nextConf
      return True
    else:
      return False

  def getWinner(self):
   return self.curConf.winner

  def getWinnerString(self):
    return getPlayerString(self.curConf.winner)

# For testing
def testInitialize(numNodes, numWins, sizeWin):
  winningSet = []

  # Create numWins arbitrary 'wins'
  while len(winningSet) < numWins:
    win = []
    while len(win) < sizeWin:
      x = randint(1, sizeWin)
      if x not in win:
        win.append(str(x))
    winningSet.append(win)

  # Create game
  game = TicTacToeGame(numNodes, winningSet)
  
  # Run initialization
  print "initializing..."
  game.getMaxConfiguration(game.curConf)
    
    

