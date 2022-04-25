import enum
import time
from radtc.grid import Grid, Node
import pygame as pg

class RadtcGUI:
    def __init__(self, grid: 'Grid', landmarks) -> None:
        #Colors
        self.START = (88, 47, 14)
        self.FINISH = (51, 61, 41)
        self.FRONTIER = (166, 138, 100)
        self.PATH = (127, 79, 36)
        self.PATH_SOLVED = (88, 47, 14)
        self.BACKGROUND = (164, 172, 134)
        
        #Grid
        self.grid = grid
        self.GRID_HEIGHT = grid.height
        self.GRID_WIDTH = grid.width

        #Squares
        self.SQUARE_SIDE = 50
        self.SQUARE_MARGIN = 20
        
        #Landmarks
        self.start = landmarks['start']
        self.finish = landmarks['finish']
        self.path = []
        self.solved = False

        #Window
        self.WINDOW_HEIGHT = (self.GRID_HEIGHT * self.SQUARE_SIDE) + (self.GRID_HEIGHT * self.SQUARE_MARGIN) + self.SQUARE_MARGIN
        self.WINDOW_WIDTH = (self.GRID_WIDTH * self.SQUARE_SIDE) + (self.GRID_WIDTH * self.SQUARE_MARGIN) + self.SQUARE_MARGIN

        print (self.WINDOW_HEIGHT, self.WINDOW_WIDTH)
        pg.init()
    
    def setup(self):
        self.screen = pg.display.set_mode([self.WINDOW_WIDTH, self.WINDOW_HEIGHT])
        pg.display.set_caption("RADTC Runner")

        self.clock = pg.time.Clock()
        self.pause = "play"

        self.font = pg.font.SysFont('Arial', 11, bold=True)

    def setPatherRender(self, patherRender):
        self.patherRender = patherRender

    def runGui(self) -> bool:
        self.screen.fill(self.BACKGROUND)
        self.drawGrid()

        pg.display.update()
        for ev in pg.event.get():
            if ev.type == pg.QUIT:
                pg.display.quit()
                pg.quit()
                return 'end'
            elif ev.type == pg.MOUSEBUTTONDOWN:
                print (ev)
            elif ev.type == pg.KEYDOWN:
                if ev.key == pg.K_SPACE:
                    self.pause = "pause" if self.pause == "play" else "play"
        return self.pause

    def updatePath(self, path, solved=False):
        self.path = path
        self.solved = solved


    def drawGrid(self) -> None:
        for row in range(self.GRID_WIDTH):
            for col in range(self.GRID_HEIGHT):
                self.drawSquare(row, col)
                self.drawWeights(row, col)

    def drawSquare(self, row, col) -> None:
        node = self.grid.get_node(row, col)
        color = self.FRONTIER
        special = False
        if node.location == self.start:
            color = self.START if not self.solved else self.PATH_SOLVED
            special = True

        elif node.location == self.finish:
            color = self.FINISH if not self.solved else self.PATH_SOLVED
            special = True

        elif node in self.path:
            color = self.PATH if not self.solved else self.PATH_SOLVED
            special = True
        
        self.patherRender(self.screen, color, row, col, self.SQUARE_SIDE, self.SQUARE_MARGIN, special)

    def drawWeights(self, row, col) -> None:
        node = self.grid.get_node(row, col)
        adj_nodes = [node.get_adjacent_east(), node.get_adjacent_north(), node.get_adjacent_west(), node.get_adjacent_south()]
        #placement offsets [(x1, y1, x2, y2, text_x, text_y)]
        offsets = [(50, 10, 25, 10, -13, 0), (10, 50, 10, 25, 0, -13), (0, 35, 50, 35, 0, 0), (35, 0, 35, 50, 0, 0)]
        #[node.get_adjacent_east(), node.get_adjacent_north(), node.get_adjacent_west(), node.get_adjacent_south()]

        for index, adj_node in enumerate(adj_nodes):
            if adj_node:
                #weight
                x1 = ((self.SQUARE_MARGIN + self.SQUARE_SIDE) * node.location.x + self.SQUARE_MARGIN) + offsets[index][0]
                y1 = ((self.SQUARE_MARGIN + self.SQUARE_SIDE) * node.location.y + self.SQUARE_MARGIN) + offsets[index][1]
                x2 = ((self.SQUARE_MARGIN + self.SQUARE_SIDE) * adj_node.location.x + self.SQUARE_MARGIN) + offsets[index][2]
                y2 = ((self.SQUARE_MARGIN + self.SQUARE_SIDE) * adj_node.location.y + self.SQUARE_MARGIN) + offsets[index][3]
            
                pg.draw.line(self.screen, (0, 0, 0), (x1, y1), (x2, y2))

                text = self.font.render(f'{self.grid.get_edge_between_nodes(node, adj_node).cost}', True, (0, 0, 0))

                x_m_point = (x1 + x2)//2
                y_m_point = (y1 + y2)//2
                text_rect = text.get_rect()
                text_rect.center = (x_m_point + offsets[index][4], y_m_point + offsets[index][5])
                self.screen.blit(text, text_rect)



        


