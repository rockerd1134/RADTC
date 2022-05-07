from calendar import c
from heapq import heapify
from queue import PriorityQueue
from tkinter import W
from turtle import up
from radtc import pather_base
from radtc.grid import Grid, Node
from radtc.pather_base import PatherBase

#page numbers refer to: http://idm-lab.org/bib/abstracts/papers/aaai02b.pdf


#I got this idea from https://github.com/vinayannam/Lifelong-A-star/blob/0c3a2c2caa4061180467e8d007b5ca70ae16b03f/util.py#L226
#it's a wrapper so that the queue has the same commands as the dlite psudo code
# key, node
class DlitePQ( ):
    def __init__( self ) -> None:
        self.queue = PriorityQueue()

    #view the key of the top thing in the queue
    def top_key( self) -> tuple:
        if self.queue.empty():
            return (float( 'inf '), float( 'inf' ) )
        else:
            return self.queue.queue[0][0]

    def top( self ) -> tuple:
        if self.queue.empty():
            return None
        else:
            return self.queue.queue[0][1]

    def pop( self ) -> tuple:
        return self.queue.pop()

    def insert( self, vertex: tuple ) -> None:
        self.queue.put( vertex )

    def remove( self, node: 'Node' ) -> None:
        try:
            removed = False
            for queued_node in self.queue.queue:
                if queued_node[ 1 ] == node:
                    self.queue.queue.remove( queued_node )
                    removed = True
            if removed:
                heapify( self.queue.queue )
        except ValueError as e:
            pass

    def contains( self, node ) -> bool:
        for queued_node in self.queue.queue:
            if queued_node[ 1 ] == node:
                return queued_node
        return False

    def update( self, node_tuple: tuple ) -> None:
        self.remove( node_tuple[1] )
        self.queue.put( node_tuple )




class PatherDLite( PatherBase ):
    
    #pg 5 ln 2
    def __init__( self, grid: 'Grid', start: 'Node', finish: 'Node' ) -> None:
        super().__init__( grid, start, finish )
        self.g_table = {}
        self.k_table = {}
        self.rhs_table = {}
        self.frontier = DlitePQ()
        self.k_m = 0

        #initialize all nodes to infinity
        for node in self.grid.get_nodes():
            self.g_table[ node ] = float( 'inf' )
            self.rhs_table[ node ] = float( 'inf' )

        #we are going to be going backwards so rhs from finish is 0
        self.rhs_table[ self.finish ] = 0

        #insert finish to queue with priority based on manhattan from finish to start
        #pg 5 ln 06
        self.frontier.insert( ( ( self.grid.get_manhattan_between_nodes( self.start, self.finish ), 0 ), self.finish ) )
        #print( self.frontier.queue.queue )

    #pg 5 ln 1
    def calculate_key( self, node ):
        key_0 = min( self.g_table[ node ], self.rhs_table[ node ] ) + self.grid.get_manhattan_between_nodes( self.start, node )
        key_1 = min( self.g_table[ node ], self.rhs_table[ node ] )
        return ( key_0, key_1 )

    #pg 5 ln 07
    def update_vertex( self, node ) -> None:
        if self.g_table[ node ] != self.rhs_table[ node ]:
            if self.frontier.contains( node ):
                self.frontier.update( ( self.calculate_key( node ), node ))
            else:
                self.frontier.insert( ( self.calculate_key( node ), node ) )
        elif self.g_table[ node ] == self.rhs_table[ node ]:
            self.frontier.remove( node )

    def get_rhs( self, node ) -> int:
        #rocekr start here
        min_rhs_a = [ float( 'inf' ) ]
        for sucessor in node.expand_for_successor_nodes():
            sucessor_rhs = self.g_table[ sucessor ] + node.get_cost_to( sucessor )
            min_rhs_a.append( sucessor_rhs )
        return min( min_rhs_a )

    def get_path (self) -> list[ 'Node' ]:
        if self.finish == self.start:
            return [ self.start ]
        else:
            path = [ ]
            path_step = self.start
            count = 0
            while path_step != self.finish and count < 150:
                if self.g_table[ path_step ] == float( 'inf' ):
                    print( f"path_step: {path_step} == inf")
                count += 1 
                path.append( path_step )
                #print( f"p: {path_step} g: {self.g_table[ path_step ]}" )
                next_step_cost = float( 'inf' )
                the_next_step = None
                for next_step in path_step.expand_for_successor_nodes( free_expand=True ):
                    #print( f"n: {next_step} g: {self.g_table[ next_step ]}" )
                    #if True:
                    if not next_step in path:
                        new_next_step_cost = self.g_table[ next_step ] + path_step.get_cost_to( next_step )
                        if  new_next_step_cost < next_step_cost:
                            #print( f"good next_step {next_step} {self.g_table[ next_step]}")
                            the_next_step = next_step
                            next_step_cost = new_next_step_cost
                path_step = the_next_step
                if path_step == None:
                    break
                    
                    #else:
                    #    print( f"bad next_step {next_step} {self.g_table[ next_step]}")
                    #    print( path )
                #exit(1)
            path.append( self.finish )
            return path

    def step( self ) -> dict:
        results = {
            'path': None,
            'solved': False
        }

        modded_edges = self.grid.get_last_edge_modifications()
        #check if modified edges effect anything in reached
        #to needed work for those
        if len( modded_edges ) > 0:
            self.k_m = self.k_m + self.grid.get_manhattan_between_nodes( self.start, self.finish )
            s_last = self.start
            for modded_edge in modded_edges:
