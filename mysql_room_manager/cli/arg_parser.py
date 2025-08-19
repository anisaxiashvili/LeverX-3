"""Command line argument parser."""
import argparse
from ..constants import Commands, AnalyticsOpts, DbOps, OptOps


class ArgParser:
    
    def __init__(self):
        self.parser = argparse.ArgumentParser(
            description="MySQL Student Room Manager - Analytics and Data Import Tool",
            formatter_class=argparse.RawDescriptionHelpFormatter
        )
        self._setup_args()
    def _setup_args(self):
        subparsers = self.parser.add_subparsers(dest='command', help='Available commands')
        
        import_parser = subparsers.add_parser(Commands.IMPORT, help='Import data from JSON files')
        import_parser.add_argument('--students', required=True, 
                                 help='Path to students JSON file')
        import_parser.add_argument('--rooms', required=True,
                                 help='Path to rooms JSON file')
        import_parser.add_argument('--format', default='json',
                                 help='Data file format (default: json)')
        
        analytics_parser = subparsers.add_parser(Commands.ANALYTICS, help='Run analytics queries')
        analytics_parser.add_argument('--report', action='store_true',
                                    help='Generate full analytics report')
        analytics_parser.add_argument('--room-counts', action='store_true',
                                    help='Show room student counts')
        analytics_parser.add_argument('--youngest-rooms', type=int, metavar='N', default=5,
                                    help='Show top N youngest rooms (default: 5)')
        analytics_parser.add_argument('--age-gaps', type=int, metavar='N', default=5,
                                    help='Show top N rooms with largest age gaps (default: 5)')
        analytics_parser.add_argument('--mixed-gender', action='store_true',
                                    help='Show mixed gender rooms')
        
        opt_parser = subparsers.add_parser(Commands.OPTIMIZE, help='Database optimization analysis')
        opt_parser.add_argument('--analyze', action='store_true',
                               help='Analyze query performance')
        opt_parser.add_argument('--recommendations', action='store_true',
                               help='Show optimization recommendations')
        
        db_parser = subparsers.add_parser(Commands.DATABASE, help='Database management')
        db_parser.add_argument('--init', action='store_true',
                              help='Initialize database schema')
        db_parser.add_argument('--drop', action='store_true',
                              help='Drop all tables')
        db_parser.add_argument('--status', action='store_true',
                              help='Show database status')
        
        self.parser.add_argument('--config', help='Configuration file path')
        self.parser.add_argument('--log-level', default='INFO',
                               choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
                               help='Logging level (default: INFO)')
        self.parser.add_argument('--log-file', help='Log file path')
    
    def parse_args(self) -> argparse.Namespace:
        return self.parser.parse_args()