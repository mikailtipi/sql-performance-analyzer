"""
Developed by Mikail Tipi
mkltipi@gmail.com
https://www.linkedin.com/in/mikailtipi/

Description:
    This module is part of the SQL Query Analyzer project. It provides the main Streamlit-based user interface for analyzing SQL Server queries.
    Created using Python 3.x and Streamlit.
"""

import re

def extract_tables_from_query(query):
    # Capture table names coming from FROM and JOIN
    # FROM ve JOIN ile gelen tablo adlarını yakala
    
    return re.findall(r'(?:from|join)\s+([a-zA-Z0-9_\[\]\.]+)', query.lower())

def analyze_structure(query, table_metadata_dict):
    findings = []

    if "select *" in query.lower():
        findings.append("🚘 'SELECT *' usage detected. Only required columns should be selected.")

    if "where" not in query.lower():
        findings.append("⚠️ There is no WHERE filter in the query. There may be a risk of full scan on the tables.")

    tables = extract_tables_from_query(query)
    for raw_table in tables:
        cleaned_table = raw_table.replace("[", "").replace("]", "")
        parts = cleaned_table.split('.')
        if len(parts) == 3:
            db, schema, name = parts
            key = f"{db.strip().lower()}.{schema.strip().lower()}.{name.strip().lower()}"
        elif len(parts) == 2:
            schema, name = parts
            key = f"{schema.strip().lower()}.{name.strip().lower()}"
        else:
            name = parts[0]
            key = name.strip().lower()

        if key in table_metadata_dict:
            meta = table_metadata_dict[key]

            if meta["row_count"] > 1_000_000:
                findings.append(f"🔥 Table '{key}' contains over 1M rows. WHERE clause is recommended.")
                if not meta["has_index"]:
                    findings.append(f"🧱 Table '{key}' is large but has no index defined.")
        else:
            findings.append(f"❓ Table '{key}' not found in Excel metadata.")

    if not findings:
        findings.append("✅ Query is clean. It follows basic optimization rules.")

    return findings
