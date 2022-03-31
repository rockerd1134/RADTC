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

    def __gt__( self, other: 'GridLocation' ):
        if other == None:
            return True
        else: 
            if self.x > other.x:
                return True
            elif self.x == other.x and self.y > other.y:
                return True
            else:
                return False

    def __lt__( self, other: 'GridLocation' ):
        if other == None:
            return True
        else: 
            if self.x < other.x:
                return True
            elif self.x == other.x and self.y < other.y:
                return True
            else:
                return False

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
        if other == None:
            return False
        return self.source == other.source and self.destination == other.destination and self.cost == other.cost

    def __gt__( self, other: 'Edge' ):
        if other == None:
            return True
        else: 
            if self.source > other.source:
                return True
            elif self.source == other.source and self.destination > other.destination:
                return True
            else:
                return False

    def __lt__( self, other: 'Edge' ):
        if other == None:
            return False
        else: 
            if self.source < other.source:
                return True
            elif self.source == other.source and self.destination < other.destination:
                return True
            else:
                return False
    
    def __hash__( self ):
        return str( self )

class Edges:
    def __init__(self, edges: list[Edge] ) -> None:
        #we store an edge map which is dictionary keyed by Nodes, with all connectiong nodes 
        self.edge_map = {}
        self.count = len( edges )
        self.farthest_source = None

        for edge in sorted( edges ):
            if not edge.source in self.edge_map:
                self.edge_map[ edge.source ] = { }
            self.edge_map[ edge.source ][ edge.destination ] = edge
            #set farthest edge
            if not isinstance( self.farthest_source, GridLocation ):
                self.farthest_source = edge.source
            #print( edge )
            if self.farthest_source.x <= edge.source.x and self.farthest_source.y <= edge.source.y:
                self.farthest_source = edge.source

    def get_node_edges( self, node ):
        edges = []
        for edge in list( self.edge_map[ node ].keys() ):
            edges.append( self.edge_map[ node ][ edge ] ) 
        return edges

    def get_edges( self ) -> list[ 'Edge' ]:
        edges = []
        for node in list( self.edge_map.keys() ):
            for edge in list( self.edge_map[ node ].keys() ):
                edges.append( self.edge_map[ node ][ edge ] ) 
        return edges

    def get_edge_between_locations( self, src_loc, dest_loc ) -> 'Edge':
        if src_loc in self.edge_map:
            if dest_loc in self.edge_map[ src_loc ]:
                return self.edge_map[ src_loc ][ dest_loc ]
        return None


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
    def get_height_and_width_from_max_and_ratio( cls, max: int, ratio: int ) -> dict:
        x = int( max / ( ratio + 1 ) )
        y = int ( ratio * x  )
        return { 'x': x, 'y':y, 'node_count': x * y, 'edge_count': x * y - x - y }

    @classmethod
    def _get_edge_cost_on_create( cls ):
        return 10


    @classmethod
    def from_config( cls, config: dict ) -> 'Grid':
        '''Creates a grid object from a config dictionary'''

        if 'generate' in config:
            #max_nodes = int( config[ 'generate' ].get( 'max_nodes', 100) )
            #hw_ratio = int( config[ 'generate' ].get( 'hw_ratio', 1) )
            height = int( config[ 'generate' ].get( 'height', 10) )
            width = int( config[ 'generate' ].get( 'height', 10) )
            edge_range = int( config[ 'generate' ].get( 'edge_range', 100) )
            edge_minimum = int( config[ 'generate' ].get( 'edge_minimum', 1) )
            impassible_percentage = int( config[ 'generate' ].get( 'impassible_percentage', 0) )
            cardnality = int( config[ 'generate' ].get( 'cardnality', 0) )

            #node_counts = Grid.get_height_and_width_from_max_and_ratio( max_nodes, hw_ratio )
            x_max = width - 1
            y_max = height - 1

            edges = []
            for x in range( width ):
                for y in range( height ):
                    #print( f"{x},{y}" )
                    next_x = x + 1
                    next_y = y + 1
                    #make edge to the East
                    if next_x <= x_max:
                        east_edge_forward = Edge( 
                            GridLocation( x,  y ), 
                            GridLocation( next_x, y ), 
                            Grid._get_edge_cost_on_create()    
                        )
                        east_edge_backward = Edge( 
                            GridLocation( next_x,  y ), 
                            GridLocation( x, y ), 
                            Grid._get_edge_cost_on_create()    
                        )
                        edges.append( east_edge_forward )
                        edges.append( east_edge_backward )
                    
                    #make edge to the North
                    if next_y <= y_max:
                        north_edge_forward = Edge( 
                            GridLocation( x,  y ), 
                            GridLocation( x, next_y ), 
                            Grid._get_edge_cost_on_create()    
                        )
                        north_edge_backward = Edge( 
                            GridLocation( x,  next_y ), 
                            GridLocation( x, y ), 
                            Grid._get_edge_cost_on_create()    
                        )
                        edges.append( north_edge_forward )
                        edges.append( north_edge_backward )

            return Grid( edges )

    @classmethod
    def adjacent_north_of( cls, location: 'GridLocation' ) -> 'GridLocation':
        return GridLocation( location.x, location.y + 1 )

    @classmethod
    def adjacent_east_of( cls, location: 'GridLocation' ) -> 'GridLocation':
        return GridLocation( location.x + 1, location.y )

    @classmethod
    def adjacent_south_of( cls, location: 'GridLocation' ) -> 'GridLocation':
        return GridLocation( location.x, location.y - 1 )

    @classmethod
    def adjacent_west_of( cls, location: 'GridLocation' ) -> 'GridLocation':
        return GridLocation( location.x - 1, location.y )

    def location_is_in_bounds( self, loc: 'GridLocation' ) -> bool:
        if loc.x >= self.GRID_X_START_INDEX and loc.y >= self.GRID_Y_START_INDEX:
            #how to check max range?
            if loc.x <= self.edges.farthest_source.x and loc.y <= self.edges.farthest_source.y:
                return True
        return False

    def get_node( self, x: int, y: int ) -> 'Node':
        loc = GridLocation( x, y )
        if self.location_is_in_bounds( loc ):
            return Node( self, loc )
        else: 
            return None

    #This is expensive 
    def get_nodes( self ) -> set[ 'Node' ]:
        ''' Get's all possible edge source and destination'''
        nodes = set()
        for edge in self.get_edges():
            if not edge.source in nodes:
                nodes.add( edge.source ) 
            if not edge.destination in nodes:
                nodes.add( edge.destination ) 
        return nodes

    def get_edges( self ) -> list[ 'Edge' ]:
        return self.edges.get_edges()

    def get_node_at_location( self, loc: 'GridLocation' ) -> 'Node':
        if self.location_is_in_bounds( loc ):
            return Node( self, loc )
        else: 
            return None

    def get_edge_between_locations( self, src_loc: 'GridLocation', dest_loc: 'GridLocation' ) -> 'Edge':
        if self.location_is_in_bounds( src_loc ) and self.location_is_in_bounds( dest_loc ):
            return self.edges.get_edge_between_locations( src_loc, dest_loc )
        else:
            return None

    def get_edge_between_nodes( self, src: 'Node', dest: 'Node' ) -> 'Edge':
        return self.get_edge_between_locations( src.location, dest.location )

