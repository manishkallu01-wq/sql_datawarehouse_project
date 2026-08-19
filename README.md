# 🏗️ Modern SQL Server Data Warehouse — Medallion Architecture

> End-to-end **Data Engineering** project implementing a **Bronze → Silver → Gold** warehouse on SQL Server, with source ingestion, data cleansing, cross-system integration, dimensional modeling, data-quality controls, and analytics-ready SQL.

## Executive Summary

This repository covers the complete lifecycle of a batch analytical warehouse:

**CRM + ERP files → Bronze ingestion → Silver transformation → Gold dimensional model → Data-quality validation → Analytics**

The focus is the engineering work that sits behind reliable reporting: preserving raw source data, applying deterministic transformation rules, integrating systems, modeling business entities, and validating the resulting warehouse.

## 🎯 What The implementation covers

- Designing a layered **medallion architecture** in SQL Server
- Building repeatable ingestion procedures with `BULK INSERT`
- Cleansing and standardizing multi-source operational data
- Deduplicating records with SQL window functions
- Integrating CRM and ERP identifiers
- Building fact and dimension models for analytics
- Implementing reusable data-quality checks
- Separating ingestion, transformation, and analytical consumption
- Producing business-ready SQL views from warehouse data

## 🏛️ Architecture

![Data Architecture](docs/Data%20Architecture.png)

```text
CRM CSV ──────┐
              ├──► BRONZE ──► SILVER ──► GOLD ──► ANALYTICS
ERP CSV ──────┘       │           │         │
                      │           │         └── Fact + Dimensions
                      │           └──────────── Cleansing + Integration
                      └──────────────────────── Raw Source Preservation
```

### Bronze — Raw Ingestion

- Loads CRM and ERP files into dedicated Bronze tables.
- Preserves source-level values before business transformations.
- Isolates ingestion from downstream analytical logic.
- Captures warehouse load timing for operational traceability.

### Silver — Cleansing & Integration

- Standardizes names, gender, marital status, country, and product-line values.
- Removes duplicate customer records using `ROW_NUMBER()`.
- Converts encoded source dates into SQL `DATE` values.
- Validates sales, prices, quantities, and customer dates.
- Normalizes identifiers across CRM and ERP sources.
- Handles nulls and invalid source values consistently.

### Gold — Business Model

- Builds customer and product dimensions.
- Builds the sales fact model.
- Generates surrogate keys.
- Integrates CRM and ERP attributes into a reporting-ready structure.
- Exposes business-facing views for downstream SQL and BI workloads.

## 📊 Dimensional Model

![Data Model](docs/Data%20Model.png)

| Model | Role | Purpose |
|---|---|---|
| `gold.dim_customers` | Dimension | Customer attributes and demographics |
| `gold.dim_products` | Dimension | Product, category, cost, and product-line attributes |
| `gold.fact_sales` | Fact | Order-level sales measures and dimension keys |

The Gold layer follows a star-schema-oriented design so analytical queries can consume business entities without repeatedly traversing raw source tables.

## 🔄 Data Flow

![Data Flow](docs/Data%20flow.png)

1. **Ingest** CRM and ERP source files.
2. **Preserve** source data in Bronze tables.
3. **Clean** and standardize records in Silver.
4. **Integrate** identifiers and business attributes across sources.
5. **Model** facts and dimensions in Gold.
6. **Validate** keys, values, dates, and business rules.
7. **Consume** Gold views for analytics and reporting.

## 🧪 Data Quality Framework

The repository includes SQL validation for:

- Null and duplicate keys
- Whitespace contamination
- Standardized categorical values
- Negative or invalid costs
- Invalid date relationships
- Sales / quantity / price consistency
- Out-of-range customer birth dates
- Country and category consistency

These checks are treated as part of the pipeline rather than an afterthought to reporting.

## ⚙️ Engineering Implementation

### Source Ingestion

`bronze.load_bronze` loads source files into SQL Server and reports load duration, providing a repeatable ingestion boundary.

### Transformation Pipeline

`silver.load_silver` performs the main transformation workload, including:

