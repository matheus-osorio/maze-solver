class Maze_Solver:
    def __init__(self,maze, codes):

        self.maze = [line.copy() for line in maze]
        self.unnasigned = codes['unnasigned']
        self.wall = codes['wall']
        self.assigned = codes['assigned']
        self.start = codes['start']
        self.finish = codes['finish']
        self.node = -1
        self.accounted = -2
        self.path = -3
        self.minPath = -4
        self.maxPath = -5
        self.sharedPath = -6
        self.width = len(self.maze)
        self.height = len(self.maze[0])
        self.ids = {}
        self.nodeList = {}

        self.results = []
    
    def solve(self, start, finish):
        self.prepare(start, finish)
        self.create_nodes()
        self.create_paths(*start)
        self.graph_path()
        return self.choose_paths()

    def make_name(self,i,j):
        return f'{"0" if i < 10 else ""}{i}-{"0" if j < 10 else ""}{j}'

    def prepare(self, start, finish):
        self.ids[0] = {
            'id': 0,
            'location': start,
            'connections': []
        }

        self.ids[1] = {
            'id': 1,
            'location': finish,
            'connections': []
        }

        startId = self.make_name(*start)
        finishId = self.make_name(*finish)

        self.nodeList[startId] = 0
        self.nodeList[finishId] = 1

        

    def move_choices(self, x, y):

        if self.maze[x][y] == self.wall:
            return []
        
        positions = []

        if x > 0  and self.maze[x-1][y] == self.assigned: positions.append('up')
        if x < self.width - 1 and self.maze[x+1][y] == self.assigned: positions.append('down')
        if y > 0 and self.maze[x][y-1] == self.assigned: positions.append('left')      
        if y < self.height - 1 and self.maze[x][y+1] == self.assigned: positions.append('right')

        return positions


    def create_nodes(self):
        for i in range(len(self.maze)):
            for j in range(len(self.maze[0])):
                locId = self.make_name(i,j)
                if locId in self.nodeList:
                    continue

                choices = self.move_choices(i,j)

                if len(choices) > 2:
                    id = len(self.nodeList)
                    self.ids[id] = {
                        'id': id,
                        'location': (i,j),
                        'connections': []
                    }

                    self.nodeList[locId] = id
    
    def create_paths(self,x, y):

        self.maze[x][y] = self.node
        currentId = self.nodeList[self.make_name(x,y)]
        while True:
            positions = self.move_choices(x,y)
            if not positions:
                break
            
            i,j = x,y
            path = []
            while True:
            
                positions = self.move_choices(i,j)
                
                if not positions:
                    break
                for position in positions:
                    if position == 'up':
                        i -= 1
                    if position == 'down':
                        i += 1
                    if position == 'left':
                        j -= 1
                    if position == 'right':
                        j += 1
                    break

                nodeNameId = self.make_name(i,j)
                
                if nodeNameId in self.nodeList:
                    newId = self.nodeList[nodeNameId]
                    self.create_paths(i,j)
                    self.ids[currentId]['connections'].append({
                        'id': newId,
                        'path': path,
                        'cost': len(path)
                    })
                    self.ids[newId]['connections'].append({
                        'id': currentId,
                        'path': path[::-1],
                        'cost': len(path)
                    })

                    break

                else:
                    self.maze[i][j] = self.accounted
                    path.append((i,j))


    def graph_path(self, picked = {'path': [], 'nodes':[]}, position = 0):
        if position == 1:
            realPath = [move for sublist in picked['path'] for move in sublist]
            self.results.append({
                'path': realPath,
                'nodes': picked['nodes'].copy(),
                'cost': len(realPath)
            })
            return
        picked['nodes'].append(position)
        node = self.ids[position]
        for conn in node['connections']:
            id = conn['id']
            if id in picked['nodes']:
                continue
            picked['path'].append(conn['path'])
            self.graph_path(picked,id)
            picked['path'].pop()
        
        picked['nodes'].pop()
    
    def choose_paths(self):
        minPath = self.results[0]
        maxPath = self.results[0]
        for result in self.results:
            if result['cost'] < minPath['cost']:
                minPath = result
            if result['cost'] > maxPath['cost']:
                maxPath = result
        
        self.paths = {
            'min': minPath,
            'max': maxPath
        }

    def simplified_nodes(self):
        nodes = {}

        for name in self.ids:
            nodes[name] = {}
            for conn in self.ids[name]['connections']:
                nodes[name][conn['id']] = {
                    'location': self.ids[conn['id']]['location'],
                    'cost': len(conn['path'])
                }
        
        return nodes
    
    def prepare_to_print(self):
        maze = self.maze
        maze = [line.copy() for line in maze]
        print('min equal max: ', self.paths['min']['cost'] == self.paths['max']['cost'])
        minPath = self.paths['min']['path']
        maxPath = self.paths['max']['path']

        minNodes = self.paths['min']['nodes']
        maxNodes = self.paths['max']['nodes']


        for direction in minPath:
            maze[direction[0]][direction[1]] = self.minPath
        
        for direction in maxPath:
            if maze[direction[0]][direction[1]] == self.minPath:
                 maze[direction[0]][direction[1]] = self.sharedPath
            else:
                 maze[direction[0]][direction[1]] = self.maxPath
        
        for node in minNodes:
            location = self.ids[node]['location']
            maze[location[0]][location[1]] = self.minPath
        
        for node in maxNodes:
            location = self.ids[node]['location']
            if maze[location[0]][location[1]] == self.minPath:
                 maze[location[0]][location[1]] = self.sharedPath
            else:
                 maze[location[0]][location[1]] = self.maxPath

        return maze




    def __str__(self):
        conversion = {
            self.wall: '■■',
            self.assigned: '  ',
            self.start: 'BB',
            self.finish: 'EE',
            self.node:'NN',
            self.accounted: '  ',
            self.path: '**'
        }
        text = ''
        for path in self.paths:
            maze = self.maze
            maze = [line.copy() for line in maze]

            directions = self.paths[path]['path']

            for direction in directions:
                maze[direction[0]][direction[1]] = self.path
            wall = [self.wall for line in maze[0]]
            maze.insert(0, wall.copy())
            maze.append(wall.copy())

            
            for line in maze:
                line.insert(0, self.wall)
                line.append(self.wall)
        
        
            for line in maze:
                for square in line:
                    text += conversion[square]
                text += '\n'
            
            text += '\n'*5



        return text
    


        
        
        
