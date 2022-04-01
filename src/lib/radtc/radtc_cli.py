import yaml

class RadtcCLI( ):
    def __init__( self ) -> None:
        pass

    @classmethod
    def print_report( cls, report: dict ) -> None:
        print( yaml.safe_dump( report ) )