class Node:

    expands = 0
    ''' A class that represents a node but is really an interface for 4 edges'''
    def __init__( self,  grid: 'Grid', grid_location: 'GridLocation' ) -> None:
        self.location = grid_location
        self.grid = grid

    def __str__( self ):
        return str( self.location )

    #### gets
    def expand( self ) -> list[ 'Node' ]:
        ''' returns adjacent nodes N,E,W,S '''
        #record the expantion
        self.__class__.expands += 1

        nodes = []
        north = self.get_adjacent_north()
        if north:
            nodes.append( north )
        east = self.get_adjacent_east()
        if east:
            nodes.append( east )
        south = self.get_adjacent_south()
        if south:
            nodes.append( south )
        west = self.get_adjacent_west()
        if west:
            nodes.append( west )
        return nodes


        
        pass

    def get_adjacent_north( self ) -> 'Node':
        return self.grid.get_node_at_location( self.grid.adjacent_north_of( self.location ) )

    def get_adjacent_east( self ) -> 'Node':
        return self.grid.get_node_at_location( self.grid.adjacent_east_of( self.location ) )

    def get_adjacent_south( self ) -> 'Node':
        return self.grid.get_node_at_location( self.grid.adjacent_south_of( self.location ) )

    def get_adjacent_west( self ) -> 'Node':
        return self.grid.get_node_at_location( self.grid.adjacent_west_of( self.location ) )


    def get_edge_to( self, node: 'Node' ) -> 'Edge':
        if self.is_adjacent( node ):
            return self.grid.get_edge_between_nodes( self, node )
        else:
            return None

    #### tests
    def is_adjacent( self, node: 'Node' ) -> bool:
        ''' checks if node is reachable '''
        if ( self.is_adjacent_east_of( node ) 
            or self.is_adjacent_west_of( node ) 
            or self.is_adjacent_north_of( node ) 
            or self.is_adjacent_south_of( node ) ):
            return True
        else:
            return False

    def is_north_of( self, node: 'Node' ) -> bool:
        ''' checks if node is north of a node'''
        if node.location.y < self.location.y: 
            return True
        else: 
            return False

    def is_west_of( self, node: 'Node' ) -> bool:
        ''' checks if node is west of a node'''
        if node.location.x > self.location.x: 
            return True
        else: 
            return False

    def is_south_of( self, node: 'Node' ) -> bool:
        ''' checks if node is south of a node'''
        if node.location.y > self.location.y: 
            return True
        else: 
            return False

    def is_east_of( self, node: 'Node' ) -> bool:
        ''' checks if node is east of a node'''
        if node.location.x < self.location.x: 
            return True
        else: 
            return False

    def is_adjacent_north_of( self, node: 'Node' ) -> bool:
        ''' checks if node is north of a node'''
        if node.location.y + 1 == self.location.y: 
            return True
        else: 
            return False

    def is_adjacent_west_of( self, node: 'Node' ) -> bool:
        ''' checks if node is west of a node'''
        if node.location.x - 1 == self.location.x: 
            return True
        else: 
            return False

    def is_adjacent_south_of( self, node: 'Node' ) -> bool:
        ''' checks if node is south of a node'''
        if node.location.y - 1 == self.location.y: 
            return True
        else: 
            return False

    def is_adjacent_east_of( self, node: 'Node' ) -> bool:
        ''' checks if node is east of a node'''
        if node.location.x + 1 ==  self.location.x: 
            return True
        else: 
            return False


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
