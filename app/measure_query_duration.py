"""
Developed by Mikail Tipi
mkltipi@gmail.com
https://www.linkedin.com/in/mikailtipi/

Description:
    This module is part of the SQL Query Analyzer project. It provides the main Streamlit-based user interface for analyzing SQL Server queries.
    Created using Python 3.x and Streamlit.
"""
import re
import pyodbc

def measure_query_duration_v3(connection, query):
    cursor = connection.cursor()
    try:
        # Sorgudan veritabanı adını çek (örnek: x.dbo.tablo)
        # Retrieve the database name from the query (example: x.dbo.table)
        match = re.search(r'(\w+)\.\w+\.\w+', query.lower())
        target_db = match.group(1) if match else connection.getinfo(pyodbc.SQL_DATABASE_NAME).lower()

        # Bu SP'yi git içerisinden bulabilirsiniz. Kendi veritabanınızda oluşturmanız gerekmektedir.
        # You can find this SP inside. You need to create it in your own database.
        cursor.execute(f"EXEC [{target_db}].dbo.RunAndMeasure ?", query)

        while True:
            if cursor.description is not None:
                result = cursor.fetchone()
                if result is not None and len(result) == 2 and isinstance(result[0], int):
                    return {
                        "status": "success",
                        "duration_ms": int(result[0]),
                        "row_count": int(result[1])
                    }
            if not cursor.nextset():
                break

        return {
            "status": "error",
            "error": "No valid performance result found."
        }

    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }
