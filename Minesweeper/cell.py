from tkinter import Button 
import tkinter
import settings

class Cell:
    CELL_WIDTH = 2
    CELL_HEIGHT = 1

    def __init__(self, root, is_mine = False):
        self.value = 0
        self.state = tkinter.ACTIVE
        self.is_mine = is_mine
        self.root = root
        self.cell_btn_object = None
    
    # Create button
    def create_button_object(self, r, c):
        btn = Button(
            self.root,
            bg = settings.QUITE_GRAY,
            width = Cell.CELL_WIDTH,
            height = Cell.CELL_HEIGHT
        )
        btn.grid(row=r, column=c)
        btn.bind('<Button-3>', self.right_click_actions) # <Button-3> = right click
        self.cell_btn_object = btn  
    
    # Right click event
    def right_click_actions(self, event):   
        if self.cell_btn_object['text'] == '':
            self.cell_btn_object.config(text='🚩', bg = 'blue', state = tkinter.DISABLED)
        elif self.cell_btn_object['text'] == '🚩':
            self.cell_btn_object.config(text='', bg = settings.QUITE_GRAY, state = tkinter.ACTIVE)

    def __str__(self):
        return self.cell_btn_object.cget("text")