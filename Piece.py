import pygame,numpy
import CONSTANTS
class Piece(pygame.sprite.Sprite):
    pid = 0
    side = 0
    sprite = None
    hasMoved = False

    # 0 = white , 1 = Black
    def __init__(self,Piece_id,side) -> None:
        super().__init__()

        self.pid = Piece_id
        self.side = side

        self.loadToSprite(Piece_id*CONSTANTS.BOX_SIZE,self.side*CONSTANTS.BOX_SIZE)

        self.rect = self.image.get_rect()
        self.image = pygame.transform.scale(self.image,(CONSTANTS.TILESIZE,CONSTANTS.TILESIZE))

    def loadToSprite(self,localX,localY):
        self.image = CONSTANTS.SpriteSheet.subsurface(pygame.Rect(localX,localY,CONSTANTS.BOX_SIZE,CONSTANTS.BOX_SIZE))


def DOit():
    tempPis = numpy.zeros((8, 8)).tolist()

        # Loading Kings
    tempPis[4][7] = Piece(CONSTANTS.PIECE_IDS["King"], 0)
    tempPis[4][0] = Piece(CONSTANTS.PIECE_IDS["King"], 1)

    # Loading Queens
    tempPis[3][7] = Piece(CONSTANTS.PIECE_IDS["Queen"], 0)
    tempPis[3][0] = Piece(CONSTANTS.PIECE_IDS["Queen"], 1)

    # Loading Bishop
    tempPis[2][7] = Piece(CONSTANTS.PIECE_IDS["Bishop"], 0)
    tempPis[2][0] = Piece(CONSTANTS.PIECE_IDS["Bishop"], 1)

    tempPis[5][7] = Piece(CONSTANTS.PIECE_IDS["Bishop"], 0)
    tempPis[5][0] = Piece(CONSTANTS.PIECE_IDS["Bishop"], 1)

    # Loading Knight
    tempPis[1][7] = Piece(CONSTANTS.PIECE_IDS["Knight"], 0)
    tempPis[1][0] = Piece(CONSTANTS.PIECE_IDS["Knight"], 1)

    tempPis[6][7] = Piece(CONSTANTS.PIECE_IDS["Knight"], 0)
    tempPis[6][0] = Piece(CONSTANTS.PIECE_IDS["Knight"], 1)

    # Loading Rook
    tempPis[0][7] = Piece(CONSTANTS.PIECE_IDS["Rook"], 0)
    tempPis[0][0] = Piece(CONSTANTS.PIECE_IDS["Rook"], 1)

    tempPis[7][7] = Piece(CONSTANTS.PIECE_IDS["Rook"], 0)
    tempPis[7][0] = Piece(CONSTANTS.PIECE_IDS["Rook"], 1)
    # Loading Pawns

    for pos in range(0, 8):
        tempPis[pos][1] = Piece(CONSTANTS.PIECE_IDS["Pawn"], 1)

    for pos in range(0, 8):
        tempPis[pos][6] = Piece(CONSTANTS.PIECE_IDS["Pawn"], 0)

