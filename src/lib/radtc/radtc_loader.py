import yaml
from radtc.radtc_runner import Runner

class RadTCLoader():
    def __init__(self, config_file: str ) -> None:
        self.runner = self.__class__.from_config_file( config_file )

    @classmethod
    def from_config_file( cls, config_file: str ) -> 'Runner':
        with open( config_file, 'r' ) as conf_f:
            config = yaml.safe_load( conf_f.read() )
            return Runner( config )


