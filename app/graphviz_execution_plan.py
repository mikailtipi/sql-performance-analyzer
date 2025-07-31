"""
Developed by Mikail Tipi
mkltipi@gmail.com
https://www.linkedin.com/in/mikailtipi/

Description:
    This module is part of the SQL Query Analyzer project. It provides the main Streamlit-based user interface for analyzing SQL Server queries.
    Created using Python 3.x and Streamlit.
"""
import xml.etree.ElementTree as ET

def parse_execution_plan_for_graphviz(xml_text):
    try:
        root = ET.fromstring(xml_text)
        plan_nodes = []
        edges = []

        def traverse(node, parent_id=None):
            if node.tag.endswith("RelOp"):
                node_id = node.attrib.get("NodeId", f"node{len(plan_nodes)}")
                logical_op = node.attrib.get("LogicalOp", "Unknown")
                physical_op = node.attrib.get("PhysicalOp", "Unknown")
                est_rows = node.attrib.get("EstimateRows", "N/A")

                label = f"{physical_op}\n{logical_op}\nRows: {est_rows}"
                plan_nodes.append((node_id, label))

                if parent_id:
                    edges.append((parent_id, node_id))

                for child in node:
                    traverse(child, node_id)
            else:
                for child in node:
                    traverse(child, parent_id)

        traverse(root)

        dot_output = "digraph ExecutionPlan {\n"
        for node_id, label in plan_nodes:
            dot_output += f'  "{node_id}" [label="{label}", shape=box];\n'
        for src, dst in edges:
            dot_output += f'  "{src}" -> "{dst}";\n'
        dot_output += "}"

        return {"status": "success", "dot": dot_output}

    except Exception as e:
        return {"status": "error", "error": str(e)}
