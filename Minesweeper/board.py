from cell import Cell
import random
import time
import settings

class State:
    STATE = 'state'
    NORMAL = 'normal'
    DISABLED = 'disabled'
    ACTIVE = 'active'
    FLAGGED = '🚩'

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
        self.auto_playing = False

    # Start Auto Play
    def auto_play(self):
        self.auto_playing = True
        self.auto_play_step()

    # Action per step
    def auto_play_step(self):
        if not self.auto_playing:
            return

        def is_open(cell):
            return cell.cell_btn_object[State.STATE] == State.DISABLED and cell.cell_btn_object['text'] != State.FLAGGED

        def is_flagged(cell):
            return cell.cell_btn_object['text'] == State.FLAGGED

        changed = False
        actions = []

        # Handle logic for clear case
        for row in range(self.rows):
            for col in range(self.cols):
                cell = self.grid[row][col]

                if not is_open(cell) or cell.value == 0:
                    continue

                neighbors = self.get_neighbors(row, col)
                unopened = [c for c in neighbors if not is_open(c) and not is_flagged(c)]
                flagged = [c for c in neighbors if is_flagged(c)]

                if cell.value == len(unopened) + len(flagged) and unopened:
                    for c in unopened:
                        actions.append(('flag', c))
                        changed = True

                elif cell.value == len(flagged) and unopened:
                    for c in unopened:
                        curr_r = c.cell_btn_object.grid_info()['row']
                        curr_c = c.cell_btn_object.grid_info()['column']
                        actions.append(('reveal', curr_r, curr_c))
                        changed = True

        # Guess 
        if not changed:
            frontier = []
            fallback = []

            for row in range(self.rows):
                for col in range(self.cols):
                    cell = self.grid[row][col]
                    if is_open(cell) or is_flagged(cell):
                        continue
                    neighbors = self.get_neighbors(row, col)
                    if any(is_open(n) for n in neighbors):
                        frontier.append(cell)
                    else:
                        fallback.append(cell)

            candidates = frontier if frontier else fallback
            if candidates:
                guess = random.choice(candidates)
                r = guess.cell_btn_object.grid_info()['row']
                c = guess.cell_btn_object.grid_info()['column']
                actions.append(('reveal', r, c))
                changed = True

        # Do action if exist
        if actions:
            action = actions.pop(0)

            if not self.auto_playing:
                return

            if action[0] == 'flag':
                self.place_flag(action[1].cell_btn_object)
            elif action[0] == 'reveal':
                self.reveal_cell(action[1], action[2])

            self.root.after(500, self.auto_play_step)

    # Get neighbors
    def get_neighbors(self, row, col):
        neighbors = []
        for dr, dc in self.directions:
            nr, nc = row + dr, col + dc
            if 0 <= nr < self.rows and 0 <= nc < self.cols:
                neighbors.append(self.grid[nr][nc])
        return neighbors                    

    # Function to create the grid of cells
    def create_grid(self):
        for r in range(self.rows):
            for c in range(self.cols):
                cell = Cell(self.root)
                cell.create_button_object(r, c)
                cell.cell_btn_object.config(command=lambda r=r, c=c: self.reveal_cell(r, c))
                cell.cell_btn_object.bind('<Button-3>', self.place_flag_on_cell)  # Right click to place flag
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
            color = colors.get(str(curr_cell.value), settings.BLACK)
            curr_cell.cell_btn_object.config(text=str(curr_cell.value), state = State.DISABLED, disabledforeground=color, bg=settings.LIGHT_GRAY, fg=color)
        else:
            curr_cell.cell_btn_object.config(text="", state = State.DISABLED, bg=settings.LIGHT_GRAY)
            self.reveal_neighbor(row, col)
        self.revealed_cells += 1

        self.check_end_game()

    # Check end game
    def check_end_game(self):
        if self.flags == 0 and self.revealed_cells == (self.rows * self.cols - self.mines):
            if self.on_game_over:
                self.on_game_over()

    # Reveal adjecent cells
    def reveal_neighbor(self, row, col):
        for dr, dc in self.directions:
            nr,nc = row + dr, col + dc
            if 0 <= nr < self.rows and 0 <= nc < self.cols:
                neighbor = self.grid[nr][nc]
                if neighbor.cell_btn_object[State.STATE] == State.NORMAL and not neighbor.is_mine:
                    self.reveal_cell(nr, nc)

    # Reveal all bombs 
    def reveal_all_bomb(self):
        for row,col in self.mines_position:
            cell = self.grid[row][col]
            cell.cell_btn_object.config(text = '*', bg = settings.RED , state = State.DISABLED, disabledforeground = settings.BLACK)
        for row in self.grid:
            for cell in row:
                cell.cell_btn_object.config(state = State.DISABLED)

    # Place flag on right click
    def place_flag_on_cell(self, event):
        cell = event.widget
        self.place_flag(cell)
    
    # Place flag
    def place_flag(self, cell_btn_object):
        if cell_btn_object['text'] == '':
            cell_btn_object.config(text = State.FLAGGED, bg = settings.LIGHT_BLUE, state = State.DISABLED)
            self.flags -= 1
        elif cell_btn_object['text'] == State.FLAGGED:
            cell_btn_object.config(text = '', bg = settings.QUITE_GRAY, state = State.NORMAL)
            self.flags += 1
        
        if self.on_update_flag:
            self.on_update_flag()

        self.check_end_game()