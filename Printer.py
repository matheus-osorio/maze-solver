import cv2
import numpy as np
class Printer:
    def __init__(self, maze, points, repeat=1):
        self.maze = maze
        self.repeat = repeat
        self.points = points
    
    def prepare(self):
        maze = [line.copy() for line in self.maze]
        line = len(maze)
        column = len(maze[0])
        maze[self.points['start'][0]][self.points['start'][1]] = 10
        maze[self.points['finish'][0]][self.points['finish'][1]] = 11
        

        for i in range(line-1,-1,-2):
            repeat = maze[i]
            for j in range(self.repeat):
                maze.insert(i,repeat.copy())
        
        for line in maze:
            for j in range(column-1, -1, -2):
                repeat = line[j]
                for k in range(self.repeat):
                    line.insert(j,repeat)
        wall = [1 for v in maze[0]]
        maze.insert(0,wall.copy())
        maze.append(wall.copy())

        for line in maze:
            line.insert(0,1)
            line.append(1)
        
        self.maze = maze
        
    
    def print(self):
        self.prepare()
        self.make_maze({
            1: (0,0,0),
            10: (162,179,18),
            11: (16,51,176),
            'default': (255,255,255)
        }, 'empty.png')

        self.make_maze({
            1: (0,0,0),
            -4: (0,255,0),
            -5: (0,0,255),
            -6: (0,255,255),
            10: (162,179,18),
            11: (16,51,176),
            'default': (255,255,255)
        }, 'path.png')

    
    
    def make_maze(self, colors, name):

        maze = []

        for line in self.maze:
            colored = []
            for square in line:
                if square in colors:
                    colored.append(colors[square])
                else:
                    colored.append(colors['default'])
            maze.append(colored)
        
        
        shape = (len(maze), len(maze[0]), 3)
        lined_maze = [value for line in maze for square in line for value in square]

        maze = np.array(lined_maze)
        maze = maze.reshape(shape)
        cv2.imwrite(name, maze)

        
        
        

            