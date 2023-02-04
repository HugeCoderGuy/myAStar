import numpy as np
from heapq import heappop, heappush


#TODO research how to make a visual respresntaion of this A*
class Node():
    def __init__(self, value: int, position: tuple):
        """Node class to represent graph data structure

        Args:
            value (int): Value greater than 0. Initialized to np.inf
            position (tuple): tuple of form (y, x) with (0,0) in top left of grid
        """
        self.value = value
        self.position = position
        self.neighbor = []
        
    def set_neighbor(self, node: tuple):
        self.neighbor.append(node)
        
    def drop_neighbor(self, index: tuple):
        self.neighbor.remove(index)
        


class Graph():
    def __init__(self, grid_size: tuple):
        """Parent class to track grid nodes and a path between them
        
        self.grid maintains high level grid structure in np.array()
        self.node_log stores node classes with a query to their index location
        
        All graph nodes in network are initalized to a value of np.inf with
        with all adjacent nodes preset as neighbors

        Args:
            grid_size (tuple): number of nodes that make up the grid with 0 
            index and of form (y, x)
        """
        self.grid = np.full(grid_size, np.inf)
        self.node_log = {}
        self.x_bound = grid_size[1] - 1 # drop the 1 base index to 0 based index
        self.y_bound = grid_size[0] - 1
        
        # establish all points in grid as nodes with corresponding neighbors
        for y, row in enumerate(self.grid):
            for x, node_value in enumerate(row):
                current_node = Node(node_value, (y, x))
                self.node_log[(y, x)] = current_node
                # corner cases with references to other nodes as directions suchas North East as NE
                # top left corner
                if x == 0 and y == 0:
                    current_node.set_neighbor((0, 1))
                    current_node.set_neighbor((1, 0))
                    current_node.set_neighbor((1, 1))
                # top right corner
                elif x == self.x_bound and y == 0:
                    current_node.set_neighbor((0, self.x_bound - 1)) # node to left
                    current_node.set_neighbor((1, self.x_bound)) # node below
                    current_node.set_neighbor((1, self.x_bound - 1)) # node adjacent
                # bottom left node at corner
                elif x == 0 and y == self.y_bound:
                    current_node.set_neighbor((self.y_bound, 1)) # to the E
                    current_node.set_neighbor((self.y_bound - 1, 1)) # adjacent NE
                    current_node.set_neighbor((self.y_bound - 1, 0)) # N
                # bottom right corner
                elif x == self.x_bound and y == self.y_bound:
                    current_node.set_neighbor((self.y_bound, self.x_bound - 1)) # node to left
                    current_node.set_neighbor((self.y_bound - 1, self.x_bound - 1)) # node NE
                    current_node.set_neighbor((self.y_bound, self.x_bound)) # node N
                    
                # edge cases with corners staisfied 
                # top edge
                elif y == 0:
                    for i in range(x-1, x+2):
                        if i == x:
                            current_node.set_neighbor((y + 1, x))
                        else:
                            current_node.set_neighbor((y, i))
                            current_node.set_neighbor((y + 1, i))
                # West edge
                elif x == 0:
                    for j in range(y-1, y+2):
                        if j == y:
                            current_node.set_neighbor((y, x + 1)) # East
                        else:
                            current_node.set_neighbor((j, x))
                            current_node.set_neighbor((j, x + 1))
                # South edge
                elif y == self.y_bound:
                    for i in range(x-1, x+2):
                        if i == x:
                            current_node.set_neighbor((y - 1, x))
                        else:
                            current_node.set_neighbor((y, i))
                            current_node.set_neighbor((y - 1, i))
                # West edge
                elif x == self.x_bound:
                    for j in range(y-1, y+2):
                        if j == y:
                            current_node.set_neighbor((y, x - 1)) # East
                        else:
                            current_node.set_neighbor((j, x))
                            current_node.set_neighbor((j, x - 1))
                            
                # final node case has neighbors surrounding everywhere
                else:
                    for j in range(y-1, y+2):
                        for i in range(x-1, x+2):
                            # avoid setting curent node as its own neighbor
                            if i == x and j == y:
                                continue
                            else:
                                current_node.set_neighbor((j, i))
                                
                                
    def define_rect_object(self, from_index: tuple, to_index: tuple, clear:bool = False):
        """Creates a blocking oject that prevents path traversal
        
        Current design has all object nodes dropping relations to other nodes.
        Could be optimized by orphaning nodes within object bounderies from
        external nodes.

        Args:
            from_index (tuple): one corner of rectangular object
            to_index (tuple): other corner of rectangular object
        """
        # capture rectangular bounderies of boject
        x_min = min([from_index[1], to_index[1]])
        x_max = max([from_index[1], to_index[1]])
        y_min = min([from_index[0], to_index[0]])
        y_max = max([from_index[0], to_index[0]])
        
        if not clear:
            # iterate through neighbors of each object node and remove relationship
            for j in range(y_min, y_max + 1):
                for i in range(x_min, x_max + 1):
                    current_node = self.node_log[(j, i)]
                    current_node.value = None
                    self.grid[j][i] = None
                    for neighbor in current_node.neighbor:
                        # current_node.drop_neighbor(neighbor)
                        self.node_log[neighbor].drop_neighbor((j, i))
                        
        else:
            # iterate through neighbors of each object node and remove relationship
            for j in range(y_min, y_max + 1):
                for i in range(x_min, x_max + 1):
                    current_node = self.node_log[(j, i)]
                    current_node.value = np.inf
                    self.grid[j][i] = np.inf
                    for neighbor in current_node.neighbor:
                        # current_node.set_neighbor(neighbor)
                        self.node_log[neighbor].set_neighbor((j, i))
                    
                    
    
    # TODO implement a min heap or something to track 
    def a_star(self, from_node: tuple, to_node: tuple) -> list:
        """Classic A* search algorithm with euclidian heuristic

        Args:
            from_node (tuple): starting or current location
            to_node (tuple): final location

        Raises:
            AttributeError: if no path is found, error is raised

        Returns:
            list: list containing path of nodes (y, x) from start to finish
        """
        dist_between_nodes = 1
        count = 0
        paths_and_distances = {}
        for coord, node in self.node_log.items():
            paths_and_distances[node.position] = [node.value, [node.position]]
            
        paths_and_distances[from_node][0] = 0
        vertices_to_explore = [(0, from_node)]
        self.grid[from_node[0]][from_node[1]] = self.h(from_node, to_node)
        
        while vertices_to_explore and paths_and_distances[to_node][0] == np.inf:
            current_distance, current_node = heappop(vertices_to_explore)
            for neighbor in self.node_log[current_node].neighbor:
                new_distance = current_distance + dist_between_nodes + self.h(neighbor, to_node)
                new_path = paths_and_distances[current_node][1] + [self.node_log[neighbor].position]
            
                if new_distance < paths_and_distances[neighbor][0]:
                    paths_and_distances[neighbor][0] = new_distance
                    paths_and_distances[neighbor][1] = new_path
                    heappush(vertices_to_explore, (new_distance, neighbor))
                    count += 1
                    self.grid[neighbor[0]][neighbor[1]] = new_distance
        
                
        print("Found a path from {0} to {1} in {2} steps: ".format(from_node, to_node, count), paths_and_distances[to_node][1])
    
        return paths_and_distances[to_node][1]

        
        # while to_explore:
        #     current_node = None# find the min value from heap as next node
        #     if current_node == to_node:
        #         visited.append(current_node)
        #         break
            
        #     for neighbor in self.node_log[current_node].neighbor:
        #         current_cost = (self.h(neighbor, to_node) + 
        #                                 self.h(neighbor, from_node))
        #         # if neighbor in to_explore:
        #         if current_cost < self.node_log[neighbor].value:
        #             self.node_log[neighbor].value = current_cost
                
        #         if neighbor not in visited:
        #             to_explore.append(neighbor)
                    
        #     visited.append(current_node)
        #     to_explore.remove(current_node)
            
        # if current_node != to_node:
        #     raise AttributeError("No path to goal!")
                
        
        
    
    def h(self, from_index: tuple, to_index: tuple):
        # returns heuristic distance between two nodes
        # print("h is from", from_index, "to", to_index, ": ", np.sqrt((to_index[1] - from_index[1])**2 + (to_index[0] - from_index[0])**2))
        return np.sqrt((to_index[1] - from_index[1])**2 + (to_index[0] - from_index[0])**2)
    
        
        
if __name__ == "__main__":
    # note that graph is instantiated with 1 index, but nodes are set with 0 index
    graph = Graph((4,4))
    
    
    # Below code test the object instatiation in graph 
    node_in_question = (1 , 1)
    print(graph.node_log[node_in_question].neighbor)

    graph.define_rect_object((1,1),(2,2))
    print(graph.grid)
    print(graph.node_log[node_in_question].neighbor)
    
    # help(np.full)

    
        
        
