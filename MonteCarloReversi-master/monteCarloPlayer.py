#M1161006_cgu_ yeh guan-chih
import time
import Reversi
import random
from playerInterface import *
from MonteCarlo import MonteCarloNode
from MonteCarlo import MonteCarloTree

BOARDSIZE = 8
SEED = 13459
HASHSIZE = 100000
#hashTable = HashTable(HASHSIZE)

DEADLINE = round(time.time()*1000) + 1000*60*5  #5 minutes deadline

class myPlayer(PlayerInterface):

    def __init__(self):
        self._board = Reversi.Board(10)
        self._mycolor = None
        self._name = "Player"
        self._startFlag = 0
        self.deadline = 9999


    def getPlayerName(self):
        return self._name

    def getPlayerMove(self):
        #initialize the deadline
        if self._startFlag == 0:
            self._deadline = DEADLINE
            self._startFlag = 1

        if self._board.is_game_over():
            print("Game is over!")
            return (-1,-1)


        #if there is not enough time -> random
        if (self._startFlag):
            if (self._deadline - time.time() < 1000):
                moves = self._board.legal_moves()
                (c, x, y) = moves[random.randint(0, len(moves)-1)]
                return (x, y)

        bestMove = self.monteCarloSearch()
        self._board.push(bestMove)

        print("I am playing ", bestMove)
        (c,x,y) = bestMove
        assert(c == self._mycolor)
        print("My current board :")
        print(self._board)

        return (x,y)

    def playOpponentMove(self, x, y):
        assert(self._board.is_valid_move(self._opponent, x, y))
        print("Opponent played ", (x,y))
        self._board.push([self._opponent, x, y])

    def newGame(self, color):
        self._mycolor = color
        self._opponent = 1 if color == 2 else 2

    def endGame(self, winner):
        if self._mycolor == winner:
            print("I won!!!")
        else:
            print("I lost!!")


    """ MONTE CARLO """
    def monteCarloSearch(self):

        mct = MonteCarloTree(self._board, self._mycolor)

        endTime = round(time.time()*1000.0) + 1000.0  #1s
        while (round(time.time()*1000.0) < endTime):
            mct.treeWalk(mct.root)

        return mct.selection(mct.root).move
