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
        # self.print_grid()

    # TO-DO: Complete function
    # Function to randomly generate mines position
    def place_mines(self):
        # self.grid[1][1].cell_btn_object.config(text="2")
        pass

    # TO-DO: Complete function
    # Funtion to indexing number on per cell
    def calculate_number(self):
        directions = [(-1, -1), (-1, 0), (-1, 1),  # Top left,Top,Top right
                      (0, -1), (0, 1),  # left , right
                      (1, -1), (1, 0), (1, 1)
                      ]
        for row in range(self.rows):
            for col in range(self.cols):
                # Bỏ qua nếu ô đó là bom
                if self.grid[row][col] == '*':
                    continue
                mine_count = 0
                #Duyệt qua từng hướng trong danh sách Directions
                for dr,dc in directions:
                    #nr= hàng của ô lân cận, nc = cột của ô lân cận
                    nr,nc = row+dr,col+dc
                    # Kiểm tra xem tọa độ (nr,nc) có nằm trong các ô lân cận không
                    if 0<=nr<self.rows and 0<=nc<self.cols:
                        if self.grid[nr][nc]=='*':
                            mine_count+=1
                #Đánh dấu số
                self.grid[row][col] = str(mine_count)
        pass

    # Print the grid
    def print_grid(self):
        for row in self.grid:
            for col in row:
                print(col, end="  ")
            print()