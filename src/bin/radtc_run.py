#!/bin/env python3
import sys
import argparse
sys.path.append( '../lib')
from radtc.radtc_loader import RadTCLoader
from radtc.radtc_cli import RadTCCLI

parser = argparse.ArgumentParser( description='RADTC runner' )
parser.add_argument( 
    '--config_file', '-c',
    action='store',
    dest='config_file',
    required=True
)
parser.add_argument( 
    '--loop', '-l',
    action='store',
    type=int,
    dest='loop',
    default=1
)
args = parser.parse_args()

for i in range(args.loop):
    print( f'#####  Start Trial {i}  #####\n')
    runner = RadTCLoader.from_config_file( config_file= args.config_file)
    runner.run()
    RadTCCLI.print_report( runner.get_report() )
    print( f'#####  End Trial {i}  #####\n\n')

