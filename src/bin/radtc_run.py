#!/bin/env python3
import sys
import argparse
sys.path.append( '../lib')
from radtc.radtc_loader import RadTCLoader

parser = argparse.ArgumentParser( description='RADTC runner' )
parser.add_argument( 
    '--config_file', '-c',
    action='store',
    dest='config_file',
    required=True
)
args = parser.parse_args()

runner = RadTCLoader.from_config_file( config_file= args.config_file)
runner.run()
print( runner.get_report() )

