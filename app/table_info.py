"""
Developed by Mikail Tipi
mkltipi@gmail.com
https://www.linkedin.com/in/mikailtipi/

Description:
    This module is part of the SQL Query Analyzer project. It provides the main Streamlit-based user interface for analyzing SQL Server queries.
    Created using Python 3.x and Streamlit.
"""
import pandas as pd
from datetime import datetime
import pyodbc

def get_table_info(connection, export_excel=False, export_version="v1"):
    cursor = connection.cursor()
    result_list = []

    # Dinamik dosya adı oluştur
    # Create dynamic file name
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    export_path = f"table_info_output_{timestamp}_{export_version}.xlsx"

    # Aktif veritabanı adını al
    # Get the name of the active database
    db_name = connection.getinfo(pyodbc.SQL_DATABASE_NAME)

    # Tabloları al
    # Get the tables
    cursor.execute("""
        SELECT 
            s.name AS schema_name,
            t.name AS table_name,
            SUM(p.rows) AS row_count
        FROM sys.tables t
        INNER JOIN sys.schemas s ON t.schema_id = s.schema_id
        INNER JOIN sys.partitions p ON t.object_id = p.object_id
        WHERE p.index_id IN (0,1)
        GROUP BY s.name, t.name
        ORDER BY row_count DESC;
    """)
    tables = cursor.fetchall()

    for table in tables:
        schema_name = table[0]
        table_name = table[1]
        row_count = table[2]
        full_table_name = f"[{schema_name}].[{table_name}]"

        # Kolon sayısı (parametreli)
        # Number of columns (parameterised)
        cursor.execute("""
            SELECT COUNT(*) 
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_SCHEMA = ? AND TABLE_NAME = ?
        """, (schema_name, table_name))
        column_count = cursor.fetchone()[0]

        # Index bilgisi
        # Index information
        cursor.execute("""
            SELECT i.name, i.type_desc
            FROM sys.indexes i
            INNER JOIN sys.tables t ON i.object_id = t.object_id
            INNER JOIN sys.schemas s ON t.schema_id = s.schema_id
            WHERE t.name = ? AND s.name = ? AND i.name IS NOT NULL
        """, (table_name, schema_name))
        indexes = cursor.fetchall()
        index_list = [f"{i[0]} ({i[1]})" for i in indexes]
        index_str = ", ".join(index_list) if index_list else "Yok"

        print(f" Table: {full_table_name}")
        print(f"   ➞ Number of lines: {row_count}")
        print(f"   ➞ Number of columns: {column_count}")
        print(f"   ➞ Indexes: {index_str}\n")

        # Index kolon bilgisi
        # Index column information
        cursor.execute("""
            SELECT c.name
            FROM sys.index_columns ic
            JOIN sys.indexes i ON ic.object_id = i.object_id AND ic.index_id = i.index_id
            JOIN sys.columns c ON ic.object_id = c.object_id AND ic.column_id = c.column_id
            JOIN sys.tables t ON t.object_id = i.object_id
            JOIN sys.schemas s ON t.schema_id = s.schema_id
            WHERE t.name = ? AND s.name = ? AND i.is_primary_key = 0 AND i.name IS NOT NULL
        """, (table_name, schema_name))
        index_column_names = [row[0] for row in cursor.fetchall()]

        result_list.append({
            "database": db_name.lower(),
            "schema": schema_name.lower(),
            "table": table_name.lower(),
            "row_count": row_count,
            "column_count": column_count,
            "has_index": index_str != "Yok",
            "index_columns": index_column_names
        })

    if export_excel:
        df = pd.DataFrame(result_list)
        df.to_excel(export_path, index=False)
        print(f"\n📄 Excel output created: {export_path}")

    return result_list, export_path
