from calendar import c
import sys
from radtc.grid import Grid

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

        #based on code referenced here
        #https://www.bensnider.com/dynamically-import-and-instantiate-python-classes.html
        if 'pather_module_lib_path' in config:
            sys.path.append( config[ 'run' ][ 'pather_module_lib_path' ] )
        self.pather_module = __import__( config[ 'run' ][ 'pather_module' ] )
        print( dir( self.pather_module ) )
        print( dir( self.pather_module.pather_bfs ) )
        #self.pather_class = getattr( self.pather_module, config[ 'run' ][ 'pather_class' ] )
        #self.pather_class = globals()[ config[ 'run' ][ 'pather_class' ] ]
        self.pather_class = getattr( self.pather_module.pather_bfs, config[ 'run' ][ 'pather_class' ] )

         

    def run( self ) -> None:
        bfs = self.pather_class( self.grid, self.grid.get_node(  0, 0 ), self.grid.get_node( 1, 3))

        result = { 'path': None }
        count = 0
        while result[ 'path' ] == None and count < self.emergency_break_count:
            count += 1
            result = bfs.step()
            print( result )
            #print( sys.getsizeof( bfs ))

    def report( self ) -> dict:
        report = {}
        return report

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