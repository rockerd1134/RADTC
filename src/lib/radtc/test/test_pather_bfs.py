import pytest
import sys
sys.path.append( '../..')

from radtc.grid import Grid
from radtc.pather_bfs import patherBFS

@pytest.fixture
def my_grid():
    config = {
        'generate' :{
            'height' : 10,
            'width' : 10
                #'edge_range' : 100,
                #'edge_minimum' : 100,
                #'impassible_percentage' : 100,
                #'cardnality' : 100
        }
    }
    
    #first test the first node. Should get two nodes
    my_grid = Grid.from_config( config )
    return my_grid

def test_patherBSF( my_grid ):

    bfs = patherBFS( my_grid, my_grid.get_node(  0, 0 ), my_grid.get_node( 1, 3))

    result = { 'path': None }
    emergency_break_count = 102
    count = 0
    while result[ 'path' ] == None and count < emergency_break_count:
        count += 1
        result = bfs.step()
        print( result )
        print( sys.getsizeof( bfs ))