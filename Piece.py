import pygame
import CONSTANTS
class Piece(pygame.sprite.Sprite):
    pid = 0
    side = 0
    sprite = None
    hasMoved = False
    def __init__(self,Piece_id,side) -> None:
        super().__init__()

        self.pid = Piece_id
        self.side = side

        self.loadToSprite(Piece_id*CONSTANTS.BOX_SIZE,self.side*CONSTANTS.BOX_SIZE)

        self.rect = self.image.get_rect()
        self.image = pygame.transform.scale(self.image,(CONSTANTS.TILESIZE,CONSTANTS.TILESIZE))

    def loadToSprite(self,localX,localY):
        self.image = CONSTANTS.SpriteSheet.subsurface(pygame.Rect(localX,localY,CONSTANTS.BOX_SIZE,CONSTANTS.BOX_SIZE))

