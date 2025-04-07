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
        app_logo_label.pack(pady=50)
        
        # Title
        title_label = Label(
            self.root, 
            text=settings.APP_NAME, 
            font=("Arial", 24, "bold"), 
            fg=settings.QUITE_GRAY
        )
        title_label.pack(pady=5)

        # Button Player play
        button_play = Button(
            self.root, 
            text=settings.H1, 
            font=("Arial", 14, "bold"), 
            width=15, 
            fg=settings.QUITE_WHITE, 
            bg=settings.QUITE_GRAY, 
            command=self.player_play
        )
        button_play.pack(pady=20)

        # Button Bot play
        button_bot_play = Button(
            self.root, 
            text=settings.H2, 
            font=("Arial", 14, "bold"), 
            width=15, 
            fg=settings.QUITE_WHITE, 
            bg=settings.QUITE_GRAY
        )
        button_bot_play.pack(pady=20)

        # Button How to play
        button_guide = Button(
            self.root, 
            text=settings.H3, 
            font=("Arial", 14, "bold"), 
            width=15, 
            fg=settings.QUITE_WHITE, 
            bg=settings.QUITE_GRAY, 
            command=self.show_how_to_dialog
        )
        button_guide.pack(pady=20)

    def player_play(self):
        # self.root.withdraw() # Hide home screen
        game_screen = Toplevel()
        app = Minesweeper(game_screen)

    def show_how_to_dialog(self):
        dialog = Toplevel()
        dialog.geometry(f'{settings.DIALOG_WIDTH}x{settings.DIALOG_HEIGHT}')
        dialog.configure(bg=settings.GRAY)
        dialog.grab_set() # Focus on dialog

        # Title
        label_title = Label(dialog, text=settings.H3, font=("Arial", 14, "bold"), fg=settings.LIGHT_BLACK, anchor='w', bg=settings.GRAY)
        label_title.pack(fill=X, padx=20, pady=(8, 8))

        mp = {1 : settings.HT1, 2 : settings.HT2, 3 : settings.HT3, 4 : settings.HT4, 5: settings.HT5 }

        # Content 
        label_content = Label(
            dialog, 
            font=("Arial", 12), 
            fg=settings.LIGHT_BLACK, 
            bg=settings.GRAY, 
            anchor='w', 
            wraplength=580, 
            justify=LEFT
        )
        label_content.pack(fill=X, padx=20)

        self.curr_content = 1

        label_content.config(text=mp[self.curr_content])

        # Button Frame
        button_frame = Frame(dialog, bg=settings.GRAY)
        button_frame.pack(side=BOTTOM, fill=X, padx=20, pady=10, anchor='e')

        def on_next():
            self.curr_content += 1
            label_content.config(text=mp[self.curr_content])

            if self.curr_content == 5:
                second_btn.config(text=settings.HT0_1, command=on_end)
                first_btn.config(text=settings.HT0_3, command=on_back)
            elif self.curr_content >= 2:
                first_btn.config(text=settings.HT0_3, command=on_back)

        def on_back():
            self.curr_content -= 1
            label_content.config(text=mp[self.curr_content])

            if self.curr_content == 1:
                first_btn.config(text=settings.HT0_1, command=on_end)
                second_btn.config(text=settings.HT0_2, command=on_next)

        def on_end():
            dialog.destroy()

        # Second Button
        second_btn = Button(button_frame, text=settings.HT0_2, width=10, font=("Arial", 10), fg = settings.QUITE_WHITE, bg = settings.QUITE_GRAY,command=on_next)
        second_btn.pack(side=RIGHT, padx=15, pady=5)

        # Second Button
        first_btn = Button(button_frame, text=settings.HT0_1, width=10, font=("Arial", 10), command=on_end)
        first_btn.pack(side=RIGHT, padx=15, pady=5)

class Minesweeper:
    def __init__(self, root):
        self.root = root
        self.root.configure(bg = settings.BLACK) # Change background color
        self.root.title('Minesweeper Game') # Set title for the window
        self.root.resizable(False, False) # Unresizable the window 
        self.time_elapsed = 0
        self.board = Board(None, 16, 30, 99) # FOR TESTING
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