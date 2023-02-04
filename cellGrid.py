from tkinter import *
from graph import Graph
import numpy as np
from cell import Cell

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
        self.bind("<Button-1>", self.handleMouseClick)  
        #bind moving while clicking
        self.bind("<B1-Motion>", self.handleMouseMotion)
        #bind release button action - clear the memory of midified cells.
        self.bind("<ButtonRelease-1>", lambda event: self.switched.clear())
        
        # TODO: search and see how to handle a right mouse click 
        self.bind("<Button-3>", self.handle_start_and_end_points)


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
            self.display_costs()

                        
        # reset state
        elif self.end_coord and self.start_coord:
            start_cell = self.grid[self.start_coord[0]][self.start_coord[1]]
            end_cell = self.grid[self.end_coord[0]][self.end_coord[1]]

            start_cell._switch()
            start_cell.start_point()
            end_cell._switch()
            end_cell.end_point()
            self.display_route(self.route)
            self.clear_costs()
            
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
                
    def display_costs(self):
        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                cell.label(f'{self.graph.grid[y, x]:.1f}') 
                
    def clear_costs(self):
        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                cell.clear_label() 
                self.graph.grid[y, x] = np.inf

            
        
            
