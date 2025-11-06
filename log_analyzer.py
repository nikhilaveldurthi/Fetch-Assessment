#!/usr/bin/env python3
"""
Log Analysis Expert Tool
This script analyzes log files to identify errors, exceptions, and issues.
Supports various log formats including application logs, PostgreSQL logs, and general system logs.
"""

import re
import sys
from datetime import datetime
from collections import defaultdict
from typing import List, Dict, Tuple


class LogAnalyzer:
    """Expert log analyzer that identifies errors and issues in log files."""
    
    def __init__(self):
        # Common error patterns
        self.error_patterns = [
            (r'(?i)error[:|\s]', 'ERROR'),
            (r'(?i)exception[:|\s]', 'EXCEPTION'),
            (r'(?i)failed[:|\s]', 'FAILED'),
            (r'(?i)fatal[:|\s]', 'FATAL'),
            (r'(?i)critical[:|\s]', 'CRITICAL'),
            (r'(?i)traceback', 'TRACEBACK'),
            (r'(?i)stack trace', 'STACK_TRACE'),
            (r'(?i)segmentation fault', 'SEGFAULT'),
            (r'(?i)out of memory', 'OOM'),
            (r'(?i)connection refused', 'CONNECTION_REFUSED'),
            (r'(?i)timeout', 'TIMEOUT'),
            (r'(?i)permission denied', 'PERMISSION_DENIED'),
            (r'(?i)null pointer', 'NULL_POINTER'),
            (r'(?i)assertion failed', 'ASSERTION_FAILED'),
            (r'(?i)panic[:|\s]', 'PANIC'),
        ]
        
        # PostgreSQL specific error patterns
        self.postgres_patterns = [
            (r'ERROR:\s+(.+)', 'POSTGRES_ERROR'),
            (r'FATAL:\s+(.+)', 'POSTGRES_FATAL'),
            (r'PANIC:\s+(.+)', 'POSTGRES_PANIC'),
            (r'WARNING:\s+(.+)', 'POSTGRES_WARNING'),
            (r'deadlock detected', 'DEADLOCK'),
            (r'duplicate key value', 'DUPLICATE_KEY'),
            (r'foreign key violation', 'FK_VIOLATION'),
            (r'syntax error', 'SYNTAX_ERROR'),
            (r'relation .+ does not exist', 'MISSING_RELATION'),
        ]
        
        # HTTP error codes
        self.http_error_pattern = r'\s(4\d{2}|5\d{2})\s'
        
        self.errors_found = []
        self.error_summary = defaultdict(int)
        
    def analyze_file(self, filepath: str) -> Dict:
        """
        Analyze a log file and return structured error information.
        
        Args:
            filepath: Path to the log file
            
        Returns:
            Dictionary containing error analysis results
        """
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
        except FileNotFoundError:
            return {'error': f'File not found: {filepath}'}
        except Exception as e:
            return {'error': f'Error reading file: {str(e)}'}
        
        self.errors_found = []
        self.error_summary = defaultdict(int)
        
        for line_num, line in enumerate(lines, 1):
            self._analyze_line(line, line_num)
        
        return self._generate_report(filepath, len(lines))
    
    def _analyze_line(self, line: str, line_num: int):
        """Analyze a single line for errors."""
        # Check general error patterns
        for pattern, error_type in self.error_patterns:
            if re.search(pattern, line):
                self.errors_found.append({
                    'line_number': line_num,
                    'error_type': error_type,
                    'content': line.strip(),
                    'severity': self._get_severity(error_type)
                })
                self.error_summary[error_type] += 1
        
        # Check PostgreSQL patterns
        for pattern, error_type in self.postgres_patterns:
            if re.search(pattern, line):
                self.errors_found.append({
                    'line_number': line_num,
                    'error_type': error_type,
                    'content': line.strip(),
                    'severity': self._get_severity(error_type)
                })
                self.error_summary[error_type] += 1
        
        # Check HTTP error codes
        match = re.search(self.http_error_pattern, line)
        if match:
            status_code = match.group(1)
            error_type = f'HTTP_{status_code}'
            self.errors_found.append({
                'line_number': line_num,
                'error_type': error_type,
                'content': line.strip(),
                'severity': 'HIGH' if status_code.startswith('5') else 'MEDIUM'
            })
            self.error_summary[error_type] += 1
    
    def _get_severity(self, error_type: str) -> str:
        """Determine severity level based on error type."""
        critical_types = ['FATAL', 'CRITICAL', 'PANIC', 'POSTGRES_FATAL', 
                         'POSTGRES_PANIC', 'SEGFAULT', 'OOM']
        high_types = ['ERROR', 'EXCEPTION', 'POSTGRES_ERROR', 'FAILED',
                     'DEADLOCK', 'FK_VIOLATION']
        
        if error_type in critical_types:
            return 'CRITICAL'
        elif error_type in high_types:
            return 'HIGH'
        else:
            return 'MEDIUM'
    
    def _generate_report(self, filepath: str, total_lines: int) -> Dict:
        """Generate a comprehensive error report."""
        report = {
            'file': filepath,
            'total_lines': total_lines,
            'total_errors': len(self.errors_found),
            'error_summary': dict(self.error_summary),
            'errors': self.errors_found,
            'analysis_time': datetime.now().isoformat()
        }
        
        # Add severity breakdown
        severity_count = defaultdict(int)
        for error in self.errors_found:
            severity_count[error['severity']] += 1
        report['severity_breakdown'] = dict(severity_count)
        
        return report
    
    def print_report(self, report: Dict):
        """Print a human-readable error report."""
        if 'error' in report:
            print(f"Error: {report['error']}")
            return
        
        print("=" * 80)
        print(f"LOG ANALYSIS REPORT: {report['file']}")
        print("=" * 80)
        print(f"Total Lines Analyzed: {report['total_lines']}")
        print(f"Total Errors Found: {report['total_errors']}")
        print(f"Analysis Time: {report['analysis_time']}")
        print()
        
        if report['total_errors'] == 0:
            print("✓ No errors found in the log file!")
            print("=" * 80)
            return
        
        # Print severity breakdown
        print("SEVERITY BREAKDOWN:")
        print("-" * 40)
        for severity, count in sorted(report['severity_breakdown'].items()):
            print(f"  {severity}: {count}")
        print()
        
        # Print error summary
        print("ERROR TYPE SUMMARY:")
        print("-" * 40)
        for error_type, count in sorted(report['error_summary'].items(), 
                                       key=lambda x: x[1], reverse=True):
            print(f"  {error_type}: {count}")
        print()
        
        # Print top 10 critical errors
        critical_errors = [e for e in report['errors'] if e['severity'] == 'CRITICAL']
        if critical_errors:
            print("TOP CRITICAL ERRORS:")
            print("-" * 40)
            for error in critical_errors[:10]:
                print(f"  Line {error['line_number']} [{error['error_type']}]:")
                print(f"    {error['content'][:120]}...")
                print()
        
        # Print high priority errors
        high_errors = [e for e in report['errors'] if e['severity'] == 'HIGH']
        if high_errors:
            print("TOP HIGH PRIORITY ERRORS:")
            print("-" * 40)
            for error in high_errors[:10]:
                print(f"  Line {error['line_number']} [{error['error_type']}]:")
                print(f"    {error['content'][:120]}...")
                print()
        
        print("=" * 80)
        
        # Provide diagnosis
        self._provide_diagnosis(report)
    
    def _provide_diagnosis(self, report: Dict):
        """Provide expert diagnosis based on errors found."""
        print("EXPERT DIAGNOSIS:")
        print("-" * 40)
        
        error_summary = report['error_summary']
        
        if 'POSTGRES_ERROR' in error_summary or 'POSTGRES_FATAL' in error_summary:
            print("• Database errors detected - Check PostgreSQL connection and queries")
        
        if 'DEADLOCK' in error_summary:
            print("• Deadlocks detected - Review transaction isolation levels and query order")
        
        if 'FK_VIOLATION' in error_summary or 'DUPLICATE_KEY' in error_summary:
            print("• Data integrity errors - Validate input data and constraints")
        
        if 'CONNECTION_REFUSED' in error_summary or 'TIMEOUT' in error_summary:
            print("• Network/connectivity issues - Check service availability and network config")
        
        if 'OOM' in error_summary:
            print("• Out of memory errors - Increase memory allocation or optimize queries")
        
        if 'PERMISSION_DENIED' in error_summary:
            print("• Permission issues - Review file/database access permissions")
        
        if any(k.startswith('HTTP_5') for k in error_summary.keys()):
            print("• Server errors (5xx) - Check application server logs and health")
        
        if any(k.startswith('HTTP_4') for k in error_summary.keys()):
            print("• Client errors (4xx) - Validate request parameters and authentication")
        
        if report['total_errors'] > 100:
            print(f"• HIGH ERROR VOLUME ({report['total_errors']} errors) - Immediate attention required")
        
        print("=" * 80)


def main():
    """Main entry point for the log analyzer."""
    if len(sys.argv) < 2:
        print("Usage: python log_analyzer.py <log_file_path>")
        print("Example: python log_analyzer.py /var/log/application.log")
        sys.exit(1)
    
    log_file = sys.argv[1]
    analyzer = LogAnalyzer()
    
    print(f"Analyzing log file: {log_file}")
    print()
    
    report = analyzer.analyze_file(log_file)
    analyzer.print_report(report)


if __name__ == '__main__':
    main()
