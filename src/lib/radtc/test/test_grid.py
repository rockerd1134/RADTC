import pytest 
import sys
sys.path.append( '../')
import grid

def test_hw_ratio():
    res = grid.Grid.get_height_and_width_from_max_and_ratio( 100, 4 ) 
    assert res[0] == 20
    assert res[1] == 80

def test_grid_created_from_config():
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
    print( f"edge_count: {my_grid.edges.count}" ) 
    print( f"farthest_source: {my_grid.edges.farthest_source}")
    my_edges = my_grid.edges.get_edges()
    for edge in my_edges:
        print( f"{str(edge.source)}" )
    
    assert isinstance( my_grid, grid.Grid )
    #assert len( my_grid.edges == 20 * 2 + 18 * )