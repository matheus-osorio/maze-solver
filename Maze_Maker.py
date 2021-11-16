import numpy as np
import numpy.random as rd

class Maze_Maker:
    unnasigned = 0
    wall = 1
    assigned = 2
    start = 3
    finish = 4
    def __init__(self, height, width):
        self.width = width
        self.height = height
    
    def make(self):
        #positional maze
        line = [self.unnasigned for i in range(self.width)]
        maze = [line.copy() for i in range(self.height)]
        self.positional = {
            'maze': maze,
            'shape': (len(maze), len(line))
        }

        #walled maze
        maze = []
        line = [self.assigned if i % 2 == 0 else self.wall for i in range((self.width-1) * 2) ]
        line.append(self.assigned)
        wall = [self.wall for i in range((self.width-1) * 2) ]
        wall.append(self.wall)
        for i in range(self.height - 1):
            maze.append(line.copy())
            maze.append(wall.copy())
        maze.append(line)
        self.walled = {
            'maze': maze,
            'shape': (len(maze), len(line))
        }
        self.path_finder(0,0)
        self.objectives = {
            'start': (0,0),
            'finish': (len(maze)-1, len(maze[0])-1)
        }
        maze[0][0] = self.start
        maze[-1][-1] = self.finish
        
        
        
    
    def path_finder(self, x,y):
        positions = self.available_positions(x,y)
        history = []
        history.append((x,y))
        while history:
            x,y = history.pop()
            positions = self.available_positions(x,y)
            while positions:
                choice = rd.choice(positions)
                history.append((x,y))
                (x,y) = self.make_path(x,y, choice)
                positions = self.available_positions(x,y)     
        return self.walled['maze']
    
    def available_positions(self, x,y):
        positions = []
        if y > 0 and self.positional['maze'][x][y-1] == self.unnasigned:
            positions.append('up')
        if y < self.positional['shape'][1]-1 and self.positional['maze'][x][y+1] == self.unnasigned:
            positions.append('down')
        if x > 0 and self.positional['maze'][x-1][y] == self.unnasigned:
            positions.append('left')
        if x < self.positional['shape'][0]-1 and self.positional['maze'][x+1][y] == self.unnasigned:
            positions.append('right')
        return positions
    
    def make_path(self, x,y, choice):
        posMaze = self.positional['maze']
        wallMaze = self.walled['maze']
        newX = x
        newY = y
        if choice == 'up':
            posMaze[x][y-1] = self.assigned
            wallMaze[x*2][y*2 - 1] = self.assigned
            newY -= 1
        
        elif choice == 'down':
            posMaze[x][y+1] = self.assigned
            wallMaze[x*2][y*2 + 1] = self.assigned
            newY += 1
        
        elif choice == 'left':
            posMaze[x-1][y] = self.assigned
            wallMaze[x*2 - 1][y*2] = self.assigned
            newX -= 1
        
        elif choice == 'right':
            posMaze[x+1][y] = self.assigned
            wallMaze[x*2 + 1][y*2] = self.assigned
            newX += 1
        
        return newX,newY

    def get_maze(self):
        maze = [line.copy() for line in self.walled['maze']]
        maze[0][0] = self.assigned
        maze[-1][-1] = self.assigned
        return maze

    
    def get_codes(self):
        return {
            'unnasigned': self.unnasigned,
            'wall': self.wall,
            'assigned': self.assigned,
            'start': self.start,
            'finish': self.finish
        }

    def get_objectives(self):
        return self.objectives

    def __str__(self):
        maze = self.get_maze()
        maze = [line.copy() for line in maze]
        wall = [self.wall for line in maze[0]]
        maze.insert(0, wall.copy())
        maze.append(wall.copy())
        for line in maze:
            line.insert(0, self.wall)
            line.append(self.wall)
        text = ''
        conversion = {
            self.wall: '■■',
            self.assigned: '  ',
            self.start: 'BB',
            self.finish: 'EE'
        }
        for line in maze:
            for square in line:
                text += conversion[square]
            text += '\n'
        return text
    






    








        