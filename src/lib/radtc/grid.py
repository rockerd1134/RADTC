class GridLocation: 
    def __init__( self, x: int, y: int ) -> None:
        self.x = x
        self.y = y

    def __str__( self ) -> str:
        return( f"x: {self.x} y: {self.y}" )

    def __eq__( self, other: 'GridLocation' ):
        if other == None:
            return False
        return self.x == other.x and self.y == other.y

    def __hash__( self ):
        return self.x * 1000000 + self.y 

class Edge:
    def __init__( self, source: GridLocation, destination: GridLocation, cost: int ) -> None:
        self.source = source
        self.destination = destination
        self.cost = cost

    def __str__( self ):
        return f"{self.source} -( {self.cost} )-> {self.destination}"

    def __eq__( self, other ):
        return self.source == other.source and self.desitnation == other.destination and self.cost == other.cost
    
    def __hash__( self ):
        return str( self )

class Edges:
  def __init__(self, edges: list[Edge] ) -> None:
    #we store an edge map which is dictionary keyed by Nodes, with all connectiong nodes 
    self.edge_map = {}
    self.count = len( edges )
    self.farthest_source = None

    for edge in edges:
        print( edge )
        if not edge.source in self.edge_map:
            self.edge_map[ edge.source ] = { }
        self.edge_map[ edge.source ][ edge.destination ] = edge
        #set farthest edge
        if not isinstance( self.farthest_source, GridLocation ):
            self.farthest_source = edge.source

        if self.farthest_source.x <= edge.source.x and self.farthest_source.y <= edge.source.y:
            self.farthest_source = edge.source

  def get_node_edges( self, node ):
    edges = []
    for edge in list( self.edge_map[ node ].keys() ):
        edges.append( self.edge_map[ node ][ edge ] ) 
    return edges

  def get_edges( self ):
    edges = []
    for node in list( self.edge_map.keys() ):
        for edge in list( self.edge_map[ node ].keys() ):
            edges.append( self.edge_map[ node ][ edge ] ) 
    return edges


#containes the needed information for creating a grid
class GridConfig:
    def __init__( self, **kwargs ) -> None:
        self.config = {}

class Grid: 

    GRID_X_START_INDEX = 0
    GRID_Y_START_INDEX = 0

    def __init__( self, edges: list[ Edge ] ) -> None:
        self.height = None 
        self.width = None 
        self.edges = Edges( edges )
        #self.lines = Lines( lines )
    
    def __str__( self ) -> str:
        output = 'Edges:\n'
        for edge in self.edges.get_edges():
            output += f'{edge}\n'
        output += 'Lines:\n'
#        for line in self.lines.get_lines():
#            output += f'{line}\n'
#        return str( output )

    @classmethod
    def get_height_and_width_from_max_and_ratio( cls, max: int, ratio: int ) -> tuple:
        x = int( max / ( ratio + 1 ) )
        y = int ( ratio * x  )
        return ( x, y )

    @classmethod
    def _get_edge_cost_on_create( cls ):
        return 10


    @classmethod
    def from_config( cls, config: dict ) -> 'Grid':
        '''Creates a grid object from a config dictionary'''

        if 'generate' in config:
            max_nodes = int( config[ 'generate' ].get( 'max_nodes', 100) )
            hw_ratio = int( config[ 'generate' ].get( 'hw_ratio', 1) )
            edge_range = int( config[ 'generate' ].get( 'edge_range', 100) )
            edge_minimum = int( config[ 'generate' ].get( 'edge_minimum', 1) )
            impassible_percentage = int( config[ 'generate' ].get( 'impassible_percentage', 0) )
            cardnality = int( config[ 'generate' ].get( 'cardnality', 0) )

            node_counts = Grid.get_height_and_width_from_max_and_ratio( max_nodes, hw_ratio )
            x_max = node_counts[0] 
            y_max = node_counts[1] 

            edges = []
             
            
            for x in range( x_max ):
                for y in range( y_max ):
                    #make edge to the East
                    if x + 1 <= x_max:
                        east_edge_forward = Edge( 
                            GridLocation( x,  y ), 
                            GridLocation( x + 1, y ), 
                            Grid._get_edge_cost_on_create()    
                        )
                        east_edge_backward = Edge( 
                            GridLocation( x + 1,  y ), 
                            GridLocation( x, y ), 
                            Grid._get_edge_cost_on_create()    
                        )
                        edges.append( east_edge_forward )
                        edges.append( east_edge_backward )
                    
                    #make edge to the North
                    if y + 1 <= y_max:
                        north_edge_forward = Edge( 
                            GridLocation( x,  y ), 
                            GridLocation( x, y + 1 ), 
                            Grid._get_edge_cost_on_create()    
                        )
                        north_edge_backward = Edge( 
                            GridLocation( x,  y + 1 ), 
                            GridLocation( x, y ), 
                            Grid._get_edge_cost_on_create()    
                        )
                        edges.append( north_edge_forward )
                        edges.append( north_edge_backward )

            return Grid( edges )

                
            #genorator has
            #  max nodes
            #  h/w ratio
            #  edge range
            #  max 
            #  min
            #  cardnality


        return cls()

    @classmethod
    def adjacent_north_of( cls, location: GridLocation ) -> GridLocation:
        return GridLocation( location.x, location.y + 1 )

    @classmethod
    def adjacent_east_of( cls, location: GridLocation ) -> GridLocation:
        return GridLocation( location.x + 1, location.y )

    @classmethod
    def adjacent_south_of( cls, location: GridLocation ) -> GridLocation:
        return GridLocation( location.x, location.y - 1 )

    @classmethod
    def adjacent_west_of( cls, location: GridLocation ) -> GridLocation:
        return GridLocation( location.x - 1, location.y )


class Node:
    ''' A class that represents a node but is really an interface for 4 edges'''
    def __init__( self,  grid: 'Grid', grid_location: 'GridLocation' ) -> None:
        self.location = grid_location
        self.grid = grid

    def expand( self ):
        ''' returns adjacent nodes N,E,W,S '''
        pass

    def is_adjacent( self, node: 'Node' ) -> bool:
        ''' checks if node is reachable '''
        pass

    def is_north_of( self, node: 'Node' ) -> bool:
        ''' checks if node is north of a node'''
        pass

    def is_west_of( self, node: 'Node' ) -> bool:
        ''' checks if node is west of a node'''
        pass

    def is_south_of( self, node: 'Node' ) -> bool:
        ''' checks if node is south of a node'''
        pass

    def is_east_of( self, node: 'Node' ) -> bool:
        ''' checks if node is east of a node'''
        pass




#class Lines:
#  def __init__( self, lines ):
#    self.line_map = {}
#    for line in lines:
#      self.line_map[ line[0] ] = line[1]
#
#  def get_lines( self ):
#    lines = []
#    for node in list( self.line_map.keys() ):
#        lines.append( ( node, self.line_map[ node ] ))
#    return lines
#
#  def get_line( self, node ):
#    return ( node, self.line_map[ node ] )
