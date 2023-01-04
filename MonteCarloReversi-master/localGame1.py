#M1161006_cgu_ yeh guan-chih
import Reversi
import monteCarloPlayer

step_count = 0
b = Reversi.Board(10)

players = []
player1 = monteCarloPlayer.myPlayer()
player1.newGame(b._BLACK)
players.append(player1)
player2 = monteCarloPlayer.myPlayer()
player2.newGame(b._WHITE)
players.append(player2)

nextplayer = 0
nextplayercolor = b._BLACK
step_count = 1

while not b.is_game_over():
    print("Board:")
    print(b)
    print("Legal Moves: ", b.legal_moves()) #list 列出broad可動的move，len=0 #pass
    otherplayer = (nextplayer + 1) % 2 #換人條件
    othercolor = b._BLACK if nextplayercolor == b._WHITE else b._WHITE#換色條件

    move = players[nextplayer].getPlayerMove() #print bestmoves、myboard
    (x,y) = move
    if not b.is_valid_move(nextplayercolor,x,y):#可行
        print("Problem: illegal move")
        break
    b.push([nextplayercolor, x, y]) #borad push
    players[otherplayer].playOpponentMove(x,y)#

    nextplayer = otherplayer#換人
    nextplayercolor = othercolor#換色
    step_count += 1
    print(b)


print("The game is over")
print(b)
(nbwhites, nbblacks) = b.get_nb_pieces()
print("Winner: ")
if nbwhites > nbblacks:
    print("WHITE")
elif nbblacks > nbwhites:
    print("BLACK")
else:
    print("DEUCE")

print(step_count)
