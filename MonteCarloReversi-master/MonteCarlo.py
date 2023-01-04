#M1161006_cgu_ yeh guan-chih
import random
import math


class MonteCarloNode:
    """class node useful for the representation of the tree of moves"""

    def __init__(self, parent, move):
        self.parent = parent
        self.childs = []
        self.move = move
        self.visited = 0
        self.reward = 0
        self.ubc = float("inf")  #UBC1 score

    def update(self, reward):
        self.visited += 1
        self.reward += reward
        self.ubc = self.reward / self.visited + math.sqrt(2*math.log2(self.parent.visited+1)/self.visited) if self.parent != None else 0


class MonteCarloTree:
    """Monte Carlo class with tree walk and random walk methods"""

    def __init__(self, board, color):
        self.board = board
        self.root = MonteCarloNode(None, None)
        self.color = color


    def treeWalk(self, node):

        if node.childs != []: #Bandit-based phase
            best = self.selection(node)
            self.board.push(best.move)
            reward = self.treeWalk(best)
        else: #Random Phase
            self.expansion(node)
            if node.childs == []:
                self.board.push(self.board.legal_moves()[0])
                reward = self.randomWalk()
            else:
                i = random.randint(0, len(node.childs)-1)
                randomChild = node.childs[i]
                self.board.push(randomChild.move)
                reward = self.randomWalk()

        node.update(reward)
        self.board.pop()
        return reward


    def randomWalk(self):
        depth = 0
        while not self.board.is_game_over():
            legalMoves = self.board.legal_moves()
            i = random.randint(0, len(legalMoves)-1)
            randomMove = legalMoves[i]
            self.board.push(randomMove)
            depth += 1

        reward = self.evaluation()
        for i in range(depth):
            self.board.pop()
        return reward


    def selection(self, node):
 
        best_child = node.childs[0]
        best_score = node.childs[0].ubc
        for child in node.childs[1:]:
            if child.ubc > best_score:
                best_score = child.ubc
                best_child = child
        return best_child


    def expansion(self, parent):

        if self.board.is_game_over():
            return

        legalMoves = self.board.legal_moves()
        for move in legalMoves:
            parent.childs.append(MonteCarloNode(parent, move))


    def evaluation(self):

        nbWhite, nbBlack = self.board.get_nb_pieces()
        return 1 if (nbWhite > nbBlack and self.color == 2) or (nbWhite < nbBlack and self.color == 1) else 0
