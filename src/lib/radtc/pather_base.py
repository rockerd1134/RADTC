from abc import ABC, abstractmethod
from radtc import grid

class PatherBase(ABC):
    @abstractmethod
    def __init__( self, grid: 'Grid', start: 'Node', finish: 'Node' ) -> None:
        self.grid = grid
        self.start = start
        self.finish = finish

    @abstractmethod
    def step( self ) -> dict:
        ''' One iteration of the path finder routine'''
        pass
