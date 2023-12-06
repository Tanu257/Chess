import numpy
import Algorithms_L
import CONSTANTS
class GammaX1:

    shadowBoard = []
    mainBoard = None
    movablePeices = []
    N_start = 2
    def __init__(self,board,whiteStates,blackStates) -> None:
        self.shadowBoard = board
        self.Algorithms =  Algorithms_L.Algorithms(self.shadowBoard,whiteStates,blackStates)
    def getFinalMove(self,board):
        self.shadowBoard = board
        self.mainBoard = board

        return self.shadowBoard
        
    def DoLocalMoves(self):
        pass

    
    