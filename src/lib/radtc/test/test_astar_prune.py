import pytest
import sys
sys.path.append( '../..')
from radtc.radtc_runner import Runner

def test_runner():
    config = {
        'grid': {
            'generate': {
                'height': 10,
                'width' : 10
            }
        },
        'run' : {
            'start': {
                'x': 0,
                'y': 0
            },
            'finish': {
                'x': 5,
                'y': 7
            },
            #'pather_module_lib_path' : r"C:\Users\rocker\Documents\Personal\classes\MS State\Spring 2022\AI\git\RADTC\src\lib\radtc\",
            'pather_module' : 'radtc.pather_astar_prune',
            'pather_class': 'PatherASP'
        }
    }

    runner = Runner( config )
    runner.run()
    print( runner.get_report() )