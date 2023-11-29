import pygame,CONSTANTS,Board
from Piece import Piece
import pgu.gui as gui
# Initalizing
pygame.init()
screen = pygame.display.set_mode((CONSTANTS.SCREENWIDTH, CONSTANTS.SCREENHIEGHT))

options = ["Option 1", "Option 2", "Option 3", "Option 4"]

        # Define a callback function for each option
def option1():
    print("You chose option 1")

def option2():
    print("You chose option 2")

def option3():
    print("You chose option 3")

def option4():
    print("You chose option 4")

# Create a gui app and a dialog box
app = gui.App()
dialog = gui.Dialog("Choose an option", gui.Table())

# Add a table to the dialog box with the options as buttons
table = dialog.widget
table.tr()
for option in options:
    # Create a button with the option text
    button = gui.Button(option)
    # Connect the button to the corresponding callback function
    button.connect(gui.CLICK, globals()[option.lower()])
    # Add the button to the table
    table.td(button)

# Show the dialog box on the screen
dialog.open()
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