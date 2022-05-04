from heapq import heapify
from queue import PriorityQueue
from tkinter import W
from radtc import pather_base
from radtc.grid import Grid, Node
from radtc.pather_base import PatherBase

#page numbers refer to: https://www.cs.cmu.edu/~maxim/files/aij04.pdf
#page numbers refer to: Lifelong Planning A* by Sven Koenig

class PatherLPA( PatherBase ):
    def __init__( self, grid: 'Grid', start: 'Node', finish: 'Node' ) -> None:
        super().__init__( grid, start, finish )
        self.g_table = {} 
        self.rhs_table = {} 
        #preset this value. in lpa paper they do this for the whole grid
        self.g_table[ finish ] = float( 'inf' )
        self.rhs_table[ finish ] = float( 'inf' )
        self.g_table[ start ] = 0
        self.rhs_table[ start ] = 0
        self.h_table = {}
        self.pred = {} #nodes
        self.rhs_pred = {} #nodes
        #frontier queue will be populated with nodes
        #( priority, node, parent )
        self.frontier = PriorityQueue()
        self.frontier.put( ( self.calculate_key( self.start ), self.start, self.start ) )

        self.cost = {} #edges
        self.source = {} #edges

    #the hueristic funtion
    # in the grid case we use manhattan
    def get_hueristic(self, node: 'Node' ):
        return node.get_manhattan_to( self.finish )

    #pg 29 line 01
    def calculate_key(self, node ):
        g = self.g_table.get( node, float( 'inf' ) )
        if g == None:
            g = float( 'inf' )
        rhs = self.rhs_table.get( node, float( 'inf' ) )
        if rhs == None:
            rhs = float( 'inf' )

        g_rhs = min( g, rhs )
        #g_rhs = min( self.g_table.get( node, float( 'inf' ) ), self.rhs_table.get( node, float( 'inf' )) )
        return ( g_rhs + self.get_hueristic( node ), g_rhs )

    def traceback_path(self):
        path_back = []
        if self.finish in self.g_table:
            if self.g_table[ self.finish ] != float( 'inf' ):
            #maybe implement the traceback?
                current_node = self.finish
                while current_node != self.start:
                    path_back.append( current_node )
                    #this should always be true
                    if current_node in self.pred:
                        current_node = self.pred[ current_node ]
                path_back.append( current_node )
#            else:
#                print( self.g_table )
#                print( self.rhs_table )
#                print( self.pred )
#                print( self.rhs_pred )
#                print( "finish not found" )
        return path_back

    #looks at the g values of all the nodes surrounding this node
    #and looks the cost to reach this node from those nodes
    #and returns the cheapest
    #pg 29 line 09
    def get_rhs( self, node: 'Node' ) -> int:
        #print( f"get_rhs: {node}")
        min_rhs = None
        min_rhs_node = None
#        if not node in self.g_table:
#            print( f"get_rhs {node} not in gtable")
#        if node in self.pred:
#            print( f"get_rhs parent for {node} is {self.pred[ node ]}")
        for adjacent in node.expand():
#            print( f"a: {adjacent}")
            #if adjacent == self.finish:
            #    exit(1)
            if adjacent in self.g_table:
                #print( f"a: {adjacent} in table {self.g_table[ adjacent ]}")
                adjacent_rhs = adjacent.get_cost_to( node ) + self.g_table[ adjacent ]
                if not adjacent.get_cost_to( node ) == None:
                    if min_rhs == None:
                        min_rhs = adjacent_rhs
                        min_rhs_node = adjacent
                    elif min_rhs > adjacent_rhs:
                        min_rhs = adjacent_rhs
                        min_rhs_node = adjacent
                    else:
                        pass
                else:
                    print( 'no edge to this node')
                    pass
            else:
                #we have never encountered this node
                #It needs to be queued for expansion before we use it for 
                #print( f"a: {adjacent} not in table")
                pass
#        if min_rhs == float( 'inf' ):
#            print( f'min rhs is inf {node}' )

            #exit(1)
            if min_rhs == None:
                min_rhs = float( 'inf' )
        return { 'rhs': min_rhs, 'source': min_rhs_node }

    def update_vertex( self, node: 'Node' ) -> None:
        #print( f"uv: {node}" )
        #pg 29 line 09
        if node != self.start:
            rhs = self.get_rhs( node )
#            print( f"node: {node} rhs: {rhs}" )
            self.rhs_table[ node ] =  rhs[ 'rhs' ]
            self.rhs_pred[ node ] = rhs[ 'source' ]
            #if this is the first time we've seen this node
            #if not node in self.g_table:
                #this is actually pg11 ln 03
            #    self.g_table[ node ] =  float( 'inf' )
                #self.pred[ node ] = rhs[ 'source' ]


            #pg 29 line 10
            try: 
                #we can access the underlying list in the priority queue
                #and run heapify to reoganice at a cost of 0(N) + 0(NlogN)
                for queued_node in self.frontier.queue:
                    if queued_node[ 1 ] == node:
#                        print( f'removing: {node}' )
                        self.frontier.queue.remove( queued_node )
                heapify( self.frontier.queue )
            except ValueError as e:
                #The node was not in the queue
                pass
    
            #pg 29 line 11
            if not node in self.g_table:
                if rhs[ 'source' ] in self.g_table:
                    if node == self.finish:
                        #this node needs to be processed next
                        to_insert = ( (0,0), node, rhs[ 'source' ] )
                    else:
                        to_insert = ( self.calculate_key( node ), node, rhs[ 'source' ] )
                    #print( f"inserted: {to_insert}" )
                    self.frontier.put( to_insert )
            elif self.g_table[ node ] != self.rhs_table[ node ]:
