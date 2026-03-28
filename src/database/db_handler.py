from sqlalchemy import create_engine
import pandas as pd

class DatabaseHandler:
    def __init__(self, db_url="sqlite:///data/pipeline.db"):
        self.engine = create_engine(db_url)

    def save(self, df, table_name="employees"):
        df.to_sql(table_name, self.engine, if_exists='replace', index=False)
        
    def fetch_all(self, table_name="employees"):
        return pd.read_sql(f"SELECT * FROM {table_name}", self.engine)
    
    def run_query(self, query):
        return pd.read_sql(query, self.engine)