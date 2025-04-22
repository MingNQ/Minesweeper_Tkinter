from tkinter import *
from tkinter import messagebox
from cell import Cell
from board import Board
import settings
import utils

class Minesweeper: 
    def __init__(self, root, auto_play = False, on_close = None):
        self.root = root
        self.auto_play = auto_play
        self.on_close = on_close
        self.difficulty_var = IntVar(value = 2)
        r, c, m = self.get_mode()
        self.board = Board(None, r, c, m, on_game_over = self.end_game, on_update_flag = self.update_flags)
        self.time_elapsed = 0
        self.timer_id = None # Store the timer ID for cancellation
        self.create_window()
        self.root.protocol("WM_DELETE_WINDOW", self.exit_game) # Handle window close event

        if self.auto_play:
            self.root.after(1000, self.board.auto_play)

    def reload_winfo(self):
        # Get the screen width and height
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()

        self.root.configure(bg = settings.BLACK) # Change background color
        self.root.title('Minesweeper Game') # Set title for the window
        self.root.resizable(False, False) # Unresizable the window 
        # self.root.overrideredirect(True) # Remove title bar
        self.root.update_idletasks() # Update the window to get the correct size

        # Get the window width and height
        winfo_width = self.root.winfo_reqwidth()
        winfo_height = self.root.winfo_reqheight()

        x = utils.center_width(self.screen_width, winfo_width)
        y = utils.center_height(self.screen_height, winfo_height)
        self.root.geometry(f'{winfo_width}x{winfo_height}+{x}+{y}')

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
        self.flag_label.pack(side=RIGHT, padx=4, pady=(8, 8))
        self.update_flags()

        # Mode
        self.label_mode_icon = PhotoImage(file='./assets/emotion_icon.png')
        self.label_mode_icon = self.label_mode_icon.subsample(3, 3)
        self.label_mode = Button(
            top_frame, 
            image = self.label_mode_icon,
            bg = settings.LIGHT_GRAY,
            borderwidth=1,
            command=self.select_mode_dialog
        )
        self.label_mode.place(relx=0.5, rely=0.5, anchor=CENTER)

    # Time Counter
    def update_timer(self):
        minutes = self.time_elapsed // 60
        seconds = self.time_elapsed % 60
        self.time_label.config(
            text = f'{minutes}:{seconds:02d}'
        )
        self.time_elapsed += 1
        self.timer_id = self.root.after(1000, self.update_timer)

    # Flags Counter
    def update_flags(self):
        self.flag_label.config(
            text = f'{self.board.flags:03d}'
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
        self.pause_game()
        self.board.auto_playing = False

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
            bg=settings.QUITE_GRAY
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

        def on_select_mode():
            setting_dialog.destroy()
            self.select_mode_dialog()
            self.board.auto_play()

        def on_continue():
            setting_dialog.destroy()
            self.update_timer()
            self.board.auto_play()
            
        def on_exit():
            setting_dialog.destroy()
            self.exit_game()

        button_mode.config(command=on_select_mode)
        button_continue.config(command=on_continue)
        button_exit.config(command=on_exit)

    # Restart Game
    def restart_game(self):
        r, c, m = self.get_mode()
        self.time_elapsed = 0
        for widget in self.root.winfo_children():
            widget.destroy() 

        self.board = Board(None, r, c, m, on_game_over = self.end_game, on_update_flag = self.update_flags)
        self.create_window()
        self.root.grab_set()

        if self.auto_play:
            self.root.after(1000, self.board.auto_play)

    # Game Finish
    def end_game(self, game_over = False):
        self.pause_game()

        x = utils.center_width(self.screen_width, settings.RESULT_DIALOG_WIDTH)
        y = utils.center_height(self.screen_height, settings.RESULT_DIALOG_HEIGHT)
        
        result_dialog = Toplevel()
        result_dialog.overrideredirect(True)
        result_dialog.geometry(f'{settings.RESULT_DIALOG_WIDTH}x{settings.RESULT_DIALOG_HEIGHT}+{x}+{y}')
        result_dialog.configure(bg=settings.GRAY)
        result_dialog.resizable(False, False)
        result_dialog.grab_set()

        trophy_img = None
        congrat_content = None

        if game_over:
            trophy_img = PhotoImage(file="./assets/gameover_icon.png")
            trophy_img = trophy_img.subsample(2, 2)
            congrat_content = "BETTER LUCK NEXT"
        else:
            trophy_img = PhotoImage(file="./assets/victory_icon.png")
            congrat_content = "CONGRATULATION GREATEST PLAYER"

        trophy_label = Label(result_dialog, image=trophy_img, bg=settings.GRAY)
        trophy_label.image = trophy_img
        trophy_label.pack(pady=(30, 10))

        # Dialog Content
        congrat_label = Label(
            result_dialog, 
            text = congrat_content,
            font = ("Arial", 14, "bold"), 
            fg = settings.BLACK, 
            bg = settings.GRAY,
            wraplength = 180
        )
        congrat_label.pack(pady=(10, 10))

        # Time Result
        time_frame = Frame(result_dialog, bg = settings.QUITE_GRAY, bd=0)
        time_frame.pack(pady = 10)

        clock_icon = Label(time_frame, text="⏱", font=("Arial", 12), bg = settings.QUITE_GRAY, fg = settings.WHITE)
        clock_icon.pack(side="left", padx = 4, pady = 5)

        time_label = Label(time_frame, text=self.time_label.cget('text'), font=("Arial", 12), bg = settings.QUITE_GRAY, fg = settings.WHITE)
        time_label.pack(side="left", padx = 4, pady = 5)

        def destroy_dialog():
            result_dialog.destroy()
            self.exit_game()

        def play_again():
            result_dialog.destroy()
            self.restart_game()

        play_again_btn = Button(
            result_dialog,
            text = "Play Again",
            font = ("Arial", 12, "bold"),
            width = 10,
            fg = settings.QUITE_WHITE,
            bg = settings.QUITE_GRAY,
            command = play_again
        )
        play_again_btn.pack(pady=10)

        exit_btn = Button(
            result_dialog,
            text = "Exit",
            font = ("Arial", 12, "bold"),
            width = 10,
            fg = settings.QUITE_WHITE,
            bg = settings.QUITE_GRAY,
            command = destroy_dialog
        )
        exit_btn.pack(pady=10)

    # Pause Game
    def pause_game(self):
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None

    # New Game   
    def new_game(self):
        r, c, m = self.get_mode()
        self.time_elapsed = 0
        for widget in self.root.winfo_children():
            widget.destroy() 

        self.board = Board(None, r, c, m, on_game_over = self.end_game, on_update_flag = self.update_flags)
        self.create_window()

        if self.auto_play:
            self.root.after(1000, self.board.auto_play)

    # Exit Game
    def exit_game(self):
        if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
            self.root.destroy()
            if self.on_close:
                self.on_close()

    # Get Mode
    def get_mode(self):
        mode = self.difficulty_var.get()

        if mode == 0:
            r, c, m = 9, 9, 10
        elif mode == 1:
            r, c, m = 16, 16, 40
        else:
            r, c, m = 16, 30, 99

        return r, c, m

    # Select Mode Dialog
    def select_mode_dialog(self):
        self.pause_game()

        x = utils.center_width(self.screen_width, settings.MODE_DIALOG_WIDTH)
        y = utils.center_height(self.screen_height, settings.MODE_DIALOG_HEIGHT)
        
        mode_dialog = Toplevel()
        mode_dialog.overrideredirect(True)
        mode_dialog.geometry(f'{settings.MODE_DIALOG_WIDTH}x{settings.MODE_DIALOG_HEIGHT}+{x}+{y}')
        mode_dialog.configure(bg=settings.GRAY)
        mode_dialog.resizable(False, False)
        mode_dialog.grab_set()

        # Title
        mode_title = Label(
            mode_dialog, 
            text = "MODE", 
            font = ("Arial", 14, "bold"), 
            fg =settings.LIGHT_BLACK, 
            anchor = 'center', 
            bg = settings.GRAY
        )
        mode_title.pack(pady=5)

        table = Frame(mode_dialog, bg=settings.GRAY)
        table.pack()

        headers = ["", "Rows", "Columns", "Mines"]
        for i, text, in enumerate(headers):
            Label(table, text=text, font=("Arial", 10, "bold"), bg=settings.GRAY, width=10).grid(row=0, column=i)

        modes = [
            ("Beginner", 0, 9, 9, 10),
            ("Intermediate", 1, 16, 16, 40),
            ("Expert", 2, 16, 30, 99)
        ]

        for name, value, height, width, mines in modes:
            Radiobutton(table, text = name, variable = self.difficulty_var, value=value, bg=settings.GRAY).grid(row=value+1, column=0, sticky="w")
            Label(table, text=height, bg=settings.GRAY).grid(row=value+1, column=1)
            Label(table, text=width, bg=settings.GRAY).grid(row=value+1, column=2)
            Label(table, text=mines, bg=settings.GRAY).grid(row=value+1, column=3)

        def cancel_click():
            mode_dialog.destroy()
            self.root.grab_set()
            self.update_timer()

        def new_game_click():
            mode_dialog.destroy()
            self.new_game()
            
        new_game_btn = Button(
            mode_dialog,
            text = "New Game",
            font = ("Arial", 12, "bold"),
            width = 10,
            fg = settings.QUITE_WHITE,
            bg = settings.QUITE_GRAY,
            command = new_game_click
        )
        new_game_btn.pack(pady=10)

        cancel_btn = Button(
            mode_dialog,
            text = "Cancel",
            font = ("Arial", 12, "bold"),
            width = 10,
            fg = settings.QUITE_WHITE,
            bg = settings.QUITE_GRAY,
            command = cancel_click
        )
        cancel_btn.pack(pady=10)