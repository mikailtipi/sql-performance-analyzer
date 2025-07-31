"""
Developed by Mikail Tipi
mkltipi@gmail.com
https://www.linkedin.com/in/mikailtipi/

Description:
    This module is part of the SQL Query Analyzer project. It provides the main Streamlit-based user interface for analyzing SQL Server queries.
    Created using Python 3.x and Streamlit.
"""
import pyodbc

def connect_to_sql_server(server, database):
    try:
        conn_str = (
            f'DRIVER={{ODBC Driver 18 for SQL Server}};'
            f'SERVER={server};DATABASE={database};'
            f'Trusted_Connection=yes;'
            f'MARS_Connection=Yes;'
        )
        conn = pyodbc.connect(conn_str)
        print("Connection successful!")
        return conn
    except Exception as e:
        print("Connection failed. Error:")
        print(e)
        return None

# test için çalıştırılabilir
# run for testing
if __name__ == "__main__":
    server = input("Server name: ")
    database = input("Database name: ")

    conn = connect_to_sql_server(server, database)
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sys.tables")
        tables = cursor.fetchall()
        print("Tables:")
        for t in tables:
            print(f"- {t[0]}")
