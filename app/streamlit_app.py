"""
Developed by Mikail Tipi
mkltipi@gmail.com
https://www.linkedin.com/in/mikailtipi/

Description:
    This module is part of the SQL Query Analyzer project. It provides the main Streamlit-based user interface for analyzing SQL Server queries.
    Created using Python 3.x and Streamlit.
"""
import streamlit as st
import pandas as pd
from datetime import datetime
import os

def connect_to_sql_server(server, db_name, username=None, password=None):
    import pyodbc
    if username and password:
        conn_str = (
            f"DRIVER={{ODBC Driver 18 for SQL Server}};"
            f"SERVER={server};"
            f"DATABASE={db_name};"
            f"UID={username};"
            f"PWD={password};"
            f"Encrypt=yes;"
            f"TrustServerCertificate=yes;"
        )
    else:
        conn_str = (
            f"DRIVER={{ODBC Driver 18 for SQL Server}};"
            f"SERVER={server};"
            f"DATABASE={db_name};"
            f"Trusted_Connection=yes;"
            f"Encrypt=yes;"
            f"TrustServerCertificate=yes;"
        )
    try:
        return pyodbc.connect(conn_str)
    except Exception as e:
        print("Connection failed:", e)
        return None

from query_analyzer import analyze_query, analyze_execution_plan
from table_info import get_table_info
from graphviz_execution_plan import parse_execution_plan_for_graphviz

st.set_page_config(page_title="SQL Query Analysis Tool", layout="wide")

with st.sidebar:
    st.header("🎨 Theme Settings")
    theme = st.radio("Select Theme", ["Light", "Dark"])

if theme == "Dark":
    st.markdown("""
        <style>
            body {
                background-color: #0e1117;
                color: #fafafa;
            }
            .stTextInput>div>div>input,
            .stTextArea textarea {
                background-color: #1e2127;
                color: white;
            }
            .stButton>button {
                background-color: #4a4a4a;
                color: white;
            }
        </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
        <style>
            body {
                background-color: white;
                color: black;
            }
            .stTextInput>div>div>input,
            .stTextArea textarea {
                background-color: white;
                color: black;
            }
            .stButton>button {
                background-color: #f0f0f0;
                color: black;
            }
        </style>
    """, unsafe_allow_html=True)

st.title("🔮 SQL Performance and Structural Analysis Tool")

if "conn" not in st.session_state:
    st.session_state.conn = None
if "metadata" not in st.session_state:
    st.session_state.metadata = None
if "metadata_excel_path" not in st.session_state:
    st.session_state.metadata_excel_path = None
if "query_log" not in st.session_state:
    st.session_state.query_log = []

with st.sidebar:
    st.header("🚀 Connection Informations")
    server = st.text_input("Server Name", placeholder=".")
    db_list_input = st.text_input("Databases (comma separated)", placeholder="db1, db2")
    db_names = [db.strip() for db in db_list_input.split(",") if db.strip()]

    auth_method = st.selectbox("Authentication Method", ["Windows Authentication", "SQL Server Authentication"])
    username = password = None
    if auth_method == "SQL Server Authentication":
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

    if st.button("✔️ Connect"):
        if db_names:
            conn = connect_to_sql_server(server, db_names[0], username, password)
            if conn:
                st.session_state.conn = conn
                st.success(f"✅ Successfully connected to the {db_names[0]} database.")
            else:
                st.error(f"❌ Unable to connect to the {db_names[0]} database.")
        else:
            st.warning("⚠️ Please enter at least one database.")

