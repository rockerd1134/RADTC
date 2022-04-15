from calendar import c
import sys
import importlib
from tkinter import N
from radtc.grid import Grid, Node

class Runner( ):
    def __init__( self, config ) -> None:
        self.config_check = self.__class__.check_config( config )
        if not self.config_check[ 'passed' ]:
            raise Exception( f"Config incomplete. {self.config_check[ 'errors' ]}")
        self.config = config
        self.results = {
            'steps': []
        }
        self.grid = Grid.from_config( config[ 'grid' ] )
        self.start = self.grid.get_node( 
            config[ 'run' ][ 'start' ][ 'x'], 
            config[ 'run' ][ 'start' ][ 'y']
        )
        self.finish = self.grid.get_node( 
            config[ 'run' ][ 'finish' ][ 'x'], 
            config[ 'run' ][ 'finish' ][ 'y']
        )
        self.emergency_break_count = config[ 'run' ].get( 
            'emergency_break_count', 
            100000000 #change to something defined
        )

        self.step_modifications = config[ 'run' ].get( 
            'step_modifications',
            False
        )
        if self.step_modifications:
            self.step_modifications_percent = int( config[ 'run' ][ 'step_modifications' ].get( 'percent' ) )

        if 'pather_module_lib_path' in config:
            sys.path.append( config[ 'run' ][ 'pather_module_lib_path' ] )
        self.pather_module = importlib.import_module( config[ 'run' ][ 'pather_module' ] )
        self.pather_class = getattr( self.pather_module, config[ 'run' ][ 'pather_class' ] )

        #for storing our report
        # maybe this should be an object
        self.report = {}
        self.report_steps = config[ 'run' ].get( 'report_steps', False)
        self.report_memory = config[ 'run' ].get( 'report_memory', False)
        self.report_grid_edges = config[ 'run' ].get( 'report_grid_edges', False)
        self.report_grid_nodes = config[ 'run' ].get( 'report_grid_nodes', False)
        #removed because of too much memory taken
        #self.report_modifications = config[ 'run' ].get( 'report_modifications', False)
         

    def run( self ) -> None:
        pather = self.pather_class( 
            self.grid, 
            self.start, 
            self.finish
        )

        #maybe check for in bounds start and finish?

        result = { 'path': None }
        count = 0
        while result[ 'path' ] == None and count < self.emergency_break_count:
            count += 1
            result = pather.step()
            if self.step_modifications:
                self.grid.shuffle_edges( self.step_modifications_percent )
            #print( f"step: {count} ({self.emergency_break_count}) res: {result}" )
            if self.report_steps:
                self.report[ 'steps' ].append( f"step: {count} ({self.emergency_break_count}) res: {result}" )
            #print( sys.getsizeof( bfs ))
        self.report[ 'pather_result' ] = result
        self.report[ 'pather_step_count' ] = count
        self.report[ 'pather_node_expands' ] = Node.expands
        if self.report_grid_edges:
          self.report[ 'edges' ] = self.grid.get_edges()
        if self.report_grid_nodes:
          self.report[ 'nodes' ] = self.grid.get_nodes()
        #removed because of too much memory taken
        #if self.report_modifications:
        #    self.report[ 'modifications' ] = self.grid.modification_history
        Node.expands = 0

        self.report[ 'path_test' ] = self.grid.test_path( result[ 'path' ] )

    def get_report( self ) -> dict:
        return self.report

    @classmethod
    def check_config( cls, config ) -> dict:
        config_check = {
            'errors' : [],
            'passed' : None
        }
        #check for grid configuraiton
        if not 'grid' in config:
            config_check[ 'errors'].append( 'Grid section missing from config.')
            config_check[ 'passed' ] = False
        else:
            if not 'generate' in config[ 'grid' ]:
                config_check[ 'errors'].append( 'Grid.generate section missing from config.')
                config_check[ 'passed' ] = False
            else:
                if not 'height' in config[ 'grid' ][ 'generate' ] or not 'width' in config[ 'grid' ][ 'generate' ]:
                    config_check[ 'errors'].append( 'Grid.generate config section missing height or width.')
                    config_check[ 'passed' ] = False


        #check for run configuration
        if not 'run' in config:
            config_check[ 'errors'].append( 'Run section missing from config.')
            config_check[ 'passed' ] = False
        else:
            if not 'start' in config[ 'run' ]:
                config_check[ 'errors'].append( 'Run section missing start from config.')
                config_check[ 'passed' ] = False
            else:
                if not 'x' in config[ 'run' ][ 'start' ] or not 'y' in config[ 'run' ][ 'start' ]:
                    config_check[ 'errors'].append( 'Run.start section missing x or y from config.')
                    config_check[ 'passed' ] = False
            if not 'finish' in config[ 'run' ]:
                config_check[ 'errors'].append( 'Run section missing finish from config.')
                config_check[ 'passed' ] = False
            else:
                if not 'x' in config[ 'run' ][ 'finish' ] or not 'y' in config[ 'run' ][ 'finish' ]:
                    config_check[ 'errors'].append( 'Run.finish section missing x or y from config.')
                    config_check[ 'passed' ] = False
            if not 'pather_module' in config[ 'run' ]:
                config_check[ 'errors' ].append( 'Run.pather_module section missing from config.')
                config_check[ 'passed' ] = False
            if not 'pather_class' in config[ 'run' ]:
                config_check[ 'errors' ].append( 'Run.pather_class section missing from config.')
                config_check[ 'passed' ] = False

        if config_check[ 'passed' ] == None:
            config_check[ 'passed' ] = True
 
        return config_check