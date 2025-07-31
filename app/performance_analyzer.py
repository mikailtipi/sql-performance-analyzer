"""
Developed by Mikail Tipi
mkltipi@gmail.com
https://www.linkedin.com/in/mikailtipi/

Description:
    This module is part of the SQL Query Analyzer project. It provides the main Streamlit-based user interface for analyzing SQL Server queries.
    Created using Python 3.x and Streamlit.
"""

import re

def run_query_with_statistics(connection, query):
    cursor = connection.cursor()

    # Clear messages (from cursor)
    # Mesajları temizle (cursor'dan)
    cursor.messages.clear()
    
    
    # Enable STATISTICS commands
    # STATISTICS komutlarını aktif et
    cursor.execute("SET STATISTICS IO ON; SET STATISTICS TIME ON;")

    try:
        cursor.execute(query)
        try:
            _ = cursor.fetchall()
        except:
            pass  # SELECT değilse sorun çıkarmaz
                  # SELECT does not cause problems
    except Exception as e:
        return [f" Query could not be executed: {e}"]

    # STATISTICS kapat
    # close STATISTICS 

    cursor.execute("SET STATISTICS IO OFF; SET STATISTICS TIME OFF;")

    # Performans mesajlarını alır
    # Receives performance messages
    stats_output = [msg[1] for msg in cursor.messages if isinstance(msg[1], str)]

    return stats_output


def interpret_statistics_output(stats_output):
    results = []

    for line in stats_output:
        # Logical read yorumlama
        # Logical read interpretation
        if "logical reads" in line:
            table = re.search(r"Table '(\w+)'", line)
            reads = re.search(r"logical reads (\d+)", line)
            if table and reads:
                table_name = table.group(1)
                read_count = int(reads.group(1))
                if read_count > 1000:
                    results.append(f" {table_name} high logical read in table: {read_count}")
        
        # CPU süresi yorumlama
        # CPU time interpretation
        if "CPU time" in line:
            cpu_match = re.search(r"CPU time = (\d+)", line)
            if cpu_match:
                cpu_time = int(cpu_match.group(1))
                if cpu_time > 500:
                    results.append(f" High CPU time: {cpu_time} ms")

    if not results:
        results.append(" Performance values are normal.")

    return results