- Deduplication with `ROW_NUMBER()`
- String trimming and normalization
- Business-code mapping
- Date validation and conversion
- Derived sales and price correction
- Cross-source identifier normalization
- Null/default handling

### Analytical Layer

Gold views integrate Silver data into a star-schema-style model designed for analytical SQL and BI consumption.

## 📁 Repository Structure

```text
sql_datawarehouse_project/
├── datasets/                     # CRM and ERP source files
├── docs/                         # Architecture and model diagrams
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

## 🚀 Local Execution

### Prerequisites

- SQL Server 2019+ or SQL Server Express
- SQL Server Management Studio or Azure Data Studio
- Access to the repository source CSV files

### Execution Order

```text
1. Create database and schemas
2. Run Bronze DDL
3. Configure BULK INSERT paths
4. Execute bronze.load_bronze
5. Run Silver DDL
6. Execute silver.load_silver
7. Run Gold scripts/views
8. Execute quality checks
9. Query Gold models
```

Example:

```sql
EXEC bronze.load_bronze;
EXEC silver.load_silver;

SELECT TOP 100 * FROM gold.fact_sales;
SELECT TOP 100 * FROM gold.dim_customers;
SELECT TOP 100 * FROM gold.dim_products;
```

## 💡 Engineering rationale

A warehouse is more than a collection of SQL queries. The implementation covers the engineering boundaries that make analytical data trustworthy:

**raw data preservation → controlled transformations → integrated business model → automated validation → analytics consumption**

## 🔮 Production Extensions

A production evolution could add:

- Incremental loading and watermarking
- SCD Type 2 dimensions where historical tracking is required
- dbt-based transformation and testing
- Airflow orchestration
- Cloud object-storage ingestion
- Warehouse observability and freshness monitoring
- CI/CD for SQL deployment
- Metadata/catalog and lineage management

## 👨‍💻 Portfolio

**Manish Kallu** — Data engineering work focused on SQL, distributed processing, data pipelines, analytics platforms, and production-style data architecture.

- GitHub: [manishkallu01-wq](https://github.com/manishkallu01-wq)
- Email: manishkallu01@gmail.com

## 📌 Project summary Project Description

**Engineered a SQL Server data warehouse using Bronze–Silver–Gold architecture to ingest and integrate CRM/ERP data, implement cleansing and deduplication workflows, model analytical facts and dimensions, and enforce SQL-based data-quality validation for reporting-ready datasets.**

## License

MIT License. See [LICENSE](LICENSE).

## Reproducibility and acceptance criteria

This project is considered reproducible when a reviewer can provision SQL Server, point the Bronze loader at the checked-in CSV sources, execute the numbered pipeline, and receive zero rows from every quality check.

| Stage | Input | Output | Acceptance gate |
|---|---|---|---|
| Bootstrap | SQL Server instance | `DataWarehouse` + three schemas | Schemas exist |
| Bronze | Six source CSV files | Source-aligned tables | Row counts are non-zero |
| Silver | Bronze tables | Typed, standardized records | Silver quality queries return zero defects |
| Gold | Silver tables | Customer/product dimensions and sales fact | Gold key and referential checks return zero defects |

Run the scripts in this exact order:

```text
scripts/int_database.sql
scripts/bronze/ddl_bronze.sql
scripts/bronze/proc_load_bronze.sql
EXEC bronze.load_bronze
scripts/silver/ddl_silver.sql
scripts/silver/proc_load_silver.sql
EXEC silver.load_silver
scripts/gold/ddl_gold.sql
tests/quality_checks_silver.sql
tests/quality_checks_gold.sql
```

Important: `scripts/int_database.sql` is destructive and recreates the database. The Bronze loader currently uses local SQL Server filesystem paths; update those six paths for your environment before execution. A production implementation should replace full refreshes with parameterized, audited, incremental loads.

## Definition of done

- Raw inputs remain immutable and traceable.
- Transformations are deterministic and rerunnable.
- Business grain is explicit: customer, product, and sales order line.
- Dimension keys are unique and facts resolve to valid dimensions.
- Quality checks return zero failing records before Gold is released.
- README claims are limited to behavior implemented in this repository.
