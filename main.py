from tkinter import *
from cellGrid import CellGrid

            


if __name__ == "__main__" :
    app = Tk()
    size_x = 40
    size_y = 20
    cell_size = 30

    grid = CellGrid(app, size_y, size_x, cell_size)
    grid.pack()

    app.mainloop()