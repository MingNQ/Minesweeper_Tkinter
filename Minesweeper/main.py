from tkinter import *
from cell import Cell
from board import Board
import settings
import utils

class Home:
    def __init__(self, root):
        self.root = root
        self.root.title('Minesweeper Game') # Set title for the window
        self.root.geometry(f'{settings.WIDTH}x{settings.HEIGHT}') # Size of the window
        self.root.resizable(False, False) # Unresizable the window 
        
        self.create_home_ui()
    
    def create_home_ui(self):
        self.app_icon = PhotoImage(file='./assets/app_logo.png')
        self.app_icon = self.app_icon.subsample(1, 1)

        app_logo_label = Label(self.root, image=self.app_icon)
        app_logo_label.pack(pady=52)

        title_label = Label(self.root, text="MINESWEEPER", font=("Arial", 24), fg="white")
        title_label.pack(pady=5)

        play_button = Button(self.root, text="Play", font=("Arial", 14), width=15)
        play_button.pack(pady=40)

        credit_button = Button(self.root, text="Credit", font=("Arial", 14), width=15)
        credit_button.pack(pady=10)

class Minesweeper:
    def __init__(self, root):
        self.root = root
        self.root.configure(bg = "black") # Change background color
        self.root.title('Minesweeper Game') # Set title for the window
        self.root.resizable(False, False) # Unresizable the window 
        self.time_elapsed = 0
        self.board = Board(None, 16, 30, 99)
        self.create_window()

    # Create the window with all components
    def create_window(self):
        self.create_top_bar() # Top bar
        line = Frame(
            self.root, 
            bg = settings.LIGHT_BLACK,
            height=1)
        line.pack(fill=X) # Divide part
        self.create_main_frame() # Main frame

    # Top frame
    def create_top_bar(self):
        top_frame = Frame(
            self.root,
            bg = settings.LIGHT_GRAY,
            height = 64
        )
        top_frame.pack(fill=X)

        # Time Counter Label
        self.time_label = Label(
            top_frame, 
            text = '000',
            font = ('Arial', 14),
            fg = settings.QUITE_WHITE,
            bg = settings.QUITE_GRAY)
        self.time_label.pack(side=LEFT, padx=10, pady=(8, 8))
        self.update_timer()

        # Setting Button
        self.setting_icon = PhotoImage(file='./assets/setting_icon.png')
        self.setting_icon = self.setting_icon.subsample(3, 3)
        self.setting_button = Button(
            top_frame,
            image = self.setting_icon,
            bg = settings.LIGHT_GRAY,
            borderwidth=1
        )
        self.setting_button.pack(side=RIGHT, padx=10, pady=(8, 8))

        # Flag Counter Label
        self.flag_label = Label(
            top_frame, 
            text = f'{self.board.mines:03d}',
            font = ('Arial', 14),
            fg = settings.QUITE_WHITE,
            bg = settings.QUITE_GRAY)
        self.flag_label.pack(side=RIGHT, padx=10, pady=(8, 8))
        self.update_flags()

    # Time Counter
    def update_timer(self):
        minutes = self.time_elapsed // 60
        seconds = self.time_elapsed % 60
        self.time_label.config(
            text = f'{minutes}:{seconds:02d}'
        )
        self.time_elapsed += 1
        self.root.after(1000, self.update_timer)

    # Flags Counter
    def update_flags(self):
        self.flag_label.config(
            text = f'{self.board.mines:03d}'
        )

    # Main frame
    def create_main_frame(self):
        center_frame = Frame(
            self.root, 
            bg = settings.GRAY,
            height = utils.width_percentage(75)
        )
        center_frame.pack(fill=BOTH, expand=True)
        self.board.root = center_frame
        self.board.create_grid()

# Main
if __name__ == '__main__':
    root = Tk()
    home = Home(root)
    # app = Minesweeper(root)
    root.mainloop()