"""
Developed by Mikail Tipi
mkltipi@gmail.com
https://www.linkedin.com/in/mikailtipi/

Description:
    This module is part of the SQL Query Analyzer project. It provides the main Streamlit-based user interface for analyzing SQL Server queries.
    Created using Python 3.x and Streamlit.
"""
from measure_query_duration import measure_query_duration_v3
from query_optimizer_engine import analyze_structure

import re
import pyodbc

def extract_tables_from_query(query):
    raw = re.findall(r'(?:from|join)\s+([a-zA-Z0-9_\[\]\.]+)', query.lower())
    tables = []
    for t in raw:
        cleaned = t.replace("[", "").replace("]", "")
        tables.append(cleaned.strip())
    return tables

def analyze_query(connection, query, metadata_dict):
    metadata_dict = {k.strip().lower(): v for k, v in metadata_dict.items()}
    result = {
        "query": query,
        "tables": [],
        "table_metadata": [],
        "structure_findings": [],
        "performance": {},
        "recommendations": []
    }

    default_db = connection.getinfo(pyodbc.SQL_DATABASE_NAME).lower()

    #  Yapısal analiz (SELECT *, WHERE vs)
    # Structural analysis (SELECT *, WHERE vs)
    result["structure_findings"] = analyze_structure(query, metadata_dict)

    # Tabloları çıkar
    # Remove tables
    tables = extract_tables_from_query(query)
    result["tables"] = tables

    for t in tables:
        parts = t.split(".")
        if len(parts) == 3:
            db, schema, name = parts
            key = f"{db}.{schema}.{name}".lower()
        elif len(parts) == 2:
            schema, name = parts
            db = default_db
            key = f"{db}.{schema}.{name}".lower()
        else:
            name = parts[0].strip().lower()
            matches = [k for k in metadata_dict if k.endswith(f".{name}")]
            if len(matches) == 1:
                key = matches[0]
            elif len(matches) > 1:
                result["recommendations"].append(f" '{name}' table found with multiple matches: {matches}")
                continue
            else:
                result["recommendations"].append(f" '{name}' table could not be found in the metadata.")
                continue

        meta = metadata_dict.get(key.strip().lower())
        if meta is not None:
            result["table_metadata"].append({
                "table": key,
                "row_count": meta["row_count"],
                "column_count": meta["column_count"],
                "has_index": meta["has_index"]
            })
            if meta["row_count"] > 1_000_000 and not meta["has_index"]:
                result["recommendations"].append(f" {key} large but no index definition.")

    # Performans ölçümü (SP üzerinden)
    # Performance measurement (via SP)
    perf = measure_query_duration_v3(connection, query)
    result["performance"] = perf

    if perf["status"] == "success":
        dur = perf["duration_ms"]
        if dur < 200:
            result["recommendations"].append("✅ The query ran quickly.")
        elif dur < 1000:
            result["recommendations"].append("⚠️ Ran at medium speed.")
        else:
            result["recommendations"].append("🔥 The query is slow and needs to be optimised.")

    return result



def analyze_execution_plan(connection, query):
    try:
        cursor = connection.cursor()
        cursor.execute("SET SHOWPLAN_XML ON;")
        cursor.execute(query)
        plan = ""
        for row in cursor.fetchall():
            plan += row[0]  # XML text is in the first column
        cursor.execute("SET SHOWPLAN_XML OFF;")
        return {"status": "success", "plan_xml": plan}
    except Exception as e:
        return {"status": "error", "error": str(e)}
