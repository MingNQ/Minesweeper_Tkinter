from tkinter import Button 

class Cell:
    def __init__(self, is_mine = False):
        self.is_mine = is_mine
        self.cell_btn_object = None
    
    # Create button
    def create_button_object(self, location):
        btn = Button(
            location,
            text='Text'
        )
        btn.bind('<Button-1>', self.left_click_actions) # <Button-1> = left click
        btn.bind('<Button-3>', self.right_click_actions) # <Button-3> = right click
        self.cell_btn_object = btn  
    
    # Left click event
    def left_click_actions(self, event):
        print(event)
        print('Left click')

    # Right click event
    def right_click_actions(self, event):   
        print(event)
        print('Right click')