if st.session_state.conn:
    st.sidebar.header("📦 Metadata Source Selection")
    use_excel = st.sidebar.radio("Where would you like to get the metadata from?", ["Pull from Database", "Upload from Excel"])

    if use_excel == "Pull from Database":
        if st.sidebar.button("🔄 Create Metadata"):
            all_metadata = []
            for db in db_names:
                conn = connect_to_sql_server(server, db, username, password)
                if conn:
                    with st.spinner(f"🛠 Collecting metadata: {db}..."):
                        meta, _ = get_table_info(conn, export_excel=False)
                        all_metadata.extend(meta)
                else:
                    st.error(f"❌ Connection failed for {db}.")
            df = pd.DataFrame(all_metadata)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M")
            export_path = f"table_info_output_{timestamp}_merged.xlsx"
            df.to_excel(export_path, index=False)
            st.session_state.metadata_excel_path = export_path
            st.session_state.metadata = {
                f"{item['database'].lower()}.{item['schema'].lower()}.{item['table'].lower()}": item
                for item in all_metadata
            }
            st.success("✅ Metadata successfully created.")
    else:
        uploaded_file = st.sidebar.file_uploader("📤 Upload Excel Metadata File", type="xlsx")
        if uploaded_file:
            df = pd.read_excel(uploaded_file)
            st.session_state.metadata = {
                f"{row['database'].lower()}.{row['schema'].lower()}.{row['table'].lower()}": row
                for _, row in df.iterrows()
            }
            st.success("✅ Excel metadata successfully uploaded.")

if st.session_state.metadata:
    st.subheader("📃 Query Input")
    user_query = st.text_area("Write your SQL query", height=200)

    if st.button("📉 Show Execution Plan"):
        plan_result = analyze_execution_plan(st.session_state.conn, user_query)
        if plan_result["status"] == "success":
            st.success("✅ Execution plan retrieved successfully.")
            st.code(plan_result["plan_xml"][:5000], language="xml")
            graphviz_result = parse_execution_plan_for_graphviz(plan_result["plan_xml"])
            if graphviz_result["status"] == "success":
                st.graphviz_chart(graphviz_result["dot"])
            else:
                st.error(f"❌ Graphviz rendering error: {graphviz_result['error']}")
                st.download_button(
                    label="⬇️ Download Execution Plan XML",
                    data=plan_result["plan_xml"],
                    file_name="execution_plan.xml",
                    mime="application/xml"
                )
        else:
            st.error(f"❌ Failed to retrieve execution plan: {plan_result['error']}")

    if st.button("🔍 Analyze"):
        result = analyze_query(st.session_state.conn, user_query, st.session_state.metadata)
        if result["performance"]["status"] == "success":
            duration = result["performance"]["duration_ms"]
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            st.session_state.query_log.append({
                "query": user_query.strip(),
                "duration_ms": duration,
                "timestamp": timestamp
            })
            previous_runs = [q for q in st.session_state.query_log if q["query"].strip() == user_query.strip()]
            if len(previous_runs) > 1:
                previous_duration = previous_runs[-2]["duration_ms"]
                diff = duration - previous_duration
                st.info(f"⚖️ Previous run duration: {previous_duration} ms → Δ {diff:+.2f} ms")

        with st.expander("📂 Structural Analysis"):
            st.write(result["structure_findings"] or "No problem detected.")

        with st.expander("🕛 Performance Result"):
            perf = result["performance"]
            if perf["status"] == "success":
                st.metric("Duration (ms)", perf["duration_ms"])
                st.metric("Row Count", perf["row_count"])
            else:
                st.error(perf["error"])

        with st.expander("🔸 Tables and Metadata"):
            st.dataframe(pd.DataFrame(result["table_metadata"]))

        with st.expander("📊 Recommendations"):
            for r in result["recommendations"]:
                st.write("-", r)

    if st.session_state.metadata_excel_path:
        file_name = os.path.basename(st.session_state.metadata_excel_path)
        with open(st.session_state.metadata_excel_path, "rb") as f:
            st.download_button("📄 Download Metadata Excel", data=f, file_name=file_name)

else:
    st.info("Please establish a database connection and provide metadata first.")

with st.expander("🧾 Query History"):
    if st.session_state.query_log:
        df_log = pd.DataFrame(st.session_state.query_log)
        st.dataframe(df_log)
    else:
        st.info("No queries logged yet.")

st.markdown("""
    <hr style="margin-top: 50px;">
    <div style="text-align: center; font-size: 14px;">
        Developed by <b>Mikail Tipi</b><br>
        📧 <a href="mailto:mkltipi@gmail.com">mkltipi@gmail.com</a> |
        🔗 <a href="https://www.linkedin.com/in/mikailtipi/" target="_blank">LinkedIn</a>
    </div>
""", unsafe_allow_html=True)
