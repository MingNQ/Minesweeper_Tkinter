from cell import Cell
import settings

grid = []

# Calculate the height
def height_percentage(percentage):
    return (settings.HEIGHT / 100) * percentage

# Calculate the width
def width_percentage(percentage):
    return (settings.WIDTH / 100) * percentage

# TO-DO: Complete function
# Function to create the grid of cells
def create_grid(row, column):
    for x in range(row):
        tmp_row = []
        for y in range(column):
            tmp_row.append(0)
        grid.append(tmp_row)

    place_mines(0)
    indexing_grid()
    print_grid()

# TO-DO: Complete function
# Function to randomly generate mines position
'''
Index = 9 to cell so that the mine is placed at that cell.
'''
def place_mines(mine_counts):
    pass

# TO-DO: Complete function
# Funtion to indexing number on per cell
'''
index = 0 if no mine in 8 cell nearly
index = 1 if 1 mine in 8 cell nearly
v..v..
index = n if n mines in 8 cell nearly 
'''
def indexing_grid():
    pass

# Print the grid
def print_grid():
    for row in grid:
        for col in row:
            print(col, end=" ")
        print()