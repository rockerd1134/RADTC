from abc import ABC, abstractmethod
from queue import Queue
from radtc import pather_base
from radtc.grid import Grid, Node
from radtc.pather_base import PatherBase

#This code inspried by https://www.redblobgames.com/pathfinding/a-star/introduction.html

class PatherBFS( PatherBase ):
    def __init__( self, grid: 'Grid', start: 'Node', finish: 'Node' ) -> None:
        super().__init__( grid, start, finish )
        self.frontier = Queue()
        self.frontier.put( start )
        self.reached = set()
        self.reached.add( start )
        self.came_from =  {}
        self.came_from[ start ] = None
        self.path = []

    def _get_path( self ):
        current = self.finish
        path = []
        count = 0
        while current != self.start and count < 102:
            #print( f"{count} {path}")
            count += 1
            path.append( current )
            current = self.came_from[ current ]
            #print( f"current: {current} cf: {self.came_from[ current ]}")
        path.append( self.start )
        return path
        #return path.reverse()

    def step( self ) -> dict:
        results = {
            'path': None,
            'solved': False,
        }
        ''' One iteration of the path finder routine'''
        current = self.frontier.get()
        
        for next in current.expand():
            if not next in self.came_from:
                self.frontier.put(next)
                self.came_from[ next ] = current

        if self.frontier.empty():
            results[ 'path' ] = self._get_path()
            results[ 'solved' ] = True
        return results
            
