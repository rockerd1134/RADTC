import pytest
import sys
import yaml
sys.path.append( '../..')
from radtc.radtc_runner import Runner



#def test_runner():
#    config = {
#        'grid': {
#            'generate': {
#                'height': 100,
#                'width' : 100
#            }
#        },
#        'run' : {
#            'start': {
#                'x': 0,
#                'y': 0
#            },
#            'finish': {
#                'x': 50,
#                'y': 70
#            },
#            #'pather_module_lib_path' : r"C:\Users\rocker\Documents\Personal\classes\MS State\Spring 2022\AI\git\RADTC\src\lib\radtc\",
#            'pather_module' : 'radtc.pather_bfs',
#            'pather_class': 'PatherBFS'
#        }
#    }
#
#    runner = Runner( config )
#    runner.run()
#    print( runner.get_report() )
#
#
#def test_runner_astar_prune_random_edges():
#    config = {
#        'grid': {
#            'generate': {
#                'height': 100,
#                'width' : 100,
#                'edge_max' : 100,
#                'edge_minimum' : 1,
#                #'impassible_percentage' : 100,
#                'cardnality' : 8 
#            }
#        },
#        'run' : {
#            'start': {
#                'x': 0,
#                'y': 0
#            },
#            'finish': {
#                'x': 50,
#                'y': 70
#            },
#            #'pather_module_lib_path' : r"C:\Users\rocker\Documents\Personal\classes\MS State\Spring 2022\AI\git\RADTC\src\lib\radtc\",
#            'pather_module' : 'radtc.pather_astar_prune',
#            'pather_class': 'PatherASP'
#        }
#    }
#
#    runner = Runner( config )
#    runner.run()
#    print( runner.get_report() )

def test_runner_astar_prune_dynamic_edges():
    config = {
        'grid': {
            'generate': {
                'height': 100,
                'width' : 100,
                'edge_max' : 100,
                'edge_minimum' : 1,
                #'impassible_percentage' : 100,
                'cardnality' : 8 
            }
        },
        'run' : {
            'start': {
                'x': 0,
                'y': 0
            },
            'finish': {
                'x': 50,
                'y': 70
            },
            #'pather_module_lib_path' : r"C:\Users\rocker\Documents\Personal\classes\MS State\Spring 2022\AI\git\RADTC\src\lib\radtc\",
            'pather_module' : 'radtc.pather_astar_prune',
            'pather_class': 'PatherASP',
            'step_modifications': {
                'percent':5 
            }
        }
    }

    runner = Runner( config )
    runner.run()
    report = runner.get_report()
    print( report )