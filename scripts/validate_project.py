"""Dependency-free repository contract validator."""
from pathlib import Path
import re, sys

ROOT=Path(__file__).resolve().parents[1]
required=["README.md","scripts/run_pipeline.sql","scripts/int_database.sql","scripts/bronze/ddl_bronze.sql","scripts/bronze/proc_load_bronze.sql","scripts/silver/ddl_silver.sql","scripts/silver/proc_load_silver.sql","scripts/gold/ddl_gold.sql","tests/quality_checks_silver.sql","tests/quality_checks_gold.sql"]
errors=[f"missing: {p}" for p in required if not (ROOT/p).is_file()]
readme=(ROOT/"README.md").read_text(encoding="utf-8")
for phrase in ["Business need","Data flow","Run the warehouse","Validation","Results","Limitations"]:
    if phrase.lower() not in readme.lower(): errors.append(f"README missing section: {phrase}")
sql={p:(ROOT/p).read_text(encoding="utf-8") for p in required if p.endswith(".sql") and (ROOT/p).is_file()}
all_sql="\n".join(sql.values())
for layer in ["bronze","silver","gold"]:
    if not re.search(rf"\b{layer}\b",all_sql,re.I): errors.append(f"SQL missing layer: {layer}")
bronze=sql.get("scripts/bronze/ddl_bronze.sql","")
tables=["crm_cust_info","crm_prd_info","crm_sales_details","erp_loc_a101","erp_cust_az12","erp_px_cat_g1v2"]
for table in tables:
    if f"OBJECT_ID('bronze.{table}'" not in bronze: errors.append(f"Bronze DDL lacks rerun guard: {table}")
loader=sql.get("scripts/bronze/proc_load_bronze.sql","")
if "$(DatasetRoot)" not in loader: errors.append("Bronze loader does not use DatasetRoot")
if "C:\\sql\\dwh_project" in loader: errors.append("Bronze loader contains a machine-specific path")
for source in ["source_crm/cust_info.csv","source_crm/prd_info.csv","source_crm/sales_details.csv","source_erp/LOC_A101.csv","source_erp/CUST_AZ12.csv","source_erp/PX_CAT_G1V2.csv"]:
    if not (ROOT/"datasets"/source).is_file(): errors.append(f"missing dataset: {source}")
    windows=source.replace("/","\\")
    if windows not in loader: errors.append(f"loader does not reference exact dataset name: {source}")
runner=sql.get("scripts/run_pipeline.sql","")
for script in required[2:]:
    if script.endswith(".sql") and script not in runner and script!="scripts/run_pipeline.sql": errors.append(f"runner missing: {script}")
if errors:
    print("\n".join(f"ERROR {e}" for e in errors)); sys.exit(1)
print(f"PASS repository contract ({len(required)} required artifacts)")
