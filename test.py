import pygame
import pgu.gui as gui

# Initialize pygame and create a screen
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Pop up choice box example")

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Define some options for the dialog box
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

# Main loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        # Quit if the user closes the window
        if event.type == pygame.QUIT:
            running = False
        # Pass the event to the gui app
        app.event(event)
    # Fill the screen with white
    screen.fill(WHITE)
    # Paint the gui app on the screen
    app.paint()
    # Update the display
    pygame.display.flip()

# Quit pygame
pygame.quit()