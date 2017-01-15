import itertools
import random

random.seed(27)

class Cell:
    def __init__(self, x, y):
        self.parent = None
        self.x, self.y = x, y

    def find(self):                 # The root of the tree representing the set this Cell is a part of
        if self.parent is None:
            return self
        ret = self.parent.find()
        # path compression
        self.parent = ret
        return ret

    def union(self, other):
        self.find().parent = other.find()

    def __repr__(self):
        return f'Cell({self.x}, {self.y})'


class Edge:
    def __init__(self, cellA, cellB, x, y, orientation):
        self.cellA, self.cellB = cellA, cellB
        self.x, self.y = x, y
        self.orientation = orientation
        self.isRemoved = False

    def cellsSeparated(self):
        return self.cellA.find() is not self.cellB.find()

    def remove(self):
        self.cellA.union(self.cellB)
        self.isRemoved = True

    def __repr__(self):
        return f"Edge({self.cellA}, {self.cellB}, {self.x}, {self.y}, '{self.orientation}')"


class Maze:
    def __init__(self, width, height):
        self.width, self.height = width, height             # Corresponds to number of cells
        self.cells = {(x,y): Cell(x,y) for x,y in itertools.product(range(width), range(height))}

        self.edges = {}
        for x in range(width):
            for y in range(height):
                current = self.cells[x,y]
                right = self.cells.get((x+1,y))
                down = self.cells.get((x,y+1))
                if right is not None:
                    self.edges[x,y,'vertical'] = Edge(current, right, x, y, 'vertical')
                if down is not None:
                    self.edges[x,y,'horizontal'] = Edge(current, down, x, y, 'horizontal')

        unprocessedEdges = list(self.edges.values())
        while unprocessedEdges:
            edge = random.choice(unprocessedEdges)
            if edge.cellsSeparated():
                edge.remove()
            unprocessedEdges.remove(edge)

    # def __str__(self):
    #     char = 'X'          # How an edge is drawn
    #     grid = [[' ']*2*self.width for y in range(2*self.height)]
    #     for coord, edge in self.edges.items():
    #         x, y, orientation = coord
    #         if edge.isRemoved:
    #             continue
    #         if orientation == 'vertical':
    #             if y-1 >= 0:
    #                 grid[2*y-1][2*x] = char
    #             grid[2*y][2*x] = char
    #             if y+1 < self.height:
    #                 grid[2*y+1][2*x] = char

    #         else:   # orientation == 'horizontal'
    #             if x-1 >= 0:
    #                 grid[2*y][2*x-1] = char
    #             grid[2*y][2*x] = char
    #             if x+1 < self.width:
    #                 grid[2*y][2*x+1] = char

    #     return '\n'.join(''.join(row) for row in grid)

    def resultsToHtml(self):
        script = ''
        length = 20
        for edge in self.edges.values():
            if edge.isRemoved:
                continue
            if edge.orientation == 'vertical':
                script += f'ctx.moveTo({length*(edge.x+1)}, {length*edge.y});\n'
                script += f'ctx.lineTo({length*(edge.x+1)}, {length*(edge.y+1)});\n'
            else:
                script += f'ctx.moveTo({length*edge.x}, {length*(edge.y+1)});\n'
                script += f'ctx.lineTo({length*(edge.x+1)}, {length*(edge.y+1)});\n'

        template = open('template.html').read()
        script = template.replace('//template//', script)
        open('result.html', 'w').write(script)

maze = Maze(30, 30)
maze.resultsToHtml()
