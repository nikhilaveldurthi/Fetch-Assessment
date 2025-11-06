# Log Analyzer - Expert Error Detection Tool

## Overview
The Log Analyzer is a powerful Python-based tool designed to analyze log files and identify errors, exceptions, and critical issues. It's particularly useful for analyzing application logs, PostgreSQL database logs, and general system logs.

## Features

### Comprehensive Error Detection
- **Application Errors**: Detects general errors, exceptions, failures, and critical issues
- **Database Errors**: Specialized detection for PostgreSQL errors including:
  - Duplicate key violations
  - Foreign key violations
  - Deadlocks
  - Syntax errors
  - Missing relations/tables
  - Connection failures
- **HTTP Errors**: Identifies 4xx and 5xx HTTP status codes
- **System Errors**: Detects memory issues, permission problems, timeouts, and segmentation faults

### Severity Classification
Errors are automatically classified into three severity levels:
- **CRITICAL**: Fatal errors, panics, out-of-memory, segmentation faults
- **HIGH**: General errors, exceptions, database errors, deadlocks
- **MEDIUM**: Warnings, timeouts, connection issues

### Expert Diagnosis
The tool provides expert diagnosis based on the types of errors found, including:
- Database connectivity and query issues
- Transaction isolation and deadlock problems
- Data integrity violations
- Network and service availability issues
- Memory allocation problems
- Permission and access control issues
- HTTP client and server errors

## Installation

No external dependencies required! The tool uses only Python standard library.

Requirements:
- Python 3.6 or higher

## Usage

### Basic Usage
```bash
python3 log_analyzer.py <log_file_path>
```

### Examples

Analyze an application log:
```bash
python3 log_analyzer.py /var/log/application.log
```

Analyze a PostgreSQL log:
```bash
python3 log_analyzer.py /var/log/postgresql/postgresql-14-main.log
```

Analyze the sample logs provided:
```bash
python3 log_analyzer.py sample_logs/application.log
python3 log_analyzer.py sample_logs/postgresql.log
```

## Output

The tool generates a comprehensive report including:

1. **Summary Statistics**
   - Total lines analyzed
   - Total errors found
   - Analysis timestamp

2. **Severity Breakdown**
   - Count of errors by severity level (CRITICAL, HIGH, MEDIUM)

3. **Error Type Summary**
   - Count of each type of error detected

4. **Top Critical Errors**
   - Detailed listing of the most critical issues with line numbers

5. **Top High Priority Errors**
   - Detailed listing of high-priority issues

6. **Expert Diagnosis**
   - Actionable insights and recommendations based on detected errors

## Sample Output

```
================================================================================
LOG ANALYSIS REPORT: sample_logs/application.log
================================================================================
Total Lines Analyzed: 52
Total Errors Found: 45
Analysis Time: 2025-11-06T17:45:23.336527

SEVERITY BREAKDOWN:
----------------------------------------
  CRITICAL: 5
  HIGH: 29
  MEDIUM: 11

ERROR TYPE SUMMARY:
----------------------------------------
  ERROR: 19
  FAILED: 3
  POSTGRES_ERROR: 2
  ...

TOP CRITICAL ERRORS:
----------------------------------------
  Line 22 [CRITICAL]:
    2025-02-18 10:25:30 CRITICAL Out of memory: Cannot allocate 2GB...

EXPERT DIAGNOSIS:
----------------------------------------
• Database errors detected - Check PostgreSQL connection and queries
• Deadlocks detected - Review transaction isolation levels and query order
• Out of memory errors - Increase memory allocation or optimize queries
================================================================================
```

## Error Types Detected

### Application Errors
- ERROR, EXCEPTION, FAILED
- FATAL, CRITICAL
- TRACEBACK, STACK_TRACE
- SEGFAULT, NULL_POINTER
- ASSERTION_FAILED

### Database Errors (PostgreSQL)
- POSTGRES_ERROR, POSTGRES_FATAL, POSTGRES_PANIC
- POSTGRES_WARNING
- DEADLOCK
- DUPLICATE_KEY
- FK_VIOLATION (Foreign Key)
- SYNTAX_ERROR
- MISSING_RELATION

### System Errors
- OOM (Out of Memory)
- CONNECTION_REFUSED
- TIMEOUT
- PERMISSION_DENIED
- PANIC

### HTTP Errors
- HTTP_4XX (Client errors: 400-499)
- HTTP_5XX (Server errors: 500-599)

## Integration with Fetch Assessment Project

This log analyzer complements the Fetch Assessment data analytics project by:
1. Helping identify data quality issues in PostgreSQL logs
2. Detecting errors in receipt processing and user management systems
3. Monitoring application health and performance
4. Providing insights for stakeholder communication

## Sample Logs

The `sample_logs/` directory contains example log files to demonstrate the tool:
- `application.log` - Sample application log with various error types
- `postgresql.log` - Sample PostgreSQL database log

## Extending the Tool

To add custom error patterns, modify the `error_patterns` or `postgres_patterns` lists in the `LogAnalyzer` class:

```python
self.error_patterns.append(
    (r'your_custom_pattern', 'CUSTOM_ERROR_TYPE')
)
```

## Use Cases

1. **Post-Deployment Monitoring**: Quickly scan logs after deployment to identify issues
2. **Data Quality Analysis**: Detect database integrity problems
3. **Performance Troubleshooting**: Identify timeout and memory issues
4. **Security Auditing**: Find permission and authentication failures
5. **Incident Response**: Rapid error identification during outages

## Best Practices

1. Run the analyzer regularly on production logs
2. Archive analysis reports for trend analysis
3. Set up automated alerts based on critical error counts
4. Use findings to improve application logging
5. Share reports with stakeholders for transparency

## License

This tool is part of the Fetch Assessment project.
