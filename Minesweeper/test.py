import tkinter as tk
import random
import time

class Minesweeper:
    def __init__(self, root, rows=10, cols=10, mines=10):
        self.root = root
        self.rows = rows
        self.cols = cols
        self.mines = mines
        self.board = [[0 for _ in range(cols)] for _ in range(rows)]
        self.buttons = [[None for _ in range(cols)] for _ in range(rows)]
        self.mine_positions = set()
        self.create_widgets()
        self.place_mines()
        self.calculate_numbers()
        self.ai_play()

    def create_widgets(self):
        for r in range(self.rows):
            for c in range(self.cols):
                btn = tk.Button(self.root, width=2, height=1, command=lambda r=r, c=c: self.reveal_cell(r, c))
                btn.grid(row=r, column=c)
                self.buttons[r][c] = btn

    def place_mines(self):
        while len(self.mine_positions) < self.mines:
            r, c = random.randint(0, self.rows - 1), random.randint(0, self.cols - 1)
            if (r, c) not in self.mine_positions:
                self.mine_positions.add((r, c))
                self.board[r][c] = -1

    def calculate_numbers(self):
        for r in range(self.rows):
            for c in range(self.cols):
                if self.board[r][c] == -1:
                    continue
                count = sum((nr, nc) in self.mine_positions for nr in range(r-1, r+2) for nc in range(c-1, c+2) if 0 <= nr < self.rows and 0 <= nc < self.cols)
                self.board[r][c] = count

    def reveal_cell(self, r, c):
        if (r, c) in self.mine_positions:
            self.buttons[r][c].config(text='*', bg='red')
            self.game_over()
        else:
            self.buttons[r][c].config(text=str(self.board[r][c]), state=tk.DISABLED)
            if self.board[r][c] == 0:
                self.reveal_neighbors(r, c)

    def reveal_neighbors(self, r, c):
        for nr in range(r-1, r+2):
            for nc in range(c-1, c+2):
                if 0 <= nr < self.rows and 0 <= nc < self.cols and self.buttons[nr][nc]['state'] != tk.DISABLED:
                    self.reveal_cell(nr, nc)

    def game_over(self):
        for r, c in self.mine_positions:
            self.buttons[r][c].config(text='*', bg='red')
        print("Game Over")

    def ai_play(self):
        opened = set()
        while len(opened) < (self.rows * self.cols - self.mines):
            time.sleep(0.5)
            self.root.update()
            move = self.find_best_move(opened)
            if move:
                self.reveal_cell(*move)
                opened.add(move)
            else:
                break

    def find_best_move(self, opened):
        for r in range(self.rows):
            for c in range(self.cols):
                if (r, c) not in opened and (r, c) not in self.mine_positions:
                    return (r, c)
        return None

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Minesweeper")
    game = Minesweeper(root)
    root.mainloop()
