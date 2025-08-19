import sys
import time
import logging
from typing import Dict, Any, List, Callable
from tabulate import tabulate
from ..config.db_config import DbConfig
from ..config.app_config import AppConfig
from ..database.conn_manager import ConnManager
from ..database.schema_mgr import SchemaMgr
from ..database.optimizer import Optimizer
from ..data.repositories.student_repo import StudentRepo
from ..data.repositories.room_repo import RoomRepo
from ..data.repositories.analytics_repo import AnalyticsRepo
from ..services.import_svc import ImportSvc
from ..services.analytics_svc import AnalyticsSvc
from ..services.opt_svc import OptSvc
from ..utils.logging_config import setup_logging
from ..exceptions.exceptions import *
from ..constants import Commands, DbOps, OptOps
from .arg_parser import ArgParser
from .config import Config


class Controller: 
    
    def __init__(self):
        self.arg_parser = ArgParser()
        self.config = Config() 
        self.logger = None
        self.start_time = None
        
        self.cmd_handlers: Dict[str, Callable] = {  
            Commands.IMPORT: self._handle_import_cmd,      
            Commands.ANALYTICS: self._handle_analytics_cmd, 
            Commands.OPTIMIZE: self._handle_opt_cmd,       
            Commands.DATABASE: self._handle_db_cmd         
        }
    
    def run(self):
        try:
            args = self.arg_parser.parse_args()
            
            self.logger = setup_logging(
                level=args.log_level,
                log_file=args.log_file
            )
            
            self.start_time = time.time()
            handler = self.cmd_handlers.get(args.command)
            if handler:
                handler(args)
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
            if self.start_time and self.config.show_timing:
                elapsed = time.time() - self.start_time
                self._print_info(f"Total execution time: {elapsed:.2f} seconds")
    
    def _handle_import_cmd(self, args): 
        try:
            self._print_header("Data Import")
            
            conn_manager, services = self._init_services()  
            
            results = services['import_svc'].import_data(
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
    
    def _handle_analytics_cmd(self, args): 
        try:
            self._print_header("Analytics")
            
            conn_manager, services = self._init_services()
            analytics_svc = services['analytics_svc']
            
            analytics_ops = {
                'report': lambda: self._gen_full_report(analytics_svc), 
                'room_counts': lambda: self._show_room_counts(analytics_svc),
                'youngest_rooms': lambda: self._show_youngest_rooms(analytics_svc, args.youngest_rooms),
                'age_gaps': lambda: self._show_age_gaps(analytics_svc, args.age_gaps),
                'mixed_gender': lambda: self._show_mixed_gender_rooms(analytics_svc)
            }
            
            if args.report:
                analytics_ops['report']()
            else:
                if args.room_counts:
                    analytics_ops['room_counts']()
                if args.youngest_rooms:
                    analytics_ops['youngest_rooms']()
                if args.age_gaps:
                    analytics_ops['age_gaps']()
                if args.mixed_gender:
                    analytics_ops['mixed_gender']()
                    
        except Exception as e:
            self._print_error(f"Analytics failed: {e}")
            raise
    
    def _handle_opt_cmd(self, args): 
        try:
            self._print_header("Database Optimization")

            conn_manager, services = self._init_services()
            opt_svc = services['opt_svc']
            
            opt_ops = {
                OptOps.ANALYZE: lambda: self._show_perf_analysis(opt_svc),  # Brief: _show_performance_analysis → _show_perf_analysis
                OptOps.RECOMMENDATIONS: lambda: self._show_opt_recommendations(opt_svc)  # Brief: _show_optimization_recommendations → _show_opt_recommendations
            }
            
            if args.analyze and OptOps.ANALYZE in opt_ops:
                opt_ops[OptOps.ANALYZE]()
            
            if args.recommendations and OptOps.RECOMMENDATIONS in opt_ops:
                opt_ops[OptOps.RECOMMENDATIONS]()
                
        except Exception as e:
            self._print_error(f"Optimization analysis failed: {e}")
            raise
    
    def _handle_db_cmd(self, args): 
        try:
            self._print_header("Database Management")
            
            db_config = DbConfig.from_env()
            conn_manager = ConnManager(db_config)
            schema_mgr = SchemaMgr(conn_manager)
            
            db_ops = {
                DbOps.INIT: lambda: self._init_db_schema(schema_mgr),  
                DbOps.DROP: lambda: self._drop_db_tables(schema_mgr), 
                DbOps.STATUS: lambda: self._show_db_status(schema_mgr) 
            }
            
            if args.init and DbOps.INIT in db_ops:
                db_ops[DbOps.INIT]()
            
            if args.drop and DbOps.DROP in db_ops:
                db_ops[DbOps.DROP]()
            
            if args.status and DbOps.STATUS in db_ops:
                db_ops[DbOps.STATUS]()
                
        except Exception as e:
            self._print_error(f"Database operation failed: {e}")
            raise
    
    def _init_services(self) -> tuple: 
        db_config = DbConfig.from_env()
        conn_manager = ConnManager(db_config)
        
        if not conn_manager.test_conn():
            raise DbConnError("Cannot connect to database")
        
        schema_mgr = SchemaMgr(conn_manager)
        optimizer = Optimizer(conn_manager)
        
        student_repo = StudentRepo(conn_manager)
        room_repo = RoomRepo(conn_manager)
        analytics_repo = AnalyticsRepo(conn_manager)
        
        import_svc = ImportSvc(
            schema_mgr, student_repo, room_repo
        )
        analytics_svc = AnalyticsSvc(analytics_repo, optimizer)
        opt_svc = OptSvc(optimizer)
        
        services = {
            'import_svc': import_svc,
            'analytics_svc': analytics_svc,
            'opt_svc': opt_svc
        }
        
        return conn_manager, services
    
    def _gen_full_report(self, analytics_svc: 'AnalyticsSvc'):
        self._print_info("Generating comprehensive analytics report...")
        
        report = analytics_svc.gen_analytics_report()
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
    
    def _show_room_counts(self, analytics_svc: 'AnalyticsSvc'):
        """Show room student counts."""
        data = analytics_svc.get_room_student_counts()
        self._show_room_counts_data(data)
    
    def _show_room_counts_data(self, data: List[Dict[str, Any]]):
        """Display room counts data."""
        self._print_header("Room Student Counts")
        if data:
            table_data = [[r['room_name'], r['student_count']] for r in data]
            self._print_results_table(table_data, headers=["Room Name", "Student Count"])
        else:
            self._print_warning("No room data found")
    
    def _show_youngest_rooms(self, analytics_svc: 'AnalyticsSvc', limit: int):
        data = analytics_svc.get_youngest_rooms(limit)
        self._show_youngest_rooms_data(data)
    
    def _show_youngest_rooms_data(self, data: List[Dict[str, Any]]):
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
    
    def _show_age_gaps(self, analytics_svc: 'AnalyticsSvc', limit: int):
        data = analytics_svc.get_rooms_with_largest_age_gaps(limit)
        self._show_age_gaps_data(data)
    
    def _show_age_gaps_data(self, data: List[Dict[str, Any]]):
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
    
    def _show_mixed_gender_rooms(self, analytics_svc: 'AnalyticsSvc'):
        data = analytics_svc.get_mixed_gender_rooms()
        self._show_mixed_gender_rooms_data(data)
    
    def _show_mixed_gender_rooms_data(self, data: List[Dict[str, Any]]):
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
    
    def _show_perf_analysis(self, opt_svc: 'OptSvc'):
        self._print_header("Query Performance Analysis")
        
        analysis = opt_svc.analyze_query_perf() 
        
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
    
    def _show_opt_recommendations(self, opt_svc: 'OptSvc'):  
        self._print_header("Optimization Recommendations")
        
        recommendations = opt_svc.get_opt_recommendations()  
        
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
    
    def _init_db_schema(self, schema_mgr: 'SchemaMgr'): 
        self._print_info("Initializing database schema...")
        schema_mgr.create_db()
        schema_mgr.create_tables()
        schema_mgr.create_indexes()
        self._print_success("Database schema initialized successfully!")
    
    def _drop_db_tables(self, schema_mgr: 'SchemaMgr'): 
        self._print_warning("Dropping all tables...")
        schema_mgr.drop_tables()
        self._print_success("All tables dropped successfully!")
    
    def _show_db_status(self, schema_mgr: 'SchemaMgr'):  
        self._print_header("Database Status")
        from ..constants import Tables
        tables = [Tables.ROOMS, Tables.STUDENTS]
        status_data = []
        
        for table in tables:
            exists = schema_mgr.table_exists(table)
            status = "EXISTS" if exists else "MISSING"
            status_data.append([table, status])
        
        self._print_results_table(status_data, headers=["Table", "Status"])
        
        table_info = schema_mgr.get_table_info()
        if table_info:
            self._print_subheader("Table Information")
            info_data = [
                [t['table_name'], f"{t['table_size_mb']:.2f}", t['table_rows']]
                for t in table_info
            ]
            self._print_results_table(info_data, headers=["Table", "Size (MB)", "Rows"])
    
    def _print_results_table(self, data: List[List], headers: List[str]):
        if not data:
            self._print_warning("No data to display")
            return
        
        if self.config.truncate_long_text:
            processed_data = []
            for row in data:
                processed_row = []
                for cell in row:
                    cell_str = str(cell)
                    if len(cell_str) > self.config.max_text_length:
                        cell_str = cell_str[:self.config.max_text_length-3] + "..."
                    processed_row.append(cell_str)
                processed_data.append(processed_row)
            data = processed_data
        
        if len(data) > self.config.max_display_rows:
            displayed_data = data[:self.config.max_display_rows]
            print(tabulate(displayed_data, headers=headers, tablefmt=self.config.table_format))
            self._print_warning(f"Showing first {self.config.max_display_rows} of {len(data)} rows")
        else:
            print(tabulate(data, headers=headers, tablefmt=self.config.table_format))
    
    def _print_header(self, text: str):
        if self.config.use_colors:
            print(f"\n{self.config.header_color}{'='*60}")
            print(f"{text.center(60)}")
            print(f"{'='*60}{self.config.reset_color}")
        else:
            print(f"\n{'='*60}")
            print(f"{text.center(60)}")
            print(f"{'='*60}")
    
    def _print_subheader(self, text: str):
        if self.config.use_colors:
            print(f"\n{self.config.header_color}{text}:{self.config.reset_color}")
            print(f"{'-'*len(text)}")
        else:
            print(f"\n{text}:")
            print(f"{'-'*len(text)}")
    
    def _print_success(self, text: str):
        if self.config.use_colors:
            print(f"{self.config.success_color} {text}{self.config.reset_color}")
        else:
            print(f" {text}")
    
    def _print_info(self, text: str):
        if self.config.use_colors:
            print(f"{self.config.header_color} {text}{self.config.reset_color}")
        else:
            print(f" {text}")
    
    def _print_warning(self, text: str):
        if self.config.use_colors:
            print(f"{self.config.warning_color} {text}{self.config.reset_color}")
        else:
            print(f" {text}")
    
    def _print_error(self, text: str):
        if self.config.use_colors:
            print(f"{self.config.error_color} {text}{self.config.reset_color}", file=sys.stderr)
        else:
            print(f" {text}", file=sys.stderr)
    
    def _print_text(self, text: str):
        print(text)