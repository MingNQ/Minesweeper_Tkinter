from tkinter import *
from cell import Cell
from board import Board
import settings
import utils

# Create a new window
root = Tk()
root.configure(bg="black") # Change background color
root.geometry(f'{settings.WIDTH}x{settings.HEIGHT}') # Size of the window
root.title('Minesweeper Game') # Set title for the window
root.resizable(False, False) # Unresizable the window 

# Top frame
top_frame = Frame(
    root,
    bg="black",
    width=settings.WIDTH,
    height=utils.height_percentage(25) 
)
top_frame.place(x=0, y=0)

# Lef frame
left_frame = Frame(
    root, 
    bg='black',
    width=utils.width_percentage(25),
    height=utils.width_percentage(75)
)
left_frame.place(x=0, y=utils.height_percentage(25))

# Center frame
center_frame = Frame(
    root, 
    bg='black',
    width=utils.width_percentage(75),
    height=utils.width_percentage(75)
)
center_frame.place(
    x=utils.width_percentage(25), 
    y=utils.height_percentage(25)
)

# TO-DO: Create grid with x rows and y columns
Board.create_grid(rows = 0, columns = 0, mines = 0)

# Run the window
root.mainloop()