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
        self.revealed = [[False for _ in range(cols)] for _ in range(rows)]
        self.game_over = False
        self.display = [['' for _ in range(self.cols)] for _ in range(self.rows)]
        self.create_grid()
        self.place_mines()
        self.calculate_number()


    # Function to create the grid of cells
    def create_grid(self):
        for r in range(self.rows):
            for c in range(self.cols):
                cell = Cell(self.root)
                cell.create_button_object(r, c)
                cell.cell_btn_object.config(command=lambda r=r, c=c: self.reveal_cell(r, c))
                self.grid[r][c] = cell
        
        self.place_mines()
        # self.calculate_number() 

    # TO-DO: Complete function
    # Function to randomly generate mines position
    def place_mines(self):
        # self.grid[1][1].cell_btn_object.config(text="2")
        while len(self.mines_position) < self.mines:
            r = random.randint(0, self.rows - 1)
            c = random.randint(0, self.cols - 1)
            if(r, c) not in self.mines_position:
                self.mines_position.add((r, c))
                self.grid[r][c] = '*'
        pass

    # Funtion to indexing number on per cell
    def calculate_number(self):
        for row in range(self.rows):
            for col in range(self.cols):
                # Bỏ qua nếu ô đó là bom
                if self.grid[row][col] == '*':
                    continue
                mine_count = 0
                #Duyệt qua từng hướng trong danh sách Directions
                for dr,dc in self.directions:
                    #nr= hàng của ô lân cận, nc = cột của ô lân cận
                    nr,nc = row+dr,col+dc
                    # Kiểm tra xem tọa độ (nr,nc) có nằm trong các ô lân cận không
                    if 0<=nr<self.rows and 0<=nc<self.cols:
                        if self.grid[nr][nc]=='*':
                            mine_count+=1
                #Đánh dấu số
                self.grid[row][col] = str(mine_count)

    # Reveal cell when clicked
    def reveal_cell(self, row, col):
        if self.game_over:
            print("Game Over")
            return
        # Kiểm tra giới hạn
        if row < 0 or row >= self.rows or col < 0 or col >= self.cols:
            return
        if self.revealed[row][col]:
            print("You've already clicked on this cell.")
            return

        curr_cell = self.grid[row][col]
        # Nếu ô đó là bom, Game Over
        if curr_cell == '*':
            print("Game Over")
            self.game_over = True
            self.reveal_all_mines()
            return

        # Mở ô
        self.revealed[row][col] = True
        self.display[row][col] = curr_cell

        # Nếu ô đó không phải bom,hiển thị số bom xung quanh
        if curr_cell != '0':
            print(f"Revealed cell ({row}, {col}) with {curr_cell} surrounding mines.")
            self.display[row][col] = curr_cell
            return
        if curr_cell == '0':
            self.display[row][col] = '0'
            self.reveal_neighbor(row, col)
            return
        for dr, dc in self.directions:
            nr, nc = row + dr, col + dc
            self.reveal_cell(nr, nc)


    # TO-DO: Hanlde reveal cell

    # Reveal adjecent cells
    def reveal_neighbor(self, row, col):
        # TO-DO: Handle reveal adjacent cells
        for dr,dc in self.directions:
            nr,nc = row+dr,col+dc
            if 0 <= nr < self.rows and 0 <= nc < self.cols and not self.revealed[nr][nc]:
                curr_cell = self.grid[nr][nc]
                if curr_cell != '*':
                    self.display[nr][nc] = curr_cell
                    self.revealed[nr][nc] = True
                    if curr_cell == '0':
                        self.reveal_neighbor(nr, nc)


    #Reveal all mines when the game is over
    def reveal_all_mines(self):
        for row in range(self.rows):
            for col in range(self.cols):
                if self.grid[row][col] == '*':
                    print(f"Revealed cell ({row}, {col}) with a mine.")
                    self.revealed[row][col] = True
        self.print_grid()
        pass

    # Print the grid
    def print_grid(self):
        # for row in self.grid:
        #     for col in row:
        #         print(col, end="  ")
        #     print()
        print("Lưới hiện tại:")
        print("  " + " ".join(str(i) for i in range(self.cols)))
        for i in range(self.rows):
            row_display = []
            for j in range(self.cols):
                if self.revealed[i][j]:
                    # Nếu đã mở, hiển thị giá trị thực (số hoặc bom)
                    row_display.append(str(self.grid[i][j]))
                elif self.grid[i][j] == '*' and self.game_over:
                    # Nếu là bom và đã game over, tiết lộ bom
                    row_display.append('*')
                else:
                    # Ô chưa mở
                    row_display.append('■')
            print(f"{i}  " + " ".join(row_display))


def play():
    root = tkinter.Tk()
    root.title("Minesweeper")
    root.geometry("600x400")
    board = Board(root, 10, 10,30)
    while not board.game_over:
        board.print_grid()
        try:
            row = int(input("Nhập hàng: "))
            col = int(input("Nhập cột: "))
            board.reveal_cell(row, col)
        except ValueError:
            print("Vui lòng nhập số nguyên!")
        except KeyboardInterrupt:
            print("\n Thoát Game")
            break
    board.print_grid()
    print("Game Over")

if __name__ == '__main__':
    play()



