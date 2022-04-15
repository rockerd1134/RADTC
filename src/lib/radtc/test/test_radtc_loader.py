import pytest
import sys
sys.path.append( '../..')
from radtc.radtc_loader import RadTCLoader

def test_runner_loader():
    runner = RadTCLoader.from_config_file( '../examples/astar_prune.yml' )
    runner.run()
    print( runner.get_report() )
