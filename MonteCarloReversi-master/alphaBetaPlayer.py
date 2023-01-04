#M1161006_cgu_ yeh guan-chih
import time
import Reversi
import random
import sys
from playerInterface import *


BOARDSIZE = 8
SEED = 13459
HASHSIZE = 100000
DEADLINE = round(time.time()*1000) + 1000*60*5

class myPlayer(PlayerInterface):

    def __init__(self):
        self._board = Reversi.Board(10)
        self._mycolor = None
        self._name = "The Punisher"
        self._startFlag = 0
        self.deadline = 9999
        self._eval = [[35,-4,0,12,10,10,12,0,-4,35],
                       [-4,-6,1,1,1,1,1,1,-6,-4],
                       [0,0,1,1,1,1,1,1,0,0],
                       [12,1,1,4,3,3,4,1,1,12],
                       [10,1,1,3,2,2,3,1,1,10],
                       [10,1,1,3,2,2,3,1,1,10],
                       [12,1,1,4,3,3,4,1,1,12],
                       [0,0,1,1,1,1,1,1,0,0],
                       [-6,-8,1,1,1,1,1,1,-8,-6],
                       [35,-6,0,12,10,10,12,0,-6,35]]

    def getPlayerName(self):
        return self._name

    def getPlayerMove(self):
        #initialize the deadline
        if self._startFlag == 0:
            self._deadline = DEADLINE
            self._startFlag = 1

        if self._board.is_game_over():
            print("Referee told me to play but the game is over!")
            return (-1,-1)


        #if there is not enough time -> random
        if (self._startFlag):
            if (self._deadline - time.time() < 1000):
                moves = self._board.legal_moves()
                (c, x, y) = moves[random.randint(0, len(moves)-1)]
                return (x, y)

        endTime = round(time.time()*1000.0) + 1000.0
        maxi = -2**31
        bestMove = [self._board._nextPlayer, -1, -1]
        depth = 3

        #Progressive deepening
        while(round(time.time()*1000.0) < endTime):
            result = self.search(self._board, depth, endTime)
            if (result[0] > maxi):
                bestMove = result[1]
            depth += 1
        print("DEPTH : ", depth)
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
            print("I lost :(!!")


    def search(self, b, maxDepth, endTime):

        maxi = -2**31
        bestMove = [b._nextPlayer, -1, -1]
        alpha = -2**31
        beta = 2**31

        moves = b.legal_moves()
        # self.quickSort(b, moves, 0, len(moves) - 1)

        for move in moves :
            if (time.time()*1000.0 > endTime):
                break;

            b.push(move)

            score = self.jouerMin(b, maxDepth - 1, alpha, beta)
            if (score > maxi):
                maxi = score
                bestMove = move

            b.pop()

        return (maxi, bestMove)


    def jouerMax(self, b, depth, alpha, beta):

        if (depth == 0):
            return self.heuristique(b._nextPlayer)

        maxi = -2**31
        for move in b.legal_moves() :
            b.push(move)
            maxi = max(maxi, self.jouerMin(b, depth - 1, alpha, beta))
            b.pop()

            alpha = max(alpha, maxi)
            if alpha >= beta:
                break  # beta cut-off

        return maxi


    def jouerMin(self, b, depth, alpha, beta):

        if (depth == 0):
            return self.heuristique(b._nextPlayer)

        mini = 2**31
        for move in b.legal_moves() :
            b.push(move)
            mini = min(mini, self.jouerMax(b, depth - 1, alpha, beta))
            b.pop()

            beta = min(beta, mini)
            if alpha >= beta:
                break  # alpha cut-off

        return mini



    def heuristique(self, player=None):
        if player is None:
            player = self._board._nextPlayer

        ############################
        ####### Coin Parity ########
        ############################
        if player is self._board._WHITE:
            cp =  (self._board._nbWHITE - self._board._nbBLACK) / (self._board._nbWHITE + self._board._nbBLACK)
        else:
            cp =  (self._board._nbBLACK - self._board._nbWHITE) / (self._board._nbBLACK + self._board._nbWHITE)



        ############################
        #### Corner occupancy ######
        ############################
        my_corners = 0
        opp_corners = 0
        boardsize = self._board._boardsize

        if player is self._board._WHITE:
            if self._board._board[0][0] == self._board._WHITE: my_corners += 1
            elif self._board._board[0][0] == self._board._BLACK: opp_corners += 1

            if self._board._board[0][boardsize - 1] == self._board._WHITE: my_corners += 1
            elif self._board._board[0][boardsize - 1] == self._board._BLACK: opp_corners += 1

            if self._board._board[boardsize - 1][0] == self._board._WHITE: my_corners += 1
            elif self._board._board[boardsize - 1][0] == self._board._BLACK: opp_corners += 1

            if self._board._board[boardsize - 1][boardsize - 1] == self._board._WHITE: my_corners += 1
            elif self._board._board[boardsize - 1][boardsize - 1] == self._board._BLACK: opp_corners += 1

        else:
            if self._board._board[0][0] == self._board._BLACK: my_corners += 1
            elif self._board._board[0][0] == self._board._WHITE: opp_corners += 1

            if self._board._board[0][boardsize - 1] == self._board._BLACK: my_corners += 1
            elif self._board._board[0][boardsize - 1] == self._board._WHITE: opp_corners += 1

            if self._board._board[boardsize - 1][0] == self._board._BLACK: my_corners += 1
            elif self._board._board[boardsize - 1][0] == self._board._WHITE: opp_corners += 1

            if self._board._board[boardsize - 1][boardsize - 1] == self._board._BLACK: my_corners += 1
            elif self._board._board[boardsize - 1][boardsize - 1] == self._board._WHITE: opp_corners += 1


        co = 25 * (my_corners - opp_corners)


        ############################
        ##### Corner closeness #####
        ############################
        my_close_corners = 0
        opp_close_corners = 0

        if player is self._board._WHITE:
            if (self._board._board[0][0] == self._board._EMPTY):
                if self._board._board[0][1] == self._board._WHITE: my_close_corners += 1
                elif self._board._board[0][1] == self._board._BLACK: opp_close_corners += 1
                if self._board._board[1][0] == self._board._WHITE: my_close_corners += 1
                elif self._board._board[1][0] == self._board._BLACK: opp_close_corners += 1
                if self._board._board[1][1] == self._board._WHITE: my_close_corners += 1
                elif self._board._board[1][1] == self._board._BLACK: opp_close_corners += 1

            if (self._board._board[0][boardsize - 1] == self._board._EMPTY):
                if self._board._board[0][boardsize - 2] == self._board._WHITE: my_close_corners += 1
                elif self._board._board[0][boardsize - 2] == self._board._BLACK: opp_close_corners += 1
                if self._board._board[1][boardsize - 2] == self._board._WHITE: my_close_corners += 1
                elif self._board._board[1][boardsize - 2] == self._board._BLACK: opp_close_corners += 1
                if self._board._board[1][boardsize - 1] == self._board._WHITE: my_close_corners += 1
                elif self._board._board[1][boardsize - 1] == self._board._BLACK: opp_close_corners += 1

            if (self._board._board[boardsize - 1][0] == self._board._EMPTY):
                if self._board._board[boardsize - 2][0] == self._board._WHITE: my_close_corners += 1
                elif self._board._board[boardsize - 2][0] == self._board._BLACK: opp_close_corners += 1
                if self._board._board[boardsize - 2][1] == self._board._WHITE: my_close_corners += 1
                elif self._board._board[boardsize - 2][1] == self._board._BLACK: opp_close_corners += 1
                if self._board._board[boardsize - 1][1] == self._board._WHITE: my_close_corners += 1
                elif self._board._board[boardsize - 1][1] == self._board._BLACK: opp_close_corners += 1

            if (self._board._board[boardsize - 1][boardsize - 1] == self._board._EMPTY):
                if self._board._board[boardsize - 1][boardsize - 2] == self._board._WHITE: my_close_corners += 1
                elif self._board._board[boardsize - 1][boardsize - 2] == self._board._BLACK: opp_close_corners += 1
                if self._board._board[boardsize - 2][boardsize - 1] == self._board._WHITE: my_close_corners += 1
                elif self._board._board[boardsize - 2][boardsize - 1] == self._board._BLACK: opp_close_corners += 1
                if self._board._board[boardsize - 2][boardsize - 2] == self._board._WHITE: my_close_corners += 1
                elif self._board._board[boardsize - 2][boardsize - 2] == self._board._BLACK: opp_close_corners += 1

        else:
            if (self._board._board[0][0] == self._board._EMPTY):
                if self._board._board[0][1] == self._board._BLACK: my_close_corners += 1
                elif self._board._board[0][1] == self._board._WHITE: opp_close_corners += 1
                if self._board._board[1][0] == self._board._BLACK: my_close_corners += 1
                elif self._board._board[1][0] == self._board._WHITE: opp_close_corners += 1
                if self._board._board[1][1] == self._board._BLACK: my_close_corners += 1
                elif self._board._board[1][1] == self._board._WHITE: opp_close_corners += 1

            if (self._board._board[0][boardsize - 1] == self._board._EMPTY):
                if self._board._board[0][boardsize - 2] == self._board._BLACK: my_close_corners += 1
                elif self._board._board[0][boardsize - 2] == self._board._WHITE: opp_close_corners += 1
                if self._board._board[1][boardsize - 2] == self._board._BLACK: my_close_corners += 1
                elif self._board._board[1][boardsize - 2] == self._board._WHITE: opp_close_corners += 1
                if self._board._board[1][boardsize - 1] == self._board._BLACK: my_close_corners += 1
                elif self._board._board[1][boardsize - 1] == self._board._WHITE: opp_close_corners += 1

            if (self._board._board[boardsize - 1][0] == self._board._EMPTY):
                if self._board._board[boardsize - 2][0] == self._board._BLACK: my_close_corners += 1
                elif self._board._board[boardsize - 2][0] == self._board._WHITE: opp_close_corners += 1
                if self._board._board[boardsize - 2][1] == self._board._BLACK: my_close_corners += 1
                elif self._board._board[boardsize - 2][1] == self._board._WHITE: opp_close_corners += 1
                if self._board._board[boardsize - 1][1] == self._board._BLACK: my_close_corners += 1
                elif self._board._board[boardsize - 1][1] == self._board._WHITE: opp_close_corners += 1

            if (self._board._board[boardsize - 1][boardsize - 1] == self._board._EMPTY):
                if self._board._board[boardsize - 1][boardsize - 2] == self._board._BLACK: my_close_corners += 1
                elif self._board._board[boardsize - 1][boardsize - 2] == self._board._WHITE: opp_close_corners += 1
                if self._board._board[boardsize - 2][boardsize - 1] == self._board._BLACK: my_close_corners += 1
                elif self._board._board[boardsize - 2][boardsize - 1] == self._board._WHITE: opp_close_corners += 1
                if self._board._board[boardsize - 2][boardsize - 2] == self._board._BLACK: my_close_corners += 1
                elif self._board._board[boardsize - 2][boardsize - 2] == self._board._WHITE: opp_close_corners += 1

        cc = -12.5 * (my_close_corners - opp_close_corners);

        ############################
        ######### Mobility #########
        ############################
        moves = self._board.legal_moves()
        my_mobility = len(moves)
        opp_mobility = 0

        for move in moves:
            self._board.push(move)
            opp_mobility += len(self._board.legal_moves())
            self._board.pop()
        opp_mobility = opp_mobility / my_mobility

        if my_mobility + opp_mobility != 0:
            m = (my_mobility - opp_mobility) / (my_mobility + opp_mobility)
        else:
            m = 0

        ############################
        ######### End game #########
        ############################
        if (self._board.is_game_over()):
            end_game = 100000
        else:
            end_game = 0


        return 100 * cp + (800 * co) + (300 * cc) + end_game + (200 * m)

    def heuristique(self, player=None):
        if player is None:
            player = self._nextPlayer
        if player is self._board._WHITE:
            return self._board._nbWHITE - self._board._nbBLACK
        return self._board._nbBLACK - self._board._nbWHITE
