### CONWAY'S GAME OF LIFE FOR NEOMATRIX
### ALI ASHRAFY 2025

# from matrixbase import MatrixBase
from copy import deepcopy
import random



class Life:
    def __init__(self, x, y):
        # Create Grid
        # NOTE: Columns = x, rows = y
        # I.e Columns = 32, rows = 16

        self.columns = x
        self.rows = y
        
        grid = []
        for i in range(y):
            row = []
            for j in range(x):
                row.append(0)
            grid.append(row)

        self.grid = grid



    def clear_grid(self):
        x = self.columns
        y = self.rows
        grid = []
        for i in range(y):
            row = []
            for j in range(x):
                row.append(0)
            grid.append(row)

        self.grid = grid

    def set_grid(self, initial="glider-gun"):
        # NOT DONE
        # Have a variety of pre-set grids that have cool patterns.
        pass          

    def randomise_grid(self):
        x = self.columns
        y = self.rows
        grid = []
        for i in range(y):
            row = []
            for j in range(x):
                row.append(random.choice([0,1]))
            grid.append(row)

        self.grid = grid

    def _check_neighbors(self, current_grid, x, y):
        neighbor_count = 0
        neighbors = []

        if ( (x >= 1 and x < len(current_grid) - 1) and (y >= 1 and y < len(current_grid[0]) - 1)):
            neighbors = [ current_grid[x - 1][y - 1], current_grid[x][y - 1], current_grid[x + 1][y - 1], current_grid[x + 1][y], current_grid[x + 1][y + 1], current_grid[x][y + 1], current_grid[x - 1][y + 1], current_grid[x - 1][y] ]

        for neighbor in neighbors:
            if neighbor: neighbor_count += 1
        
        return neighbor_count
    
    def tick(self):
        # Tick the game forward by one
        previous_grid = deepcopy(self.grid)

        for i in range(1, self.rows):
            for j in range(1, self.columns):
                neighbors = self._check_neighbors(self.grid, i, j)
                
                if neighbors > 3:
                    previous_grid[i][j] = False

                elif neighbors < 2:
                    previous_grid[i][j] = False

                elif neighbors == 2:
                    if previous_grid[i][j] == True:
                        previous_grid[i][j] = True
                    
                    else:
                        previous_grid[i][j] = False
                
                elif neighbors == 3:
                    previous_grid[i][j] = True

        return previous_grid
