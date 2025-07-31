"""
Developed by Mikail Tipi
mkltipi@gmail.com
https://www.linkedin.com/in/mikailtipi/

Description:
    This module is part of the SQL Query Analyzer project. It provides the main Streamlit-based user interface for analyzing SQL Server queries.
    Created using Python 3.x and Streamlit.
"""
from connection import connect_to_sql_server
from measure_query_duration import measure_query_duration_v3

if __name__ == "__main__":
    server = input("Server Name: ")
    database = input("Database Name: ")
    conn = connect_to_sql_server(server, database)

    print("\n Paste your SQL query (press Enter + Enter to finish):\n")
    lines = []
    while True:
        line = input()
        if line.strip() == "":
            break
        lines.append(line)

    user_query = "\n".join(lines)

    result = measure_query_duration_v3(conn, user_query)

    if result["status"] == "success":
        print(f"\n Time: {result['duration_ms']} ms")
        print(f" Number of affected rows: {result['row_count']}")
    else:
        print("Error:", result["error"])
