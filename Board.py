import pygame
import CONSTANTS
import numpy
import math
from Piece import Piece
import pgu.gui as gui
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
   

    def __init__(self, surface: pygame.Surface) -> None:
        self.main_surface = surface
    
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
            gotTile = self.getTile([tileX, tileY])
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
        self.indicatedTiles = self.getMovables()
        self.isHovered = True

    def MovePiece(self, x2, y2):
        toMovePiece = self.getTile(self.toMovePiece)

        Movables = self.indicatedTiles
        self.CoreChange([x2, y2], Movables, toMovePiece)

        if y2 == 0 and toMovePiece.pid == CONSTANTS.PIECE_IDS["Pawn"] and toMovePiece.side == 0:
            self.TransformPawn(x2,y2,toMovePiece.side)
        if y2 == 7 and toMovePiece.pid == CONSTANTS.PIECE_IDS["Pawn"] and toMovePiece.side == 1:
            self.TransformPawn(x2,y2,toMovePiece.side)


    def getMovables(self):
        toMovePiece = self.getTile(self.toMovePiece)
        Movables = []
        if toMovePiece.pid == CONSTANTS.PIECE_IDS["Pawn"]:

            Movables = self.Algo_Pawn(
                self.toMovePiece[0], self.toMovePiece[1])
        elif toMovePiece.pid == CONSTANTS.PIECE_IDS["Bishop"]:

            Movables = self.FindAngle45(
                self.toMovePiece[0], self.toMovePiece[1],8)

        elif toMovePiece.pid == CONSTANTS.PIECE_IDS["Rook"]:

            Movables = self.Algo_Rook(
                self.toMovePiece[0], self.toMovePiece[1])

        elif toMovePiece.pid == CONSTANTS.PIECE_IDS["Queen"]:

            Movables = self.Algo_Queen(
                self.toMovePiece[0], self.toMovePiece[1])

        elif toMovePiece.pid == CONSTANTS.PIECE_IDS["Knight"]:

            Movables = self.Algo_Knight(
                self.toMovePiece[0], self.toMovePiece[1])
        elif toMovePiece.pid == CONSTANTS.PIECE_IDS['King']:
            Movables =  self.Algo_King(
                self.toMovePiece[0], self.toMovePiece[1])
        return Movables

    def CoreChange(self, temp_l, Movables, toMovePiece):
        x2 = temp_l[0]
        y2 = temp_l[1]
        if temp_l in Movables:

            if self.getTile(temp_l) == 0:
                self.Pieces[x2][y2] = toMovePiece
                self.Pieces[self.toMovePiece[0]][self.toMovePiece[1]] = 0
                self.toMovePiece = None

            elif self.getTile(temp_l) != 0:
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

        # Loading Queens
        # Loading Pawns

        tempPis[5][5] = Piece(CONSTANTS.PIECE_IDS["Pawn"], 1)

        tempPis[3][2] = Piece(CONSTANTS.PIECE_IDS["Pawn"], 0)

        self.Pieces = tempPis

    def TransformPawn(self,x2,y2,side):
        choice = CONSTANTS.PIECE_IDS["Rook"]
        
        self.Pieces[x2][y2] = Piece(choice,side)


 # ------ AlgoRithms ------

    def isUnderCheck(self):            
        pass
    def Algo_Pawn(self, x, y):

        foundTiles = []

        curruntTile = self.getTile([x, y])
        toUp = 1

        if curruntTile.hasMoved:
            toUp = 1
        else:
            toUp = 2
        foundTiles.extend(self.FindAngle90(x, y,  toUp, True))
        foundTiles.extend(self.FindAngle45(x, y,  2, True))

        return foundTiles

    def Algo_Rook(self, x, y):

        foundTiles = []

        foundTiles.extend(self.FindAngle90(x, y,  8, False))
        foundTiles.extend(self.FindAngle0(x, y,  8))

        return foundTiles

    def Algo_Queen(self, x, y):

        foundTiles = []

        foundTiles.extend(self.FindAngle0(x, y,  8))
        foundTiles.extend(self.FindAngle90(x, y,  8, False))
        foundTiles.extend(self.FindAngle45(x, y,  8, False))

        return foundTiles
    def Algo_Knight(self, x, y):
        foundTiles = []

        self.FindL(foundTiles, [x+1, y+2])
        self.FindL(foundTiles, [x-1, y+2])

        self.FindL(foundTiles, [x+2, y-1])
        self.FindL(foundTiles, [x+2, y+1])

        self.FindL(foundTiles, [x-2, y+1])
        self.FindL(foundTiles, [x-2, y-1])

        self.FindL(foundTiles, [x+1, y-2])
        self.FindL(foundTiles, [x-1, y-2])

        return foundTiles
    def Algo_King(self,x,y):
        foundTiles = []

        foundTiles.extend(self.FindAngle0(x,y,1))
        foundTiles.extend(self.FindAngle45(x,y,2,False))
        foundTiles.extend(self.FindAngle90(x,y,1,False))


        return foundTiles
    def FindAngle90(self, x, y,  upto=8, isPawn=False):

        foundTiles = []
        if isPawn:
            if self.curruntSide == 0:
                for y_ in range(1, upto+1):
                    if self.getTile([x, y-y_]) == 0:
                        foundTiles.append([x, y-y_])

                    elif self.getTile([x, y-y_]).side != self.curruntSide:
                        break
            if self.curruntSide == 1:
                for y_ in range(1, upto+1):
                    if self.getTile([x, y+y_]) == 0:
                        foundTiles.append([x, y+y_])
                    elif self.getTile([x, y+y_]).side != self.curruntSide:
                        break
        else:
            for i in range(1, upto+1):
                temp_coord = [x, y+i]
                if temp_coord[1] < 8 and temp_coord[1] >= 0:
                    if self.getTile(temp_coord) == 0:
                        foundTiles.append(temp_coord)
                    elif self.getTile(temp_coord).side == self.curruntSide:
                        break
                    elif self.getTile(temp_coord).side != self.curruntSide:
                        foundTiles.append(temp_coord)
                        break
                else:
                    break
            for i in range(1, upto+1):
                temp_coord = [x, y-i]
                if temp_coord[1] >= 0 and temp_coord[1] < 8:
                    if self.getTile(temp_coord) == 0:
                        foundTiles.append(temp_coord)
                    elif self.getTile(temp_coord).side == self.curruntSide:
                        break
                    elif self.getTile(temp_coord).side != self.curruntSide:
                        foundTiles.append(temp_coord)
                        break
                else:
                    break

        return foundTiles

    def FindAngle0(self, x, y,upto=8):
        foundTiles = []
        for i in range(1, upto+1):
            temp_coord = [x+i, y]
            if temp_coord[0] < 8 and temp_coord[0] >= 0:
                if self.getTile(temp_coord) == 0:
                    foundTiles.append(temp_coord)
                elif self.getTile(temp_coord).side == self.curruntSide:
                    break
                elif self.getTile(temp_coord).side != self.curruntSide:
                    foundTiles.append(temp_coord)
                    break
            else:
                break
        for i in range(1, upto+1):
            temp_coord = [x-i, y]
            if temp_coord[0] >= 0 and temp_coord[0] < 8:
                if self.getTile(temp_coord) == 0:
                    foundTiles.append(temp_coord)
                elif self.getTile(temp_coord).side == self.curruntSide:
                    break
                elif self.getTile(temp_coord).side != self.curruntSide:
                    foundTiles.append(temp_coord)
                    break
            else:
                break

        return foundTiles

    def FindAngle45(self, x, y, upto=8, isPawn=False):
        foundTiles = []
        if isPawn:
            
            if self.curruntSide == 1:
                temp_coord = [x+1, y+1]
                isInLimit = self.checkInLimit(temp_coord)
                if isInLimit and self.getTile(temp_coord) != 0:

                    if self.getTile(temp_coord).side != self.curruntSide:
                        foundTiles.append(temp_coord)
                temp_coord = [x-1, y+1]
                isInLimit = self.checkInLimit(temp_coord)
                if isInLimit and self.getTile(temp_coord) != 0:
                    if self.getTile(temp_coord).side != self.curruntSide:
                        foundTiles.append(temp_coord)

            elif self.curruntSide == 0:
                temp_coord = [x-1, y-1]
                isInLimit = self.checkInLimit(temp_coord)
                if isInLimit and self.getTile(temp_coord) != 0:
                    if self.getTile(temp_coord).side != self.curruntSide:
                        foundTiles.append(temp_coord)
                temp_coord = [x+1, y-1]
                isInLimit = self.checkInLimit(temp_coord)
                if isInLimit and self.getTile(temp_coord) != 0 :
                    if self.getTile(temp_coord).side != self.curruntSide:
                        foundTiles.append(temp_coord)
        elif not isPawn:
            for i in range(1, upto):
                temp_coord = [x+i, y+i]
                isInLimit = self.checkInLimit(temp_coord)
                if isInLimit:
                    if self.getTile(temp_coord) == 0:
                        foundTiles.append(temp_coord)
                    elif self.getTile(temp_coord).side == self.curruntSide:
                        break
                    elif self.getTile(temp_coord).side != self.curruntSide:
                        foundTiles.append(temp_coord)
                        break

                else:
                    break
            for i in range(1, upto):
                temp_coord = [x+i, y-i]
                isInLimit = self.checkInLimit(temp_coord)
                if isInLimit:
                    if self.getTile(temp_coord) == 0:
                        foundTiles.append(temp_coord)
                    elif self.getTile(temp_coord).side == self.curruntSide:
                        break
                    elif self.getTile(temp_coord).side != self.curruntSide:
                        foundTiles.append(temp_coord)
                        break
                    else:
                        break
            for i in range(1, upto):
                temp_coord = [x-i, y-i]
                isInLimit = self.checkInLimit(temp_coord)
                if isInLimit:

                    if self.getTile(temp_coord) == 0:
                        foundTiles.append(temp_coord)
                    elif self.getTile(temp_coord).side == self.curruntSide:
                        break
                    elif self.getTile(temp_coord).side != self.curruntSide:
                        foundTiles.append(temp_coord)
                        break
                    else:
                        break
            for i in range(1, upto):
                temp_coord = [x-i, y+i]
                isInLimit = self.checkInLimit(temp_coord)
                if isInLimit:

                    if self.getTile(temp_coord) == 0:
                        foundTiles.append(temp_coord)
                    elif self.getTile(temp_coord).side == self.curruntSide:
                        break
                    elif self.getTile(temp_coord).side != self.curruntSide:
                        foundTiles.append(temp_coord)
                        break
                    else:
                        break

        return foundTiles
    
    def FindL(self, foundTiles, temp_coord):

        if self.checkInLimit(temp_coord):
            if self.getTile(temp_coord) == 0:
                foundTiles.append(temp_coord)
            elif self.getTile(temp_coord).side != self.curruntSide:
                foundTiles.append(temp_coord)

    # Utiliteis

    def getTile(self, coordinates):
        return self.Pieces[coordinates[0]][coordinates[1]]

    def checkInLimit(self, coordinates):
        if coordinates[0] >= 0 and coordinates[0] < 8 and coordinates[1] >= 0 and coordinates[1] < 8:
            return True
        else:
            return False

    def changeSide(self):
        if self.curruntSide == 1:
            self.curruntSide = 0
        else:
            self.curruntSide = 1
