import os
import sys

# Calculate the height
def center_height(window_height, height):
    return (window_height - height) // 2

# Calculate the width
def center_width(window_width, width):
    return (window_width - width) // 2

def resoure_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)