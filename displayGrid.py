from tkinter import *
from graph import Graph
import time

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

class CellGrid(Canvas):
    def __init__(self,master, rowNumber, columnNumber, cellSize, *args, **kwargs):
        Canvas.__init__(self, master, width = cellSize * columnNumber , height = cellSize * rowNumber, *args, **kwargs)
        self.graph = Graph((rowNumber, columnNumber))
        self.start_coord = False
        self.end_coord = False
        self.route = False

        self.cellSize = cellSize

        self.grid = []
        for row in range(rowNumber):

            line = []
            for column in range(columnNumber):
                line.append(Cell(self, column, row, cellSize))

            self.grid.append(line)

        #memorize the cells that have been modified to avoid many switching of state during mouse motion.
        self.switched = []

        #bind click action
        # self.bind("<Button-1>", self.handleMouseClick)  
        #bind moving while clicking
        self.bind("<B1-Motion>", self.handleMouseMotion)
        #bind release button action - clear the memory of midified cells.
        self.bind("<ButtonRelease-1>", lambda event: self.switched.clear())
        
        # TODO: search and see how to handle a right mouse click 
        self.bind("<Button-1>", self.handle_start_and_end_points)


        self.draw()



    def draw(self):
        for row in self.grid:
            for cell in row:
                cell.draw()

    def _eventCoords(self, event):
        row = int(event.y / self.cellSize)
        column = int(event.x / self.cellSize)
        return row, column

    def handleMouseClick(self, event):
        row, column = self._eventCoords(event)
        cell = self.grid[row][column]
        cell._switch()
        cell.draw()
        
        if cell.fill:
            try:
                self.graph.define_rect_object((row, column), (row, column))
            except ValueError:
                pass
        else:
            try:
                self.graph.define_rect_object((row, column), (row, column), clear=True)
            except ValueError:
                pass
        
        #add the cell to the list of cell switched during the click
        self.switched.append(cell)

    def handleMouseMotion(self, event):
        row, column = self._eventCoords(event)
        cell = self.grid[row][column]

        if cell not in self.switched:
            cell._switch()
            cell.draw()
            self.switched.append(cell)
            if cell.fill:
                try:
                    self.graph.define_rect_object((row, column), (row, column))
                except ValueError:
                    pass
            else:
                try:
                    self.graph.define_rect_object((row, column), (row, column), clear=True)
                except ValueError:
                    pass
            
    def handle_start_and_end_points(self, event):
        row, column = self._eventCoords(event)
        cell = self.grid[row][column]
        # end state
        if self.start_coord and not self.end_coord:
            cell._switch()
            cell.end_point()
            self.end_coord = (row, column)
            
            self.route = self.graph.a_star(self.start_coord, self.end_coord)
            self.display_route(self.route)
            print(self.graph.grid)
                        
        # reset state
        elif self.end_coord and self.start_coord:
            start_cell = self.grid[self.start_coord[0]][self.start_coord[1]]
            end_cell = self.grid[self.end_coord[0]][self.end_coord[1]]

            start_cell._switch()
            start_cell.start_point()
            end_cell._switch()
            end_cell.end_point()
            self.display_route(self.route)
            
            self.end_coord = False
            self.start_coord = False
            #delete route on map
                        
        else:
            cell._switch()
            cell.start_point()
            self.start_coord = (row, column)
            #add the cell to the list of cell switched during the click
            # self.switched.append(cell)
            
    def display_route(self, route: list, clear: bool=False):
        for step in route:
            if step == self.start_coord or step == self.end_coord:
                continue
            else:
                route_cell = self.grid[step[0]][step[1]]
                route_cell._switch()
                route_cell.make_route()
            
        
            


if __name__ == "__main__" :
    app = Tk()
    size_x = 5
    size_y = 5
    cell_size = 25

    grid = CellGrid(app, size_y, size_x, cell_size)
    grid.pack()

    app.mainloop()