from cell import Cell

class Board:
    def __init__(self, rows, cols, mines):
        self.rows = rows
        self.cols = cols
        self.mines = mines
        self.grid = [[0 for _ in range(cols)] for _ in range(rows)]
        self.create_grid(rows, cols, mines)

    # TO-DO: Complete function
    # Function to create the grid of cells
    def create_grid(self, rows, cols, mines):
        self.place_mines(0)
        self.calculate_number()
        self.print_grid()

    # TO-DO: Complete function
    # Function to randomly generate mines position
    '''
    Index = 9 to cell so that the mine is placed at that cell.
    '''
    def place_mines(self, mine_counts):
        pass

    # TO-DO: Complete function
    # Funtion to indexing number on per cell
    '''
    index = 0 if no mine in 8 cell nearly
    index = 1 if 1 mine in 8 cell nearly
    v..v..
    index = n if n mines in 8 cell nearly 
    '''
    def calculate_number(self):
        pass

    # Print the grid
    def print_grid(self):
        for row in self.grid:
            for col in row:
                print(col, end=" ")
            print()