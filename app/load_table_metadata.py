"""
Developed by Mikail Tipi
mkltipi@gmail.com
https://www.linkedin.com/in/mikailtipi/

Description:
    This module is part of the SQL Query Analyzer project. It provides the main Streamlit-based user interface for analyzing SQL Server queries.
    Created using Python 3.x and Streamlit.
"""
import pandas as pd

def load_table_metadata(path):
    df = pd.read_excel(path)
    table_dict = {}

    for _, row in df.iterrows():
        key = f"{row['Şema'].strip().lower()}.{row['Tablo Adı'].strip().lower()}"
        table_dict[key] = {
            "row_count": int(row["Row Count"]),
            "column_count": int(row["Column Count"]),
            "has_index": False if str(row["Index Information"]).strip().lower() == "yok" else True
        }

    return table_dict
