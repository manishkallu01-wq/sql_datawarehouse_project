"""Dependency-free repository contract validator."""
from pathlib import Path
import re, sys

ROOT=Path(__file__).resolve().parents[1]
required=["README.md","scripts/int_database.sql","scripts/bronze/ddl_bronze.sql","scripts/bronze/proc_load_bronze.sql","scripts/silver/ddl_silver.sql","scripts/silver/proc_load_silver.sql","scripts/gold/ddl_gold.sql","tests/quality_checks_silver.sql","tests/quality_checks_gold.sql"]
errors=[f"missing: {p}" for p in required if not (ROOT/p).is_file()]
readme=(ROOT/"README.md").read_text(encoding="utf-8")
for phrase in ["Executive Summary","Architecture","Data Quality","Reproducibility","Definition of done"]:
    if phrase.lower() not in readme.lower(): errors.append(f"README missing section: {phrase}")
sql="\n".join((ROOT/p).read_text(encoding="utf-8") for p in required if p.endswith(".sql"))
for token in ["bronze","silver","gold"]:
    if not re.search(rf"\b{token}\b",sql,re.I): errors.append(f"SQL missing layer: {token}")
if errors:
    print("\n".join(f"ERROR {e}" for e in errors)); sys.exit(1)
print(f"PASS repository contract ({len(required)} required artifacts)")
