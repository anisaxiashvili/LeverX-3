"""CLI controller for handling command line operations."""
import sys
import time
import logging
from typing import Dict, Any, List
from tabulate import tabulate
from ..config.database_config import DatabaseConfig
from ..config.app_config import AppConfig
from ..database.connection_manager import ConnectionManager
from ..database.schema_manager import SchemaManager
from ..database.query_optimizer import QueryOptimizer
from ..data.repositories.student_repository import StudentRepository
from ..data.repositories.room_repository import RoomRepository
from ..data.repositories.analytics_repository import AnalyticsRepository
from ..services.data_import_service import DataImportService
from ..services.analytics_service import AnalyticsService
from ..services.database_optimization_service import DatabaseOptimizationService
from ..utils.logging_config import setup_logging
from ..exceptions.custom_exceptions import *
from .argument_parser import ArgumentParser
from .cli_config import CLIConfig


class CLIController:
    """Main CLI controller for the application."""
    
    def __init__(self):
        self.arg_parser = ArgumentParser()
        self.cli_config = CLIConfig()
        self.logger = None
        self.start_time = None
    
    def run(self):
        """Main entry point for CLI application."""
        try:
            args = self.arg_parser.parse_args()
            
            self.logger = setup_logging(
                level=args.log_level,
                log_file=args.log_file
            )
            
            self.start_time = time.time()

            if args.command == 'import':
                self._handle_import_command(args)
            elif args.command == 'analytics':
                self._handle_analytics_command(args)
            elif args.command == 'optimize':
                self._handle_optimization_command(args)
            elif args.command == 'database':
                self._handle_database_command(args)
            else:
                self.arg_parser.parser.print_help()
                
        except KeyboardInterrupt:
            self._print_error("Operation cancelled by user")
            sys.exit(1)
        except Exception as e:
            self._print_error(f"Application error: {e}")
            if self.logger:
                self.logger.exception("Unhandled exception")
            sys.exit(1)
        finally:
            if self.start_time and self.cli_config.show_timing:
                elapsed = time.time() - self.start_time
                self._print_info(f"Total execution time: {elapsed:.2f} seconds")
    
    def _handle_import_command(self, args):
        """Handle data import command."""
        try:
            self._print_header("Data Import")

            connection_manager, services = self._initialize_services()

            results = services['import_service'].import_data(
                students_file=args.students,
                rooms_file=args.rooms,
                file_format=args.format
            )

            self._print_success("Data import completed successfully!")
            self._print_results_table([
                ["Rooms imported", results['rooms_imported']],
                ["Students imported", results['students_imported']],
                ["Total records", results['total_records']]
            ], headers=["Metric", "Count"])
            
        except Exception as e:
            self._print_error(f"Import failed: {e}")
            raise
    
    def _handle_analytics_command(self, args):
        """Handle analytics command."""
        try:
            self._print_header("Analytics")

            connection_manager, services = self._initialize_services()
            analytics_service = services['analytics_service']
            
            if args.report:
                self._generate_full_report(analytics_service)
            else:
                if args.room_counts:
                    self._show_room_counts(analytics_service)
                
                if args.youngest_rooms:
                    self._show_youngest_rooms(analytics_service, args.youngest_rooms)
                
                if args.age_gaps:
                    self._show_age_gaps(analytics_service, args.age_gaps)
                
                if args.mixed_gender:
                    self._show_mixed_gender_rooms(analytics_service)
                    
        except Exception as e:
            self._print_error(f"Analytics failed: {e}")
            raise
    
    def _handle_optimization_command(self, args):
        """Handle optimization command."""
        try:
            self._print_header("Database Optimization")

            connection_manager, services = self._initialize_services()
            opt_service = services['optimization_service']
            
            if args.analyze:
                self._show_performance_analysis(opt_service)
            
            if args.recommendations:
                self._show_optimization_recommendations(opt_service)
                
        except Exception as e:
            self._print_error(f"Optimization analysis failed: {e}")
            raise
    
    def _handle_database_command(self, args):
        """Handle database management command."""
        try:
            self._print_header("Database Management")

            db_config = DatabaseConfig.from_env()
            connection_manager = ConnectionManager(db_config)
            schema_manager = SchemaManager(connection_manager)
            
            if args.init:
                self._print_info("Initializing database schema...")
                schema_manager.create_database()
                schema_manager.create_tables()
                schema_manager.create_indexes()
                self._print_success("Database schema initialized successfully!")
            
            if args.drop:
                self._print_warning("Dropping all tables...")
                schema_manager.drop_tables()
                self._print_success("All tables dropped successfully!")
            
            if args.status:
                self._show_database_status(schema_manager)
                
        except Exception as e:
            self._print_error(f"Database operation failed: {e}")
            raise
    
    def _initialize_services(self) -> tuple:
        db_config = DatabaseConfig.from_env()
        connection_manager = ConnectionManager(db_config)

        if not connection_manager.test_connection():
            raise DatabaseConnectionError("Cannot connect to database")

        schema_manager = SchemaManager(connection_manager)
        query_optimizer = QueryOptimizer(connection_manager)
        
        student_repository = StudentRepository(connection_manager)
        room_repository = RoomRepository(connection_manager)
        analytics_repository = AnalyticsRepository(connection_manager)

        import_service = DataImportService(
            schema_manager, student_repository, room_repository
        )
        analytics_service = AnalyticsService(analytics_repository, query_optimizer)
        optimization_service = DatabaseOptimizationService(query_optimizer)
        
        services = {
            'import_service': import_service,
            'analytics_service': analytics_service,
            'optimization_service': optimization_service
        }
        
        return connection_manager, services
    
    def _generate_full_report(self, analytics_service: AnalyticsService):
        """Generate and display full analytics report."""
        self._print_info("Generating comprehensive analytics report...")
        
        report = analytics_service.generate_analytics_report()

        self._show_room_counts_data(report['room_student_counts'])
        self._show_youngest_rooms_data(report['youngest_rooms'])
        self._show_age_gaps_data(report['rooms_with_age_gaps'])
        self._show_mixed_gender_rooms_data(report['mixed_gender_rooms'])

        self._print_header("Summary")
        summary = report['summary']
        self._print_results_table([
            ["Total rooms analyzed", summary['total_rooms_analyzed']],
            ["Rooms with students", summary['rooms_with_students']],
            ["Mixed gender rooms", summary['mixed_gender_room_count']]
        ], headers=["Metric", "Count"])
    
    def _show_room_counts(self, analytics_service: AnalyticsService):
        """Show room student counts."""
        data = analytics_service.get_room_student_counts()
        self._show_room_counts_data(data)
    
    def _show_room_counts_data(self, data: List[Dict[str, Any]]):
        """Display room counts data."""
        self._print_header("Room Student Counts")
        if data:
            table_data = [[r['room_name'], r['student_count']] for r in data]
            self._print_results_table(table_data, headers=["Room Name", "Student Count"])
        else:
            self._print_warning("No room data found")
    
    def _show_youngest_rooms(self, analytics_service: AnalyticsService, limit: int):
        """Show youngest rooms."""
        data = analytics_service.get_youngest_rooms(limit)
        self._show_youngest_rooms_data(data)
    
    def _show_youngest_rooms_data(self, data: List[Dict[str, Any]]):
        """Display youngest rooms data."""
        self._print_header("Top Rooms with Smallest Average Age")
        if data:
            table_data = [
                [r['room_name'], f"{r['average_age']:.1f}", r['student_count']]
                for r in data
            ]
            self._print_results_table(table_data, 
                                    headers=["Room Name", "Average Age", "Student Count"])
        else:
            self._print_warning("No youngest rooms data found")
    
    def _show_age_gaps(self, analytics_service: AnalyticsService, limit: int):
        """Show rooms with largest age gaps."""
        data = analytics_service.get_rooms_with_largest_age_gaps(limit)
        self._show_age_gaps_data(data)
    
    def _show_age_gaps_data(self, data: List[Dict[str, Any]]):
        """Display age gaps data."""
        self._print_header("Top Rooms with Largest Age Differences")
        if data:
            table_data = [
                [r['room_name'], r['age_difference'], r['min_age'], r['max_age'], r['student_count']]
                for r in data
            ]
            self._print_results_table(table_data, 
                                    headers=["Room Name", "Age Diff", "Min Age", "Max Age", "Students"])
        else:
            self._print_warning("No age gap data found")
    
    def _show_mixed_gender_rooms(self, analytics_service: AnalyticsService):
        """Show mixed gender rooms."""
        data = analytics_service.get_mixed_gender_rooms()
        self._show_mixed_gender_rooms_data(data)
    
    def _show_mixed_gender_rooms_data(self, data: List[Dict[str, Any]]):
        """Display mixed gender rooms data."""
        self._print_header("Mixed Gender Rooms")
        if data:
            table_data = [
                [r['room_name'], r['male_count'], r['female_count'], r['total_students']]
                for r in data
            ]
            self._print_results_table(table_data, 
                                    headers=["Room Name", "Male", "Female", "Total"])
        else:
            self._print_warning("No mixed gender rooms found")
    
    def _show_performance_analysis(self, opt_service: DatabaseOptimizationService):
        """Show query performance analysis."""
        self._print_header("Query Performance Analysis")
        
        analysis = opt_service.analyze_query_performance()
        
        if 'error' in analysis:
            self._print_error(f"Analysis failed: {analysis['error']}")
            return

        self._print_subheader("Table Statistics")
        table_stats = analysis.get('table_statistics', [])
        if table_stats:
            table_data = [
                [t['table_name'], f"{t['table_size_mb']:.2f}", f"{t['data_size_mb']:.2f}", 
                 f"{t['index_size_mb']:.2f}", t['table_rows']]
                for t in table_stats
            ]
            self._print_results_table(table_data, 
                                    headers=["Table", "Total MB", "Data MB", "Index MB", "Rows"])

        self._print_subheader("Query Analysis Summary")
        query_analyses = analysis.get('query_analyses', {})
        for query_name, query_analysis in query_analyses.items():
            suggestions = query_analysis.get('optimization_suggestions', [])
            self._print_info(f"{query_name}:")
            for suggestion in suggestions[:3]: 
                self._print_text(f"  • {suggestion}")
    
    def _show_optimization_recommendations(self, opt_service: DatabaseOptimizationService):
        """Show optimization recommendations."""
        self._print_header("Optimization Recommendations")
        
        recommendations = opt_service.get_optimization_recommendations()
        
        implemented = [r for r in recommendations if r.startswith('✓')]
        suggested = [r for r in recommendations if r.startswith('•')]
        
        if implemented:
            self._print_subheader("Already Implemented")
            for rec in implemented:
                self._print_success(rec)
        
        if suggested:
            self._print_subheader("Additional Recommendations")
            for rec in suggested:
                self._print_info(rec)
    
    def _show_database_status(self, schema_manager: SchemaManager):
        """Show database status."""
        self._print_header("Database Status")

        tables = ['rooms', 'students']
        status_data = []
        
        for table in tables:
            exists = schema_manager.table_exists(table)
            status = "✓ EXISTS" if exists else "✗ MISSING"
            status_data.append([table, status])
        
        self._print_results_table(status_data, headers=["Table", "Status"])

        table_info = schema_manager.get_table_info()
        if table_info:
            self._print_subheader("Table Information")
            info_data = [
                [t['table_name'], f"{t['table_size_mb']:.2f}", t['table_rows']]
                for t in table_info
            ]
            self._print_results_table(info_data, headers=["Table", "Size (MB)", "Rows"])
    
    def _print_results_table(self, data: List[List], headers: List[str]):
        """Print results as formatted table."""
        if not data:
            self._print_warning("No data to display")
            return

        if self.cli_config.truncate_long_text:
            processed_data = []
            for row in data:
                processed_row = []
                for cell in row:
                    cell_str = str(cell)
                    if len(cell_str) > self.cli_config.max_text_length:
                        cell_str = cell_str[:self.cli_config.max_text_length-3] + "..."
                    processed_row.append(cell_str)
                processed_data.append(processed_row)
            data = processed_data

        if len(data) > self.cli_config.max_display_rows:
            displayed_data = data[:self.cli_config.max_display_rows]
            print(tabulate(displayed_data, headers=headers, tablefmt=self.cli_config.table_format))
            self._print_warning(f"Showing first {self.cli_config.max_display_rows} of {len(data)} rows")
        else:
            print(tabulate(data, headers=headers, tablefmt=self.cli_config.table_format))
    
    def _print_header(self, text: str):
        """Print section header."""
        if self.cli_config.use_colors:
            print(f"\n{self.cli_config.header_color}{'='*60}")
            print(f"{text.center(60)}")
            print(f"{'='*60}{self.cli_config.reset_color}")
        else:
            print(f"\n{'='*60}")
            print(f"{text.center(60)}")
            print(f"{'='*60}")
    
    def _print_subheader(self, text: str):
        """Print subsection header."""
        if self.cli_config.use_colors:
            print(f"\n{self.cli_config.header_color}{text}:{self.cli_config.reset_color}")
            print(f"{'-'*len(text)}")
        else:
            print(f"\n{text}:")
            print(f"{'-'*len(text)}")
    
    def _print_success(self, text: str):
        """Print success message."""
        if self.cli_config.use_colors:
            print(f"{self.cli_config.success_color}✓ {text}{self.cli_config.reset_color}")
        else:
            print(f"✓ {text}")
    
    def _print_info(self, text: str):
        """Print info message."""
        if self.cli_config.use_colors:
            print(f"{self.cli_config.header_color}ℹ {text}{self.cli_config.reset_color}")
        else:
            print(f"ℹ {text}")
    
    def _print_warning(self, text: str):
        """Print warning message."""
        if self.cli_config.use_colors:
            print(f"{self.cli_config.warning_color}⚠ {text}{self.cli_config.reset_color}")
        else:
            print(f"⚠ {text}")
    
    def _print_error(self, text: str):
        """Print error message."""
        if self.cli_config.use_colors:
            print(f"{self.cli_config.error_color}✗ {text}{self.cli_config.reset_color}", file=sys.stderr)
        else:
            print(f"✗ {text}", file=sys.stderr)
    
    def _print_text(self, text: str):
        """Print plain text."""
        print(text)
