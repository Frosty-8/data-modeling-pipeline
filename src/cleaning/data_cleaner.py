import pandas as pd

class DataCleaner:
    def __init__(self, df):
        self.df = df.copy()

    def clean_names(self):
        self.df['Name'] = self.df['Name'].fillna("unknown")
        return self
    
    def clean_email(self):
        self.df['Email'] = self.df['Email'].apply(
            lambda x: x if isinstance(x, str) and "@" in x and "." in x else None
        )
        return self
    
    def clean_age(self):
        self.df['Age'] = pd.to_numeric(self.df['Age'], errors='coerce')
        self.df['Age'] = self.df['Age'].fillna(self.df['Age'].median())
        return self
    
    def clean_salary(self):
        self.df['Salary'] = pd.to_numeric(self.df['Salary'], errors='coerce')
        self.df['Salary']=self.df['Salary'].fillna(self.df['Salary'].mean())
        return self
    
    def clean_dates(self):
        self.df['Join_Date'] = pd.to_datetime(self.df['Join_Date'], errors='coerce', format="%Y-%m-%d")
        return self
    
    def clean_department(self):
        self.df['Department'] = self.df['Department'].str.upper()
        self.df['Department']=self.df['Department'].fillna("UNKNOWN")
        return self
    
    def remove_duplicates(self):
        self.df = self.df.drop_duplicates()
        return self
    
    def get_clean_data(self):
        return self.df