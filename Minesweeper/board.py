from cell import Cell
import tkinter
import random
import settings

class Board:
    def __init__(self, root, rows, cols, mines):
        self.root = root
        self.rows = rows
        self.cols = cols
        self.mines = mines
        self.grid = [[None for _ in range(cols)] for _ in range(rows)]
        self.mines_position = set()
        self.directions = [(-1, -1), (-1, 0), (-1, 1),  # Top left,Top,Top right
                            (0, -1), (0, 1),  # left , right
                            (1, -1), (1, 0), (1, 1)
                        ]

    # Function to create the grid of cells
    def create_grid(self):
        for r in range(self.rows):
            for c in range(self.cols):
                cell = Cell(self.root)
                cell.create_button_object(r, c)
                cell.cell_btn_object.config(command=lambda r=r, c=c: self.reveal_cell(r, c))
                self.grid[r][c] = cell
        
        self.place_mines()
        self.calculate_number() 

    # Function to randomly generate mines position
    def place_mines(self):
        # self.grid[1][1].cell_btn_object.config(text="2")
        while len(self.mines_position) < self.mines:
            r = random.randint(0, self.rows - 1)
            c = random.randint(0, self.cols - 1)
            if(r, c) not in self.mines_position:
                self.mines_position.add((r, c))
                self.grid[r][c].is_mine = True
                self.grid[r][c].value = '*'

    # Funtion to indexing number on per cell
    def calculate_number(self):
        for row in range(self.rows):
            for col in range(self.cols):
                # Bỏ qua nếu ô đó là bom
                if self.grid[row][col].is_mine:
                    continue
                mine_count = 0
                #Duyệt qua từng hướng trong danh sách Directions
                for dr,dc in self.directions:
                    #nr= hàng của ô lân cận, nc = cột của ô lân cận
                    nr,nc = row+dr,col+dc
                    # Kiểm tra xem tọa độ (nr,nc) có nằm trong các ô lân cận không
                    if 0<=nr<self.rows and 0<=nc<self.cols:
                        if self.grid[nr][nc].is_mine:
                            mine_count+=1
                #Đánh dấu số
                self.grid[row][col].value = str(mine_count)

    # Reveal cell when clicked
    def reveal_cell(self, row, col):
        curr_cell = self.grid[row][col]
        # TO-DO: Hanlde reveal cell

    # Reveal adjecent cells
    def reveal_neighbor(self, row, col):
        # TO-DO: Handle reveal adjacent cells
        pass

    # Print the grid
    def print_grid(self):
        for row in self.grid:
            for col in row:
                print(col, end="  ")
            print()