from tkinter import Button 
import settings

class Cell:
    def __init__(self, root, is_mine = False):
        self.is_mine = is_mine
        self.root = root
        self.cell_btn_object = None
    
    # Create button
    def create_button_object(self, r, c):
        btn = Button(
            self.root,
            bg = settings.QUITE_GRAY,
            width = 2,
            height = 1
        )
        btn.grid(row=r, column=c)
        btn.bind('<Button-1>', self.left_click_actions) # <Button-1> = left click
        btn.bind('<Button-3>', self.right_click_actions) # <Button-3> = right click
        self.cell_btn_object = btn  
    
    # Left click event
    def left_click_actions(self, event):
        pass

    # Right click event
    def right_click_actions(self, event):   
        pass

    def __str__(self):
        return self.cell_btn_object.cget("text")