"""
Developed by Mikail Tipi
mkltipi@gmail.com
https://www.linkedin.com/in/mikailtipi/

Description:
    This module is part of the SQL Query Analyzer project. It provides the main Streamlit-based user interface for analyzing SQL Server queries.
    Created using Python 3.x and Streamlit.
"""
# tablo adı -> row count, index bilgisi şeklinde dict
# table name -> row count, index information in the form of a dict

def get_table_stats_dict(connection):
    cursor = connection.cursor()
    stats_dict = {}

    cursor.execute("""
        SELECT 
            t.name AS table_name,
            SUM(p.rows) AS row_count
        FROM sys.tables t
        INNER JOIN sys.partitions p ON t.object_id = p.object_id
        WHERE p.index_id IN (0,1)
        GROUP BY t.name;
    """)
    tables = cursor.fetchall()

    for table in tables:
        table_name = table[0]
        row_count = table[1]

        cursor.execute(f"""
            SELECT COUNT(*) 
            FROM sys.indexes i
            INNER JOIN sys.tables t ON i.object_id = t.object_id
            WHERE t.name = '{table_name}' AND i.name IS NOT NULL
        """)
        index_count = cursor.fetchone()[0]

        stats_dict[table_name.lower()] = {
            "row_count": row_count,
            "has_index": index_count > 0
        }

    return stats_dict
