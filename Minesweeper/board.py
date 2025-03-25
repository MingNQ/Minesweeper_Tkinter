from cell import Cell
import random

class Board:
    def __init__(self, root, rows, cols, mines):
        self.root = root
        self.rows = rows
        self.cols = cols
        self.mines = mines
        self.grid = [[None for _ in range(cols)] for _ in range(rows)]

    # TO-DO: Complete function
    # Function to create the grid of cells
    def create_grid(self):
        # TO-DO: create the grid of cells
        
        self.place_mines()
        self.calculate_number() 

    # TO-DO: Complete function
    # Function to randomly generate mines position
    def place_mines(self):
        pass

    # TO-DO: Complete function
    # Funtion to indexing number on per cell
    def calculate_number(self):
        pass

    # Print the grid
    def print_grid(self):
        for row in self.grid:
            for col in row:
                print(col, end="  ")
            print()