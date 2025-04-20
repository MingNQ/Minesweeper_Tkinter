from tkinter import *
from cell import Cell
from board import Board
import minesweeper
import settings
import utils

class Home:
    def __init__(self, root):
        self.root = root
        self.initialize_window()
        self.create_home_ui()

    # Initialize the window
    def initialize_window(self):
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        x = utils.center_width(self.screen_width, settings.WIDTH)
        y = utils.center_height(self.screen_height, settings.HEIGHT)
        self.root.title('Minesweeper Game') # Set title for the window
        self.root.geometry(f'{settings.WIDTH}x{settings.HEIGHT}+{x}+{y}') # Size of the window
        self.root.resizable(False, False) # Unresizable the window 
    
    # Create the home screen UI
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

    # Mode Player play
    def player_play(self):
        # self.root.withdraw() # Hide home screen
        game_screen = Toplevel()
        app = minesweeper.Minesweeper(game_screen)

    # Show Guide dialog Command
    def show_how_to_dialog(self):
        dialog = Toplevel()
        x = utils.center_width(self.screen_width, settings.DIALOG_WIDTH)
        y = utils.center_height(self.screen_height, settings.DIALOG_HEIGHT)
        dialog.geometry(f'{settings.DIALOG_WIDTH}x{settings.DIALOG_HEIGHT}+{x}+{y}')
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

# Main
if __name__ == '__main__':
    root = Tk()
    home = Home(root)
    # app = Minesweeper(root)
    root.mainloop()