from math import fabs
from xml.dom.expatbuilder import FragmentBuilder
import pytest 
import sys
sys.path.append( '../')
import grid

def test_hw_ratio():
    res = grid.Grid.get_height_and_width_from_max_and_ratio( 100, 4 ) 
    assert res[ 'x' ] == 20
    assert res[ 'y' ] == 80

def test_grid_created_from_config():
    max_nodes = 16
    hw_ratio = 1
    config = {
        'generate' :{
            'max_nodes' : max_nodes,
            'hw_ratio' : hw_ratio,
            #'edge_range' : 100,
            #'edge_minimum' : 100,
            #'impassible_percentage' : 100,
            #'cardnality' : 100
        }
    }

    my_grid = grid.Grid.from_config( config )
    print( f"edge_count: {my_grid.edges.count}" ) 
    my_edges = my_grid.edges.get_edges()
    #for edge in my_edges:
        ###print( f"{str(edge.source)} " )
       #print( f"{str(edge)} " )

    
    assert isinstance( my_grid, grid.Grid )
    #assert 
    

def test_get_nodes():
    max_nodes = 10
    hw_ratio = 1
    config = {
        'generate' :{
            'max_nodes' : max_nodes,
            'hw_ratio' : hw_ratio,
            #'edge_range' : 100,
            #'edge_minimum' : 100,
            #'impassible_percentage' : 100,
            #'cardnality' : 100
        }
    }

    my_grid = grid.Grid.from_config( config )
    #print( f"farthest_source: {my_grid.edges.farthest_source}")
    my_closest_node = my_grid.get_node( 0, 0 )
    #print( f"node: {my_closest_node}" )
    my_next_closest_east_node = my_grid.get_node( 1, 0 )
    #print( f"east_node: {my_next_closest_east_node}" )
    assert my_closest_node.is_west_of( my_next_closest_east_node )
    assert not my_closest_node.is_east_of( my_next_closest_east_node )
    assert not my_closest_node.is_south_of( my_next_closest_east_node )
    assert not my_closest_node.is_north_of( my_next_closest_east_node )

    my_next_closest_north_node = my_grid.get_node( 0, 1 )
    #print( f"north_node: {my_next_closest_north_node}" )
    assert not my_closest_node.is_west_of( my_next_closest_north_node )
    assert not my_closest_node.is_north_of( my_next_closest_north_node )
    assert my_closest_node.is_south_of( my_next_closest_north_node )
    assert not my_closest_node.is_north_of( my_next_closest_north_node )

    #test getting edge between two nodes
    #print( f"node: {my_closest_node}" )
    edge_to_north = my_closest_node.get_edge_to( my_next_closest_north_node )
    edge_to_north_two = my_closest_node.get_edge_to( my_next_closest_north_node )
    edge_from_north = my_next_closest_north_node.get_edge_to( my_closest_node )
    #print( f"{str(edge_to_north)}" )
    #print( f"{str(edge_from_north )}" )
    assert edge_to_north != edge_from_north
    assert edge_to_north == edge_to_north_two
    edge_to_east = my_closest_node.get_edge_to( my_next_closest_east_node )

    #my_farthest_node = my_grid.get_node( my_grid.edges.farthest_source.x, my_grid.edges.farthest_source.y )

def test_get_expand():
    max_nodes = 10
    hw_ratio = 1
    config = {
        'generate' :{
            'max_nodes' : max_nodes,
            'hw_ratio' : hw_ratio,
            #'edge_range' : 100,
            #'edge_minimum' : 100,
            #'impassible_percentage' : 100,
            #'cardnality' : 100
        }
    }

    #first test the first node. Should get two nodes
    my_grid = grid.Grid.from_config( config )
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