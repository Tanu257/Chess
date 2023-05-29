import pygame,CONSTANTS,Board
from Piece import Piece

# Initalizing
pygame.init()
screen = pygame.display.set_mode((CONSTANTS.SCREENWIDTH, CONSTANTS.SCREENHIEGHT))

# Loading Board

board = Board.Board(screen)
board.startOver()
# Update the display
pygame.display.update()

running = True

while running:
    board.drawGame()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if not board.isGameOver:
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                board.SetMouseClickedTile(pos)
        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    board.startOver()
    pygame.display.flip()

    
# Quit Pygame
pygame.quit()