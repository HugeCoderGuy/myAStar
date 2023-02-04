from tkinter import *
import numpy as np


class Cell():
    FILLED_COLOR_BG =       "grey"
    EMPTY_COLOR_BG =        "white"
    FILLED_COLOR_BORDER =   "grey"
    EMPTY_COLOR_BORDER =    "black" 
    START_COLOR_BG =        "green"
    START_COLOR_BORDER =    "green"
    END_COLOR_BG =          "red"
    END_COLOR_BORDER =      "red"
    ROUTE_COLOR_BG =        "blue"
    ROUTE_COLOR_BORDER =    "blue"

    def __init__(self, master, x, y, size):
        """ Constructor of the object called by Cell(...) """
        self.master = master
        self.abs = x
        self.ord = y
        self.size= size
        self.fill= False
        self.text_id = None
        
        xmin = self.abs * self.size
        xmax = xmin + self.size
        ymin = self.ord * self.size
        ymax = ymin + self.size
        
        self.average_x = int(xmin + xmax) / 2
        self.average_y = int(ymin + ymax) / 2

    def _switch(self):
        """ Switch if the cell is filled or not. """
        self.fill= not self.fill

    def draw(self):
        """ order to the cell to draw its representation on the canvas """
        if self.master != None :
            fill = Cell.FILLED_COLOR_BG
            outline = Cell.FILLED_COLOR_BORDER

            if not self.fill:
                fill = Cell.EMPTY_COLOR_BG
                outline = Cell.EMPTY_COLOR_BORDER

            xmin = self.abs * self.size
            xmax = xmin + self.size
            ymin = self.ord * self.size
            ymax = ymin + self.size

            self.master.create_rectangle(xmin, ymin, xmax, ymax, fill = fill, outline = outline)
            
    def start_point(self):
        """ order to the cell to draw its representation on the canvas """
        if self.master != None :
            fill = Cell.START_COLOR_BG
            outline = Cell.START_COLOR_BORDER

            if not self.fill:
                fill = Cell.EMPTY_COLOR_BG
                outline = Cell.EMPTY_COLOR_BORDER

            xmin = self.abs * self.size
            xmax = xmin + self.size
            ymin = self.ord * self.size
            ymax = ymin + self.size

            self.master.create_rectangle(xmin, ymin, xmax, ymax, fill = fill, outline = outline)
            
    def end_point(self):
        """ order to the cell to draw its representation on the canvas """
        if self.master != None :
            fill = Cell.END_COLOR_BG
            outline = Cell.END_COLOR_BORDER
            if not self.fill:
                fill = Cell.EMPTY_COLOR_BG
                outline = Cell.EMPTY_COLOR_BORDER

            xmin = self.abs * self.size
            xmax = xmin + self.size
            ymin = self.ord * self.size
            ymax = ymin + self.size

            self.master.create_rectangle(xmin, ymin, xmax, ymax, fill = fill, outline = outline)
            
    def make_route(self):
        """ order to the cell to draw its representation on the canvas """
        if self.master != None :
            fill = Cell.ROUTE_COLOR_BG
            outline = Cell.ROUTE_COLOR_BORDER
            if not self.fill:
                fill = Cell.EMPTY_COLOR_BG
                outline = Cell.EMPTY_COLOR_BORDER

            xmin = self.abs * self.size
            xmax = xmin + self.size
            ymin = self.ord * self.size
            ymax = ymin + self.size

            self.master.create_rectangle(xmin, ymin, xmax, ymax, fill = fill, outline = outline)
            
    def label(self, value):
        if value != str(np.inf) and value != str("nan"):
            self.text_id = self.master.create_text(self.average_x, self.average_y, text=str(value), fill="black", font=('Helvetica 6'))
        
    def clear_label(self):
        if self.text_id:
            self.master.delete(self.text_id)
        else:
            self.text_id = None