#                if not rhs[ 'source' ] in self.g_table:
#                    print( f"no source {rhs[ 'source' ]} for {node}")
                if node == self.finish:
                    #this node needs to be processed next
                    to_insert = ( (0,0), node, rhs[ 'source' ] )
                else:
                    to_insert = ( self.calculate_key( node ), node, rhs[ 'source' ] )
                self.frontier.put( to_insert )

#                to_insert = ( self.calculate_key( node ), node, rhs[ 'source' ] )
                #print( f"inserted: {to_insert}" )
#                self.frontier.put( to_insert )


    #one iteration of the search i.e. expanding one node
    #returns results
    def step( self ) -> dict:
        results = {
            'path': None,
            'solved': False,
        }
        modded_edges = self.grid.get_last_modified_edges()
        #check if modified edges effect anything in reached
        #to needed work for those
        for modded_edge in modded_edges:
#            #source = Node( self.grid, modded_edge.source )
            destination = Node( self.grid, modded_edge.destination )
#            #if source in self.g_table:
#                #self.update_vertex( source )
            if destination in self.g_table:
                self.update_vertex( destination )

#        print( self.frontier.queue ) 
        #pg 11 ln 09
#        if not self.frontier.empty():
#          print( self.frontier.queue[0] )
#          print( self.calculate_key( self.finish ) )
#          print( 'not empty' )
#        else:
#          print( 'empty')
        #pg 29 ln 12 ( while (U.TopKey() <˙ CalculateKey(sgoal) OR rhs(sgoal) 6= g(sgoal)))
        #if self.frontier.queue[0][1] != self.finish or self.rhs_table[ self.finish ] != self.g_table[ self.finish ]:
        if ( self.frontier.queue[0][0] < self.calculate_key( self.finish ) and self.frontier.queue[0][1] != self.finish ) or ( self.rhs_table[ self.finish ] != self.g_table[ self.finish ] and self.g_table[ self.finish ] != float( 'inf') ):

            #pg 11 ln 10 POP
            current_tuple = self.frontier.get()
            #print( f"ct: {current_tuple}" )
            ( key, current_node, parent ) = current_tuple
            #print( self.frontier.queue )
#            print( f"ct_g: {self.g_table.get( current_node, 'na' )}")
#            print( f"ct_rhs: {self.rhs_table.get( current_node, 'na' )}")
            #if current_node == self.finish:
            #    print( self.g_table[ self.finish ])
            #    print( self.rhs_table[ self.finish ])
            #    exit(1)
        
            #lets check if we've seen this node before
            #This is to avoid prepopulating all teh states as inf
            if not current_node in self.g_table: 
#                print( f"ct_set_g_1: {current_node} {parent}" )
                self.g_table[ current_node ] = float( 'inf' )
                self.pred[ current_node ] = parent
            if not current_node in self.rhs_table:
#                print( f"ct_set_h_1: {current_node} {parent}" )
                self.rhs_table[ current_node ] = self.g_table[ current_node ]
                self.rhs_pred[ current_node ] = self.pred[ current_node ]
                #self.g_table[ current_node ] = self.g_table[ parent ] + parent.get_cost_to( current_node )
            
            #pg 11 line 111
            #this means the node is locally inconsistent and we will modify it's g_table 
            #and pred
            if self.g_table[ current_node ] > self.rhs_table[ current_node ]:
#                print( "locally inconst" )
                self.g_table[ current_node ] = self.rhs_table[ current_node ]
                self.pred[ current_node ] = self.rhs_pred[ current_node ]
                #this is added because it will put finish into queue and it will run one more time
                #if current_node == self.finish:
#                    print( self.g_table[ self.finish ])
#                    print( self.rhs_table[ self.finish ])
                    #self.frontier.put( ( self.calculate_key( self.finish ), current_node, parent ) )
                    #pass
                #else:
                #print( f'current g215: {current_node}  {self.g_table[ current_node]}')
                for successor in current_node.expand():
                    self.update_vertex( successor )
            else:
#                print( "locally const" )
                if current_node != self.start:
                    self.g_table[ current_node ] = float( 'inf' )
                #print( f'current g224: {current_node} {self.g_table[ current_node]} {self.rhs_table[ current_node ]}')
                self.update_vertex( current_node )
                #print( f'current g226: {current_node} {self.g_table[ current_node]} {self.rhs_table[ current_node ]}')
                for successor in current_node.expand():
                    self.update_vertex( successor )

        elif self.frontier.queue[0][1] == self.finish:
            #print( f'current g229: {self.finish} {self.g_table[ self.finish]}')
            self.update_vertex( self.finish )
            #print( f'current g233: {self.finish} {self.g_table[ self.finish]}')
            #print( self.frontier.queue )
            #exit(1)
            if self.g_table[ self.finish ] > self.rhs_table[ self.finish ]:
                self.g_table[ self.finish ] = self.rhs_table[ self.finish ]
                self.pred[ self.finish ] = self.rhs_pred[ self.finish ]
#        else:
            if self.g_table[ self.finish ] != float( 'inf' ):
                #we have found a path
                results[ 'solved' ] = True
                results[ 'path' ] = list( reversed( self.traceback_path() ) )
            else:
                results[ 'solved' ] = False

        #print( self.g_table[ self.finish ])
        #print( self.rhs_table[ self.finish ])
                
        return results


