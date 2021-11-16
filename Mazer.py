from Maze_Maker import Maze_Maker as Maker
from Maze_Solver import Maze_Solver as Solver
from Printer import Printer

maze = Maker(100,100)
maze.make()
solver = Solver(maze.get_maze(), maze.get_codes())
paths = solver.solve(**maze.get_objectives())
solved = solver.prepare_to_print()
printer = Printer(solved, maze.get_objectives(), 10)
printer.print()
print('Finished')