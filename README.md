# Modern SQL Server Data Warehouse — Medallion Architecture

> End-to-end Data Engineering portfolio project implementing a **Bronze → Silver → Gold** warehouse on SQL Server, with source ingestion, data cleansing, cross-system integration, dimensional modeling, data-quality validation, and analytics-ready SQL views.

## Project Summary

This repository demonstrates the core workflow of a modern batch Data Engineering platform:

**CRM + ERP CSV sources → Bronze ingestion → Silver cleansing/integration → Gold dimensional model → Analytics & reporting**

The implementation uses SQL Server stored procedures and SQL transformations to turn raw operational files into a business-ready analytical model.

## Architecture

![Data Architecture](docs/Data%20Architecture.png)

### Bronze — Raw Ingestion

- Loads CRM and ERP CSV files with `BULK INSERT`.
- Preserves source-level data before business transformations.
- Uses dedicated `bronze` tables for source isolation.

### Silver — Cleansing & Integration

- Standardizes names, gender, marital status, product-line codes, and country values.
- Removes duplicate customer records using window functions.
- Converts encoded integer dates into SQL `DATE` values.
- Handles invalid sales, prices, quantities, future birth dates, and missing values.
- Adds warehouse load timestamps for operational traceability.

### Gold — Business Model

- Builds customer and product dimensions.
- Creates a sales fact model.
- Generates surrogate keys with `ROW_NUMBER()`.
- Integrates CRM and ERP attributes into a reporting-ready star schema.
- Exposes business-ready views for downstream analytics.

## Data Flow

![Data Flow](docs/Data%20flow.png)

```text
CRM CSV ──────┐
              ├──► Bronze ──► Silver ──► Gold Dimensions ──┐
ERP CSV ──────┘             │                              │
                            └── Data Quality Checks        ├──► Analytics
                                                           │
                                                           └──► Reporting
```

## Dimensional Model

![Data Model](docs/Data%20Model.png)

The Gold layer contains the primary analytical entities:

| Model | Purpose |
|---|---|
| `gold.dim_customers` | Customer attributes and demographics |
| `gold.dim_products` | Product, category, cost, and product-line attributes |
| `gold.fact_sales` | Order-level sales measures and dimension keys |

## Engineering Work Implemented

### Source Ingestion

`bronze.load_bronze` loads the CRM and ERP source files into SQL Server Bronze tables and reports batch/load duration.

### Transformation Pipeline

`silver.load_silver` performs the main transformation workload, including:

- Deduplication with `ROW_NUMBER()`
- String trimming and normalization
- Business-code mapping
- Date validation/conversion
- Derived sales and price correction
- Cross-source identifier normalization
- Null/default handling

### Analytical Modeling

The Gold views integrate the Silver layer into a star-schema-style model suitable for BI and SQL analytics.

### Data Quality

The repository includes SQL quality checks for:

- Null or duplicate keys
- Whitespace contamination
- Standardized categorical values
- Negative/invalid costs
- Invalid date sequences
- Sales/quantity/price consistency
- Out-of-range customer birth dates
- Country and category consistency

## Repository Structure

```text
sql_datawarehouse_project/
├── datasets/                     # CRM and ERP source files
├── docs/
│   ├── Data Architecture.png
│   ├── Data Integration.png
│   ├── Data Model.png
│   └── Data flow.png
├── scripts/
│   ├── bronze/
│   │   ├── ddl_bronze.sql
│   │   └── proc_load_bronze.sql
│   ├── silver/
│   │   ├── ddl_silver.sql
│   │   └── proc_load_silver.sql
│   └── gold/
│       └── ddl_gold.sql
├── tests/
│   └── quality_checks_silver.sql
├── README.md
└── LICENSE
```

## Local Execution

### Prerequisites

- SQL Server 2019+ or SQL Server Express
- SQL Server Management Studio (SSMS) or Azure Data Studio
- Access to the repository's source CSV files

### Execution Order

1. Create the database and schemas.
2. Run the Bronze DDL script.
3. Update the `BULK INSERT` file paths in `scripts/bronze/proc_load_bronze.sql` for your machine.
4. Execute `bronze.load_bronze`.
5. Run the Silver DDL script.
6. Execute `silver.load_silver`.
7. Run the Gold view script.
8. Execute `tests/quality_checks_silver.sql` and investigate any unexpected results.
9. Query the Gold views for analytics.

Example:

```sql
EXEC bronze.load_bronze;
EXEC silver.load_silver;

SELECT TOP 100 * FROM gold.fact_sales;
SELECT TOP 100 * FROM gold.dim_customers;
SELECT TOP 100 * FROM gold.dim_products;
```

## Data Engineering Skills Demonstrated

- SQL Server ETL
- Medallion architecture
- Batch data ingestion
- Data cleansing and standardization
- Relational data modeling
- Star-schema design
- Fact and dimension modeling
- Window functions
- Stored procedures
- Data quality validation
- Cross-system integration
- Analytical SQL
- Warehouse load monitoring

## Portfolio Positioning

This project is intentionally positioned as a **Data Engineering project**, not simply a SQL analytics exercise. The strongest interview discussion points are the ingestion boundary, transformation rules, data-quality controls, dimensional model, and separation between raw, cleansed, and business-ready data.

## License

MIT License. See [LICENSE](LICENSE).
