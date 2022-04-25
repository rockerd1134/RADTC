from abc import ABC, abstractmethod
from email.policy import default
from radtc import grid
import pygame as pg

class PatherBase(ABC):
    @abstractmethod
    def __init__( self, grid: 'Grid', start: 'Node', finish: 'Node' ) -> None:
        self.grid = grid
        self.start = start
        self.finish = finish
        self.font = pg.font.SysFont('Arial', 18, bold=True)

    @abstractmethod
    def step( self ) -> dict:
        ''' One iteration of the path finder routine'''
        pass

    @abstractmethod
    def renderNode(self, screen, color, row, col, square_side, margin) -> None:
        ''' Abstract for Special Render Cases '''
        self._defaultNode(screen, color, row, col, square_side, margin)

    def _defaultNode(self, screen, color, row, col, square_side, margin) -> None:
        ''' Default Rendering of Nodes '''
        pg.draw.rect(
            screen,
            color,
            (
                (margin + square_side) * row + margin,
                (margin + square_side) * col + margin,
                square_side,
                square_side
            )
        )
