from cell import Cell
import random

class Board:
    def __init__(self, root, rows, cols, mines):
        self.root = root
        self.rows = rows
        self.cols = cols
        self.mines = mines
        self.grid = [[None for _ in range(cols)] for _ in range(rows)]
        self.mines_position = set()

    # TO-DO: Complete function
    # Function to create the grid of cells
    def create_grid(self):
        for r in range(self.rows):
            for c in range(self.cols):
                cell = Cell(self.root)
                cell.create_button_object(r, c)
                self.grid[r][c] = cell
        
        self.place_mines()
        self.calculate_number() 

    # TO-DO: Complete function
    # Function to randomly generate mines position
    def place_mines(self):
        # self.grid[1][1].cell_btn_object.config(text="2")
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