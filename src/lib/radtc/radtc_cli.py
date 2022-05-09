import yaml

class RadTCCLI( ):
    def __init__( self ) -> None:
        pass

    @classmethod
    def print_report( cls, report: dict, **kwargs ) -> None:
        show_path = kwargs.get( 'show_path', True )
        show_search_stats = kwargs.get( 'show_search_stats', True )
        #report_output = str( report )
        report_output = ''
        if show_path:
            report_output += "\n"
            report_output += f"path_report:\n  path:\n"
            if 'edge_path' in report[ 'path_test' ]:
                for path_element in report[ 'path_test' ][ 'edge_path' ]:
                #for path_element in report[ 'pather_result' ][ 'path' ]:
                    report_output += "    = {0}\n".format( str( path_element ) )
            if 'cost' in report[ 'path_test' ]:
                report_output += f"  cost: {report[ 'path_test' ][ 'cost' ]}\n  solved: {report[ 'pather_result' ][ 'solved' ]}\n congruent: {report[ 'path_test' ][ 'congruent' ]}\n"
        if show_search_stats:
            report_output += f"search_stats:\n  step_count: {report[ 'pather_step_count' ]}\n  node_expands: {report[ 'pather_step_count' ]}\n"
        if 'comparison' in report:
            report_output += f"\ncomparison:\n  comparison_class: {report[ 'comparison' ][ 'comparison_class' ]}\n  comparison_path:\n"
            if 'edge_path' in report[ 'comparison' ][ 'path_test' ]:
                for path_element in report[ 'comparison' ][ 'path_test' ][ 'edge_path' ]:
                #for path_element in report[ 'pather_result' ][ 'path' ]:
                    report_output += "    = {0}\n".format( str( path_element ) )
            report_output += f"  comparison_cost: {report[ 'comparison' ][ 'path_test' ][ 'cost' ]}\n  comparison_congruent: {report[ 'comparison' ][ 'path_test' ][ 'congruent' ]}\n"
            report_output += f"  comparison_cost_delta: {abs( int(report[ 'comparison' ][ 'path_test' ][ 'cost' ]) - int( report[ 'path_test' ][ 'cost' ] ))}\n"

        print( report_output )