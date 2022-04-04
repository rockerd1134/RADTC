from abc import ABC, abstractmethod
from queue import PriorityQueue
from radtc import pather_base
from radtc.grid import Grid, Node
from radtc.pather_base import PatherBase

class PatherASP( PatherBase ):
    def __init__( self, grid: 'Grid', start: 'Node', finish: 'Node' ) -> None:
        super().__init__( grid, start, finish )
        self.f_table = {}  #
        #reached is keyed by node and containes a dictary { node, parent }
        self.reached = {}
        self.path_back = []
        #f_table is a hash of the cost + huersitic cost for each node (i.e. cost estimate)
        self.f_table[ start ] = 0
        self.last = None
        #the frontier will be filled with prioritized path segments
        # from one adjacent node to another
        # ( pririty: int, start: Node, parent: Node )
        self.frontier = PriorityQueue()
        self.frontier.put( ( self.get_priority( start ), start, start ))
  
    #the hueristic funtion
    # in the grid case we use manhattan
    def get_priority(self, node: 'Node' ):
        return self.f_table[ node ] + node.get_manhattan_to( self.finish )

    
    #one iteration of the search i.e. expanding one node
    #returns results
    def step( self ) -> dict:
        results = {
            'path': None,
            'solved': False,
        }
    
        current_path_segment = self.frontier.get()
        self.reached[ current_path_segment[1] ] = { 
            'node': current_path_segment[1], 
            'parent': current_path_segment[2] 
        }
        #self.last = current[1] 
        
        if current_path_segment[1] == self.finish:
            #We found our end result
            path_node = self.reached[ self.finish ]
            while not path_node[ 'node' ] == path_node[ 'parent' ]:
                self.path_back.append( path_node )
                path_node = self.reached[ path_node[ 'parent' ] ]
            self.path_back.append( path_node )

            path = []
            while len( self.path_back ) > 0:
                path.append( self.path_back.pop(-1)[ 'node' ] )
            results[ 'solved' ] = True
            results[ 'path' ] = path
            #results[ 'path ' ] = self.path_back
        else:
            #expand current node
            adjacents = current_path_segment[1].expand()
            for adj_node in adjacents:
                #an edge is ( 'from node', 'to node', 'cost' )
                if adj_node == current_path_segment[2]:
                    #This is the previous node
                    #This is the pruning A star part
                    pass
                else:
                    #print( current_path_segment[1] )
                    #print( self.f_table )
                    cost_from_current = self.f_table[ current_path_segment[1] ] + current_path_segment[1].get_cost_to( adj_node )
                    if adj_node in self.f_table:            
                        #we've seen this node
                        if cost_from_current < self.f_table[ adj_node ]:
                            #this new path is cheaper than our previous path
                            self.f_table[ adj_node ] = cost_from_current
                            #maybe we will checkout it out
                            #( priority, current, parent )
                            self.frontier.put( ( self.get_priority( adj_node ), adj_node, current_path_segment[1] ))
                    else: 
                        self.f_table[ adj_node ] = cost_from_current  
                        self.frontier.put( ( self.get_priority( adj_node ), adj_node, current_path_segment[1] ))
        return results



###### FROM HW 1
#from queue import PriorityQueue
#class aStar:
#  def __init__(self, geo_map, start, finish ):
#    self.get_map = geo_map
#    self.queue = PriorityQueue()
#    self.f_table = {}
#    self.start = start
#    self.finish = finish
#    self.reached = {}
#    self.path_back = []
#    self.f_table[ start ] = 0
#    #self.last = None
#    self.current = None #for logging only
#    #astar value, node, parent
#    self.queue.put( ( self.get_priority( start ), start, start ))
#
#  #logging helper
#  def log_step(self):
#    #print( f"reached: {self.reached}" )
#    #print( "f_table: <")
#    #print( self.f_table )
#    print( f"(Log) Expanding: {self.current[1]}   with Estimated cost: {self.current[0]}" )
#
#  #the hueristic funtion
#  def get_priority(self, node):
#    return self.f_table[ node ] + self.get_map.lines.get_line( node )[1]
#    
#  #one iteration of the search i.e. expanding one node
#  def step(self):
#    #queue node ( 'priority', 'node', 'came_from' )
#    current = self.queue.get()
#    self.reached[ current[1] ] = { 'node': current[1], 'parent': current[2] }
#    #self.last = current[1] 
#    self.current = current
#    
#    
#    if current[1] == self.finish:
#      #We found our end result
#      return True
#    else:
#      #expand current node
#      edges = self.get_map.edges.get_node_edges( current[1] )
#      for edge in edges:
#        #an edge is ( 'from node', 'to node', 'cost' )
#        if edge[1] == current[2]:
#          #This is the previous node
#          #print( 'not checking parent')
#          pass
#        else:
#          cost_from_current = self.f_table[ current[1] ] + edge[2]
#          if edge[1] in self.f_table:            
#            if cost_from_current < self.f_table[ edge[1] ]:
#              self.f_table[ edge[1] ] = cost_from_current
#              self.queue.put( ( self.get_priority( edge[1]), edge[1], edge[0] ))
#          else: 
#            self.f_table[ edge[1] ] = cost_from_current  
#            self.queue.put( ( self.get_priority( edge[1] ), edge[1], edge[0] ))