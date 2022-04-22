from math import fabs
from xml.dom.expatbuilder import FragmentBuilder
import pytest 
import sys
sys.path.append( '../')
import grid

@pytest.fixture
def my_grid():
    config = {
        'generate' :{
            'height' :10,
            'width' : 9,
            'edge_max' : 100,
            'edge_minimum' : 1,
                #'impassible_percentage' : 100,
            'cardnality' : 10
        }
    }
    
    #first test the first node. Should get two nodes
    my_grid = grid.Grid.from_config( config )
    return my_grid

def test_grid_created_from_config( my_grid ):
    print( f"edge_count: {my_grid.edges.count}" ) 
    my_edges = my_grid.edges.get_edges()
    assert isinstance( my_grid, grid.Grid )
    

#def test_get_nodes(my_grid):
#    #print( f"farthest_source: {my_grid.edges.farthest_source}")
#    my_closest_node = my_grid.get_node( 0, 0 )
#    #print( f"node: {my_closest_node}" )
#    my_next_closest_east_node = my_grid.get_node( 1, 0 )
#    #print( f"east_node: {my_next_closest_east_node}" )
#    assert my_closest_node.is_west_of( my_next_closest_east_node )
#    assert not my_closest_node.is_east_of( my_next_closest_east_node )
#    assert not my_closest_node.is_south_of( my_next_closest_east_node )
#    assert not my_closest_node.is_north_of( my_next_closest_east_node )
#
#    my_next_closest_north_node = my_grid.get_node( 0, 1 )
#    #print( f"north_node: {my_next_closest_north_node}" )
#    assert not my_closest_node.is_west_of( my_next_closest_north_node )
#    assert not my_closest_node.is_north_of( my_next_closest_north_node )
#    assert my_closest_node.is_south_of( my_next_closest_north_node )
#    assert not my_closest_node.is_north_of( my_next_closest_north_node )
#
#    #test getting edge between two nodes
#    #print( f"node: {my_closest_node}" )
#    edge_to_north = my_closest_node.get_edge_to( my_next_closest_north_node )
#    edge_to_north_two = my_closest_node.get_edge_to( my_next_closest_north_node )
#    edge_from_north = my_next_closest_north_node.get_edge_to( my_closest_node )
#    #print( f"{str(edge_to_north)}" )
#    #print( f"{str(edge_from_north )}" )
#    assert edge_to_north != edge_from_north
#    assert edge_to_north == edge_to_north_two
#    edge_to_east = my_closest_node.get_edge_to( my_next_closest_east_node )
#
#    #my_farthest_node = my_grid.get_node( my_grid.edges.farthest_source.x, my_grid.edges.farthest_source.y )
#


def test_get_eges_and_nodes( my_grid ):
    nodes = my_grid.get_nodes()
    for node in sorted( nodes ):
        print( node )
    farthest_source = my_grid.edges.farthest_source
    print( f"farthest_source: {farthest_source}" )

    edges = my_grid.get_edges()
    for edge in sorted( edges ):
        print( edge )

def test_get_expand(my_grid):
    my_closest_node = my_grid.get_node( 0, 0 )
    print( f"node: {my_closest_node}" )
    next_doors = my_closest_node.expand()
    for node in next_doors:
      print( node )

    my_interesting_node = my_grid.get_node( 3, 2 )
    print( f"node: {my_interesting_node}" )
    next_doors = my_interesting_node.expand()
    for node in next_doors:
      print( node )

    farthest_source = my_grid.edges.farthest_source
    print( f"farthest_source: {farthest_source}" )
    my_farthest_node = my_grid.get_node( farthest_source.x, farthest_source.y )
    print( f"node: {my_farthest_node}" )
    next_doors = my_farthest_node.expand()
    for node in next_doors:
      print( node )

    assert grid.Node.expands == 3