#            #source = Node( self.grid, modded_edge.source )
                c_old = modded_edge[ 'was' ]
                c_new = modded_edge[ 'is' ]
                u = Node( self.grid, c_new.source )
                v = Node( self.grid, c_new.destination )
                #pg 5 ln 43
                #print( f"{c_old.cost} > {c_new.cost}")
                if c_old.cost > c_new.cost:
                    if u != self.finish:
                        self.rhs_table[ u ] = min( self.rhs_table[ u ], c_new.cost + self.g_table[ v ] )
                elif self.rhs_table[ u ] == c_old.cost + self.g_table[ v ]:
                    if u != self.finish:
                        self.rhs_table[ u ] = self.get_rhs( u )
                #else:
                #    print( f"{self.rhs_table[ u ]} == {c_old.cost} + {self.g_table[ v ]}" )
                self.update_vertex( u )

        #pg 5 ln 10
        if ( self.frontier.top_key() < self.calculate_key( self.start ) ) or self.rhs_table[ self.start ] > self.g_table[ self.start ]:
            #print( f"tk: {self.frontier.top_key()}" )
            current_node = self.frontier.top()
            k_old = self.frontier.top_key()
            k_new = self.calculate_key( current_node )
            #pg 5 ln 14
            if ( k_old < k_new ):
                self.frontier.update( ( k_new, current_node ) )
            #pg 5 ln 16
            elif self.g_table[ current_node ] > self.rhs_table[ current_node ]:
                self.g_table[ current_node ] = self.rhs_table[ current_node ]
                self.frontier.remove( current_node )
                for predecessor in current_node.expand_for_predecessor_nodes():
                    if predecessor != self.finish: 
                        #pg 5 ln 20
                        self.rhs_table[ predecessor ] = min( self.rhs_table[ predecessor ], ( self.g_table[ current_node ] + current_node.get_cost_to( predecessor ) ) )
                        self.update_vertex( predecessor )
            #pg 5 ln 23
            else:
                g_old = self.g_table[ current_node ]
                self.g_table[ current_node ] = float( 'inf' )
                #pg 5 ln 25
                for update_node in [ current_node ] + current_node.expand_for_predecessor_nodes():
                #for update_node in [ current_node ] + current_node.expand_for_predecessor_nodes():
                    #print( f"{update_node}  c {current_node}" )
                    if self.rhs_table[ update_node ] == update_node.get_cost_to( current_node ) + g_old:
                        if update_node != self.finish:
                            #pg 4 ln 27
                            self.rhs_table[ update_node ] = self.get_rhs( update_node )
                    self.update_vertex( update_node )
        #elif self.frontier.top_key() == self.calculate_key( self.start ):
        else: 
            current_node = self.frontier.top()
            if current_node == self.start:
                #print( f'start {self.g_table[ current_node ]} {self.rhs_table[ current_node]} ')
                self.update_vertex( current_node )
                #print( f'start {self.g_table[ current_node ]} {self.rhs_table[ current_node]} ')
                self.g_table[ current_node ] = self.rhs_table[ current_node ]
                #print( f'start {self.g_table[ current_node ]} {self.rhs_table[ current_node]} ')
            #for g in sorted( list(self.g_table.keys() ) ):
                #print( f"{g} {self.g_table[g]}")
            #print( self.g_table )
            results[ 'path' ] = self.get_path()
            results[ 'solved' ] = True



        #search here
        return results