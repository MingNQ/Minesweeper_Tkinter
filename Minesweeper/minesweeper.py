from tkinter import *
from cell import Cell
from board import Board
import settings
import utils

class Minesweeper: 
    def __init__(self, root, difficulty="medium"):
        self.root = root
        self.board = Board(None, 16, 30, 99) # FOR TESTING
        self.time_elapsed = 0
        self.create_window()
        self.difficulty = difficulty

    def reload_winfo(self):
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()

        self.root.configure(bg = settings.BLACK) # Change background color
        self.root.title('Minesweeper Game') # Set title for the window
        self.root.resizable(False, False) # Unresizable the window 
        self.root.overrideredirect(True) # Remove title bar
        self.root.update_idletasks() # Update the window to get the correct size

        x = utils.center_width(self.screen_width, self.root.winfo_width())
        y = utils.center_height(self.screen_height, self.root.winfo_height())
        self.root.geometry(f'{self.root.winfo_width()}x{self.root.winfo_height()}+{x}+{y}')

    # Create the window with all components
    def create_window(self):
        self.create_top_bar() # Top bar

        # Divide part
        line = Frame(
            self.root, 
            bg = settings.LIGHT_BLACK,
            height=1)
        line.pack(fill=X) 

        self.create_main_frame() # Main frame
        self.reload_winfo() # Reload window info

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
            borderwidth=1,
            command=self.setting_onclick
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
        )
        center_frame.pack(fill=BOTH, expand=True)
        self.board.root = center_frame
        self.board.create_grid()

    # Setting Command
    def setting_onclick(self):
        x = utils.center_width(self.screen_width, settings.SETTING_DIALOG_WIDTH)
        y = utils.center_height(self.screen_height, settings.SETTING_DIALOG_HEIGHT)

        setting_dialog = Toplevel()
        setting_dialog.overrideredirect(True)
        setting_dialog.geometry(f'{settings.SETTING_DIALOG_WIDTH}x{settings.SETTING_DIALOG_HEIGHT}+{x}+{y}')
        setting_dialog.configure(bg=settings.GRAY)
        setting_dialog.grab_set()

         # Title
        label_title = Label(
            setting_dialog, 
            text=settings.ST0, 
            font=("Arial", 14, "bold"), 
            fg=settings.LIGHT_BLACK, 
            anchor='center', 
            bg=settings.GRAY)
        label_title.pack(fill=X, padx=20, pady=(8, 8))

        # Button MODE play
        button_mode = Button(
            setting_dialog, 
            text=settings.ST1, 
            font=("Arial", 14, "bold"), 
            width=15, 
            fg=settings.QUITE_WHITE, 
            bg=settings.QUITE_GRAY, 
        )
        button_mode.pack(pady=20)

        # Button Continue play
        button_continue = Button(
            setting_dialog, 
            text=settings.ST2, 
            font=("Arial", 14, "bold"), 
            width=15, 
            fg=settings.QUITE_WHITE, 
            bg=settings.QUITE_GRAY
        )
        button_continue.pack(pady=20)

        # Button Exit to Home
        button_exit = Button(
            setting_dialog, 
            text=settings.ST3, 
            font=("Arial", 14, "bold"), 
            width=15, 
            fg=settings.QUITE_WHITE, 
            bg=settings.QUITE_GRAY
        )
        button_exit.pack(pady=20)

        def on_continue():
            setting_dialog.destroy()
        
        def on_exit():
            setting_dialog.destroy()
            self.root.destroy()

        button_continue.config(command=on_continue)
        button_exit.config(command=on_exit)