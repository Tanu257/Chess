import pygame
BOX_SIZE = 333
TILESIZE = 80
SCREENWIDTH = TILESIZE * 8
SCREENHIEGHT= TILESIZE * 8

imagePath = "Pieces.png"
SpriteSheet = pygame.image.load(imagePath)

PIECE_IDS = {
    "King":0,
    "Queen":1,
    "Rook":4,
    "Bishop":2,
    "Knight":3,
    "Pawn":5
}
IDS_2_KEY = {
    0:"King",
    1:"Queen",
    4:"Rook",
    2:"Bishop",
    3:"Knight",
    5:"Pawn"
}
BLACK = (100,100,100)
WHITE = (255,255,255)
TEXTCOLOR = (200, 100, 80)  # White
HIGHLIGHTER = (222, 210, 80,100)
INDICATOR_CIRCLE_RADIUS = TILESIZE/2 - 20

font_size = 36

def PointToPos(x,y):
    x = x * TILESIZE
    y = y * TILESIZE

    return x,y
