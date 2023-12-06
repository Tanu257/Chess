from Piece import Piece
import CONSTANTS
class Algorithms:

    def __init__(self,piece,whiteStates,blackStates):
        self.Pieces = piece
        self.whiteStates = whiteStates
        self.blackStates = blackStates
    def getMovables(self,toMovePiece,curruntSide):
        self.toMovePiece = toMovePiece
        self.curruntSide = curruntSide
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


    def TransformPawn(self,x2,y2,side):
        if side == 0:
            self.Pieces[x2][y2] = Piece(self.whiteStates["pretransformation"],side)
        elif side == 1:
            self.Pieces[x2][y2] = Piece(self.blackStates["pretransformation"],side)
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
    
    def getTile(self, coordinates):

        return self.Pieces[coordinates[0]][coordinates[1]]

    def checkInLimit(self, coordinates):
        if coordinates[0] >= 0 and coordinates[0] < 8 and coordinates[1] >= 0 and coordinates[1] < 8:
            return True
        else:
            return False
