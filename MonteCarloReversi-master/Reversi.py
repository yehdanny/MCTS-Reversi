#M1161006_cgu_ yeh guan-chih

class Board:
    _BLACK = 1
    _WHITE = 2
    _EMPTY = 0

   
    def __init__(self, boardsize = 8):
      self._nbWHITE = 2
      self._nbBLACK = 2
      self._nextPlayer = self._BLACK
      self._boardsize = boardsize
      self._board = []
      for x in range(self._boardsize):
          self._board.append([self._EMPTY]* self._boardsize)
      _middle = int(self._boardsize / 2)
      self._board[_middle-1][_middle-1] = self._BLACK 
      self._board[_middle-1][_middle] = self._WHITE
      self._board[_middle][_middle-1] = self._WHITE
      self._board[_middle][_middle] = self._BLACK 
      
      self._stack= []
      self._successivePass = 0

    def reset(self):
        self.__init__()

    # 給出棋盤的大小
    def get_board_size(self):
        return self._boardsize

    # 給出棋盤上白色和黑色棋子的數量
    #勝者判斷
    def get_nb_pieces(self):
      return (self._nbWHITE, self._nbBLACK)

    #是否允許玩家在 (x,y) 中玩
    def is_valid_move(self, player, x, y):
        if x == -1 and y == -1:
            return not self.at_least_one_legal_move(player)
        return self.lazyTest_ValidMove(player,x,y)

    def _isOnBoard(self,x,y):
        return x >= 0 and x < self._boardsize and y >= 0 and y < self._boardsize 

    # 如果著法有效則返回要返回的棋子列表
     # 否則返回false
    def testAndBuild_ValidMove(self, player, xstart, ystart):
        if self._board[xstart][ystart] != self._EMPTY or not self._isOnBoard(xstart, ystart):
            return False
    
        self._board[xstart][ystart] = player # On pourra remettre _EMPTY ensuite 
    
        otherPlayer = self._flip(player)
    
        tilesToFlip = [] # Si au moins un coup est valide, on collecte ici toutes les pieces a retourner
        for xdirection, ydirection in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
            x, y = xstart, ystart
            x += xdirection 
            y += ydirection
            if self._isOnBoard(x, y) and self._board[x][y] == otherPlayer:
                # There is a piece belonging to the other player next to our piece.
                x += xdirection
                y += ydirection
                if not self._isOnBoard(x, y):
                    continue
                while self._board[x][y] == otherPlayer:
                    x += xdirection
                    y += ydirection
                    if not self._isOnBoard(x, y): # break out of while loop, then continue in for loop
                        break
                if not self._isOnBoard(x, y):
                    continue
                if self._board[x][y] == player: # We are sure we can at least build this move. Let's collect
                    while True:
                        x -= xdirection
                        y -= ydirection
                        if x == xstart and y == ystart:
                            break
                        tilesToFlip.append([x, y])
    
        self._board[xstart][ystart] = self._EMPTY # restore the empty space
        if len(tilesToFlip) == 0: # If no tiles were flipped, this is not a valid move.
            return False
        return tilesToFlip

    # 與上面相同，但只返回 true/false（允許更快的測試）
    def lazyTest_ValidMove(self, player, xstart, ystart):
        if self._board[xstart][ystart] != self._EMPTY or not self._isOnBoard(xstart, ystart):
            return False
    
        self._board[xstart][ystart] = player # On pourra remettre _EMPTY ensuite 
    
        otherPlayer = self._flip(player)
    
        for xdirection, ydirection in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
            x, y = xstart, ystart
            x += xdirection 
            y += ydirection
            if self._isOnBoard(x, y) and self._board[x][y] == otherPlayer:
                # There is a piece belonging to the other player next to our piece.
                x += xdirection
                y += ydirection
                if not self._isOnBoard(x, y):
                    continue
                while self._board[x][y] == otherPlayer:
                    x += xdirection
                    y += ydirection
                    if not self._isOnBoard(x, y): # break out of while loop, then continue in for loop
                        break
                if not self._isOnBoard(x, y): # On a au moins 
                    continue
                if self._board[x][y] == player: # We are sure we can at least build this move. 
                    self._board[xstart][ystart] = self._EMPTY
                    return True
                 
        self._board[xstart][ystart] = self._EMPTY # restore the empty space
        return False

    def _flip(self, player):
        if player == self._BLACK:
            return self._WHITE 
        return self._BLACK

    def is_game_over(self):
        if self.at_least_one_legal_move(self._nextPlayer):
            return False
        if self.at_least_one_legal_move(self._flip(self._nextPlayer)):
            return False
        return True 

    def push(self, move):
        [player, x, y] = move
        assert player == self._nextPlayer
        if x==-1 and y==-1: # pass
            self._nextPlayer = self._flip(player)
            self._stack.append([move, []])
            return
        toflip = self.testAndBuild_ValidMove(player,x,y)
        self._stack.append([move, toflip])
        self._board[x][y] = player
        for xf,yf in toflip:
            self._board[xf][yf] = self._flip(self._board[xf][yf])
        if player == self._BLACK:
            self._nbBLACK += 1 + len(toflip)
            self._nbWHITE -= len(toflip)
            self._nextPlayer = self._WHITE
        else:
            self._nbWHITE += 1 + len(toflip)
            self._nbBLACK -= len(toflip)
            self._nextPlayer = self._BLACK

    def pop(self):
        [move, toflip] = self._stack.pop()
        [player,x,y] = move
        self._nextPlayer = player 
        if len(toflip) == 0: # pass
            assert x == -1 and y == -1
            return
        self._board[x][y] = self._EMPTY
        for xf,yf in toflip:
            self._board[xf][yf] = self._flip(self._board[xf][yf])
        if player == self._BLACK:
            self._nbBLACK -= 1 + len(toflip)
            self._nbWHITE += len(toflip)
        else:
            self._nbWHITE -= 1 + len(toflip)
            self._nbBLACK += len(toflip)
    # 是否可以採取行動
    def at_least_one_legal_move(self, player):
        for x in range(0,self._boardsize):
            for y in range(0,self._boardsize):
                if self.lazyTest_ValidMove(player, x, y):
                   return True
        return False

    # 返回可能的移動列表
    def legal_moves(self):
        moves = []
        for x in range(0,self._boardsize):
            for y in range(0,self._boardsize):
                if self.lazyTest_ValidMove(self._nextPlayer, x, y):
                    moves.append([self._nextPlayer,x,y])
        if len(moves) is 0:
            moves = [[self._nextPlayer, -1, -1]] # We shall pass
        return moves

    # count chess
    def heuristique(self, player=None):
        if player is None:
            player = self._nextPlayer
        if player is self._WHITE:
            return self._nbWHITE - self._nbBLACK
        return self._nbBLACK - self._nbWHITE

    def _piece2str(self, c):
        if c==self._WHITE:
            return 'O'
        elif c==self._BLACK:
            return 'X'
        else:
            return '.'

    def __str__(self):
        toreturn=""
        for l in self._board:
            for c in l:
                toreturn += self._piece2str(c)
            toreturn += "\n"
        toreturn += "Player: " + ("BLACK" if self._nextPlayer == self._BLACK else "WHITE") + " Move\n"
        toreturn += str(self._nbBLACK) + " blacks and " + str(self._nbWHITE) + " whites on board\n"
        return toreturn

    __repr__ = __str__


