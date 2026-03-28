import pandas as pd

class FeatureBuilder:
    def __init__(self, df):
        self.df = df.copy()

    def create_features(self):
        self.df['experience_years'] = (
            pd.Timestamp.now() - self.df['Join_Date']
        ).dt.days / 365

        self.df = self.df.drop(columns=['Join_Date'])
        
        return self   # ✅ return self

    def encode(self):
        categorical_cols = self.df.select_dtypes(include=['object']).columns
        self.df = pd.get_dummies(self.df, columns=categorical_cols)
        return self

    def get_data(self):
        return self.df
    
    def split_target(self, target_col):
        y = self.df[target_col]
        self.df = self.df.drop(columns=[target_col])
        return self, y