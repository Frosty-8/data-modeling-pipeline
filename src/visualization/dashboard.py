import pandas as pd
import sqlite3
from pathlib import Path
import plotly.express as px
import plotly.graph_objects as go
from config.paths import DB_PATH

# -----------------------------
# 1️⃣ Helper functions
# -----------------------------
 
def load_data(db_path=DB_PATH):
    """Load employee data from SQLite database"""
    conn = sqlite3.connect(str(db_path))
    df = pd.read_sql_query("SELECT * FROM employees", conn)
    conn.close()
    return df

def plot_nulls(df):
    null_counts = df.isnull().sum().reset_index()
    null_counts.columns = ["Column", "Nulls"]
    fig = px.bar(null_counts, x="Column", y="Nulls", color="Nulls",
                 title="Null Values per Column", text="Nulls")
    fig.show()

def plot_email_validity(df):
    df['Email_valid'] = df['Email'].str.contains(r'^[\w\.-]+@[\w\.-]+\.\w+$', regex=True)
    valid_count = df['Email_valid'].sum()
    invalid_count = (~df['Email_valid']).sum()
    fig = go.Figure(data=[go.Pie(
        labels=["Valid Emails", "Invalid Emails"],
        values=[valid_count, invalid_count],
        hole=0.4
    )])
    fig.update_layout(title_text="Email Validity Distribution")
    fig.show()

def plot_age_distribution(df):
    df['Age_status'] = df['Age'].apply(lambda x: 'Valid' if 18 <= x <= 60 else 'Invalid')
    fig = px.histogram(df, x="Age", color="Age_status", barmode="overlay",
                       title="Age Distribution (Valid vs Invalid)", nbins=20)
    fig.show()

def plot_salary_distribution(df):
    df['Salary_status'] = df['Salary'].apply(lambda x: 'Present' if pd.notnull(x) else 'Missing')
    fig = px.histogram(df, x="Salary", color="Salary_status", barmode="overlay",
                       title="Salary Distribution (Missing Highlighted)", nbins=20)
    fig.show()

def plot_join_date_distribution(df):
    fig = px.histogram(df, x="Join_Date", nbins=12, title="Employee Join Date Distribution")
    fig.show()

def plot_department_distribution(df):
    dept_counts = df['Department'].fillna("UNKNOWN").value_counts().reset_index()
    dept_counts.columns = ["Department", "Count"]
    fig = px.bar(dept_counts, x="Department", y="Count", color="Count",
                 title="Department Distribution")
    fig.show()

def calculate_data_quality(df):
    total_cells = df.size
    total_invalids = (~df['Email_valid']).sum() + df['Age_status'].value_counts().get('Invalid', 0) + df['Salary_status'].value_counts().get('Missing', 0)
    dq_score = 100 - (total_invalids / total_cells * 100)
    print(f"Data Quality Score: {dq_score:.2f}%")
    return dq_score

# -----------------------------
# 2️⃣ Main dashboard runner
# -----------------------------

def run_dashboard():
    df = load_data()
    plot_nulls(df)
    plot_email_validity(df)
    plot_age_distribution(df)
    plot_salary_distribution(df)
    plot_join_date_distribution(df)
    plot_department_distribution(df)
    calculate_data_quality(df)

# -----------------------------
# 3️⃣ Execute
# -----------------------------
if __name__ == "__main__":
    run_dashboard()