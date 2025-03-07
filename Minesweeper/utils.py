from cell import Cell
import settings

# Calculate the height
def height_percentage(percentage):
    return (settings.HEIGHT / 100) * percentage

# Calculate the width
def width_percentage(percentage):
    return (settings.WIDTH / 100) * percentage