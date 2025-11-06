# Fetch-Assessment

# Project Execution Overview

## NEW: Log Analysis Expert Tool

A powerful Python-based log analyzer has been added to help identify errors and issues in application and database logs.

**Key Features:**
- Detects errors, exceptions, and critical issues in log files
- Specialized PostgreSQL database log analysis
- HTTP error code detection (4xx, 5xx)
- Severity classification (CRITICAL, HIGH, MEDIUM)
- Expert diagnosis and recommendations
- Zero external dependencies - pure Python!

**Quick Start:**
```bash
python3 log_analyzer.py sample_logs/application.log
python3 log_analyzer.py sample_logs/postgresql.log
```

For detailed documentation, see [LOG_ANALYZER_README.md](LOG_ANALYZER_README.md)

---

Objectives

Data Modeling and Transformation
What needed to happen:
I reviewed unstructured JSON data and created a structured, relational data model. This involved identifying key entities (Users, Brands, Receipts, and optionally Receipt_Items) and defining the relationships between them.
What happened:
A normalized data model was designed with the following tables:
• Users: Contains user details, including account creation dates
• Brands: Contains brand information
• Receipts: Contains transaction data linked to both Users and Brands
• Receipt_Items (optional): Contains details about individual items per receipt

Business Query Development
What needed to happen:
I developed SQL queries to answer predetermined business questions. These included identifying the top 5 brands by receipts scanned for the most recent month, comparing rankings between the recent and previous months, comparing average spend for Accepted vs. Rejected receipts, comparing total items purchased for Accepted vs. Rejected receipts, and finding which brand had the most spend or the most transactions among users created in the past 6 months.
What happened:
A series of PostgreSQL queries were written and tested using sample data. These queries extracted and aggregated data to identify top brands by transaction count, computed averages and totals to compare spending and item counts, and filtered data based on user creation dates to focus on recent user activity.

Data Quality Evaluation
What needed to happen:
Using PostgreSQL SQL queries (and optionally Python), I needed to identify potential data quality issues by checking for missing values, duplicate records, negative values where inappropriate, validating date fields, and ensuring foreign key relationships were intact.
What happened:
I ran a series of SQL queries to check for null values in key columns, duplicate primary key entries, negative or future-dated values, and valid references for users and brands. Under the defined rules, no data quality issues were identified.

Stakeholder Communication
What needed to happen:
A clear, professional message was required to communicate findings from the data quality review, raise questions about the data, and outline next steps for data optimization, performance, and scaling.
What happened:
I composed a professional email summarizing the approach and results, asking clarifying questions to ensure alignment with business expectations, and proposing steps such as partitioning, indexing, and caching to manage performance as data volumes grow.

Conclusion
This exercise successfully accomplished the following:
• Developed a clean and normalized relational data model from unstructured JSON input
• Created and tested SQL queries to address six critical business questions
• Performed thorough data quality checks, confirming the integrity of the data
• Prepared clear communication for business stakeholders, outlining findings, questions, and future optimization steps
• **NEW**: Created a comprehensive log analysis tool that acts as an expert in identifying errors from application and database logs

All relevant documents, SQL scripts, log analysis tools, and stakeholder communications have been committed to the GitHub repository as part of the overall exercise deliverable.
<img width="792" alt="Screenshot 2025-02-18 at 10 34 49 AM" src="https://github.com/user-attachments/assets/5e939aa0-e9ec-43e9-80bb-32e87c803ef3" />

