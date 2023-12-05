import pygame
import CONSTANTS
import numpy
import math
from Piece import Piece
import threading
from SideWindow import Swind
import Algorithms_L

class Board:
    Loc = []
    main_surface = None
    selectedTile = None
    Pieces = []
    curruntSide = 0
    isHovered = False
    toMovePiece = None

    GameWinner = None
    isGameOver = False
    whiteStates = {"side":"white"}
    blackStates = {"side":"black"}
    

    def __init__(self, surface: pygame.Surface) -> None:
        self.main_surface = surface
        self.Wthread= threading.Thread(target=(Swind(self.whiteStates).runSwind))
        self.Wthread.start()
        self.Bthread = threading.Thread(target=(Swind(self.blackStates).runSwind))
        self.Bthread.start()
        self.font = pygame.font.Font(None, CONSTANTS.font_size)

    def startOver(self):
        self.LoadPieces()
        self.Loc = []
        self.selectedTile = None
        self.curruntSide = 0
        self.isHovered = False
        self.toMovePiece = None

        self.GameWinner = None
        self.isGameOver = False
        self.Algorithms =  Algorithms_L.Algorithms(self.Pieces,self.whiteStates,self.blackStates)

    def drawBackground(self):
        for x in range(0, 8):
            for y in range(0, 8):
                Pos = CONSTANTS.PointToPos(x, y)
                if (x+y) % 2 != 0:
                    pygame.draw.rect(self.main_surface, CONSTANTS.BLACK, pygame.Rect(
                        Pos[0], Pos[1], CONSTANTS.TILESIZE, CONSTANTS.TILESIZE))
                else:
                    pygame.draw.rect(self.main_surface, CONSTANTS.WHITE, pygame.Rect(
                        Pos[0], Pos[1], CONSTANTS.TILESIZE, CONSTANTS.TILESIZE))

    def drawGame(self):
        if not self.isGameOver :
            self.drawBackground()
            self.drawPieces()
            self.drawIndicators()
            self.GameOverScreen()
        else:
            self.GameOverScreen()
            
    def GameOverScreen(self):
        winnerText = None
        if self.GameWinner == 0:
            winnerText = "White Won The Game! Press Space To Rematch"
        elif self.GameWinner == 1:
            winnerText = "Black Won The Game! Press Space To Rematch"

        text_surface = self.font.render(winnerText, True, CONSTANTS.TEXTCOLOR)
        self.main_surface.blit(text_surface, (50, 250))

    def drawIndicators(self):
        if self.isHovered:
            for tile in self.indicatedTiles:
                Pos = CONSTANTS.PointToPos(tile[0],tile[1])
                IndiSurface = pygame.Surface((CONSTANTS.TILESIZE,CONSTANTS.TILESIZE), pygame.SRCALPHA)
                pygame.draw.circle(IndiSurface,CONSTANTS.HIGHLIGHTER,(CONSTANTS.TILESIZE/2,CONSTANTS.TILESIZE/2),CONSTANTS.INDICATOR_CIRCLE_RADIUS)

                self.main_surface.blit(IndiSurface,Pos)
                
    def drawPieces(self):
        for x in range(0, 8):
            for y in range(0, 8):
                if self.Pieces[x][y] != 0:
                    Pos = CONSTANTS.PointToPos(x, y)
                    self.main_surface.blit(
                        self.Pieces[x][y].image, (Pos[0], Pos[1]))

    def SetMouseClickedTile(self, pos):
        if not self.isGameOver:
            tileX = math.floor(pos[0]/CONSTANTS.TILESIZE)
            tileY = math.floor(pos[1]/CONSTANTS.TILESIZE)
            gotTile = self.Algorithms.getTile([tileX, tileY])
            if self.toMovePiece == None:
                if gotTile != 0:
                    if gotTile.side == self.curruntSide:
                        self.HoverPiece(tileX, tileY)
                    else:
                        self.isHovered = False
                else:
                    self.isHovered = False

            elif self.toMovePiece != None:
                if gotTile != 0:
                    if gotTile.side == self.curruntSide:
                        self.HoverPiece(tileX, tileY)
                    else:
                        self.MovePiece(tileX, tileY)
                else:
                    self.MovePiece(tileX, tileY)
                    self.isHovered = False

    def HoverPiece(self, tileX, tileY):
        self.toMovePiece = tileX, tileY
        self.indicatedTiles = self.Algorithms.getMovables(self.toMovePiece,self.curruntSide)
        self.isHovered = True

    def MovePiece(self, x2, y2):
        toMovePiece = self.Algorithms.getTile(self.toMovePiece)
        Movables = self.indicatedTiles
        self.CoreChange([x2, y2], Movables, toMovePiece)

        if y2 == 0 and toMovePiece.pid == CONSTANTS.PIECE_IDS["Pawn"] and toMovePiece.side == 0:
            self.Algorithms.TransformPawn(x2,y2,toMovePiece.side)
        if y2 == 7 and toMovePiece.pid == CONSTANTS.PIECE_IDS["Pawn"] and toMovePiece.side == 1:
            self.Algorithms.TransformPawn(x2,y2,toMovePiece.side)

    def CoreChange(self, temp_l, Movables, toMovePiece):
        x2 = temp_l[0]
        y2 = temp_l[1]
        if temp_l in Movables:

            if self.Algorithms.getTile(temp_l) == 0:
                self.Pieces[x2][y2] = toMovePiece
                self.Pieces[self.toMovePiece[0]][self.toMovePiece[1]] = 0
                self.toMovePiece = None

            elif self.Algorithms.getTile(temp_l) != 0:
                if self.Pieces[x2][y2].pid == 0:
                    self.GameWinner = self.changeSide
                    self.isGameOver = True
                    
                self.Pieces[x2][y2] = toMovePiece
                self.Pieces[self.toMovePiece[0]][self.toMovePiece[1]] = 0
                self.toMovePiece = None

            self.Pieces[x2][y2].hasMoved = True
            self.changeSide()
        self.isHovered = False

    def LoadPieces(self):
        # Creating Temperory List
        tempPis = numpy.zeros((8, 8)).tolist()

        # Loading Kings
        tempPis[4][7] = Piece(CONSTANTS.PIECE_IDS["King"], 0)
        tempPis[4][0] = Piece(CONSTANTS.PIECE_IDS["King"], 1)

        # Loading Pawns

        tempPis[5][5] = Piece(CONSTANTS.PIECE_IDS["Pawn"], 1)

        tempPis[3][2] = Piece(CONSTANTS.PIECE_IDS["Pawn"], 0)

        self.Pieces = tempPis

    def changeSide(self):
            if self.curruntSide == 1:
                self.curruntSide = 0
            else:
                self.curruntSide = 1