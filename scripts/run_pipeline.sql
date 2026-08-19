:On Error exit
:r scripts/int_database.sql
:r scripts/bronze/ddl_bronze.sql
:r scripts/bronze/proc_load_bronze.sql
EXEC bronze.load_bronze;
GO
:r scripts/silver/ddl_silver.sql
:r scripts/silver/proc_load_silver.sql
EXEC silver.load_silver;
GO
:r scripts/gold/ddl_gold.sql
:r tests/quality_checks_silver.sql
:r tests/quality_checks_gold.sql
