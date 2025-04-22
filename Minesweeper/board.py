from cell import Cell
import random
import settings

class Board:
    def __init__(self, root, rows, cols, mines, on_game_over = None, on_update_flag = None):
        self.root = root
        self.rows = rows
        self.cols = cols
        self.mines = mines
        self.flags = mines
        self.grid = [[None for _ in range(cols)] for _ in range(rows)]
        self.mines_position = set()
        self.directions = [(-1, -1), (-1, 0), (-1, 1),  # Top left,Top,Top right
                           (0, -1), (0, 1),  # left , right
                           (1, -1), (1, 0), (1, 1)
                        ]
        self.on_game_over = on_game_over
        self.on_update_flag = on_update_flag
        self.revealed_cells = 0

    # Function to create the grid of cells
    def create_grid(self):
        for r in range(self.rows):
            for c in range(self.cols):
                cell = Cell(self.root)
                cell.create_button_object(r, c)
                cell.cell_btn_object.config(command=lambda r=r, c=c: self.reveal_cell(r, c))
                cell.cell_btn_object.bind('<Button-3>', self.place_flag)  # Right click to place flag
                self.grid[r][c] = cell

        self.place_mines()
        self.calculate_number()

    # Function to randomly generate mines position
    def place_mines(self):
        while len(self.mines_position) < self.mines:
            r = random.randint(0, self.rows - 1)
            c = random.randint(0, self.cols - 1)
            if (r, c) not in self.mines_position:
                self.mines_position.add((r, c))
                self.grid[r][c].is_mine = True

    # Funtion to indexing number on per cell
    def calculate_number(self):
        for row in range(self.rows):
            for col in range(self.cols):
                cell = self.grid[row][col]
                # Bỏ qua nếu ô đó là bom
                if cell.is_mine:
                    continue
                mine_count = 0
                # Duyệt qua từng hướng trong danh sách Directions
                for dr, dc in self.directions:
                    # nr= hàng của ô lân cận, nc = cột của ô lân cận
                    nr, nc = row + dr, col + dc
                    # Kiểm tra xem tọa độ (nr,nc) có nằm trong các ô lân cận không
                    if 0 <= nr < self.rows and 0 <= nc < self.cols:
                        if self.grid[nr][nc].is_mine:
                            mine_count += 1
                # Đánh dấu số
                cell.value = mine_count

    # Reveal cell when clicked
    def reveal_cell(self, row, col):
        curr_cell = self.grid[row][col]
        colors = {
            '1': 'blue',
            '2': 'green',
            '3': 'orange',
            '4': 'red',
            '5': 'purple',
            '6': 'yellow',
            '7': 'turquoise',
            '8': 'darkblue'
        }

        if curr_cell.is_mine:
            self.reveal_all_bomb()

            if self.on_game_over:
                self.on_game_over(game_over=True)

            return
        elif curr_cell.value > 0:
            color = colors.get(str(curr_cell.value),'black')
            curr_cell.cell_btn_object.config(text=str(curr_cell.value), state="disabled", disabledforeground=color, bg=settings.LIGHT_GRAY, fg=color)
        else:
            curr_cell.cell_btn_object.config(text="", state="disabled", bg=settings.LIGHT_GRAY)
            self.reveal_neighbor(row, col)
        self.revealed_cells += 1

        if self.flags == 0 and self.revealed_cells == (self.rows * self.cols - self.mines):
            if self.on_game_over:
                self.on_game_over()

    # Reveal adjecent cells
    def reveal_neighbor(self, row, col):
        for dr, dc in self.directions:
            nr,nc = row + dr, col + dc
            if 0 <= nr < self.rows and 0 <= nc < self.cols:
                neighbor = self.grid[nr][nc]
                if neighbor.cell_btn_object['state'] == 'normal' and not neighbor.is_mine:
                    self.reveal_cell(nr, nc)

    # Reveal all bombs 
    def reveal_all_bomb(self):
        for row,col in self.mines_position:
            cell = self.grid[row][col]
            cell.cell_btn_object.config(text = '*', bg = settings.RED , state="disabled", disabledforeground='black')
        for row in self.grid:
            for cell in row:
                cell.cell_btn_object.config(state = "disabled")

    # Place flag on right click
    def place_flag(self, event):
        cell = event.widget
        if cell['text'] == '':
            cell.config(text='🚩', bg = settings.LIGHT_BLUE, state="disabled")
            self.flags -= 1
        elif cell['text'] == '🚩':
            cell.config(text='', bg = settings.QUITE_GRAY, state="normal")
            self.flags += 1
        
        if self.on_update_flag:
            self.on_update_flag()