import re

class DataValidator:
    def __init__(self, df, config):
        self.df = df
        self.config = config
        self.errors = []

    def validate_email(self):
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        invalid = self.df[~self.df['Email'].fillna("").str.match(pattern)]
        self.errors.append(("invalid_email", len(invalid)))

    def validate_age(self):
        min_age = self.config["age_min"]
        max_age = self.config["age_max"]

        invalid = self.df[
            (self.df['Age'] < min_age) | (self.df['Age'] > max_age)
        ]
        self.errors.append(("invalid_age", len(invalid)))

    def validate_salary(self):
        min_sal = self.config["salary_min"]
        max_sal = self.config["salary_max"]

        invalid = self.df[
            (self.df['Salary'] < min_sal) | (self.df['Salary'] > max_sal)
        ]
        self.errors.append(("invalid_salary", len(invalid)))

    def validate_nulls(self):
        nulls = self.df.isnull().sum().sum()
        self.errors.append(("total_nulls", int(nulls)))

    def generate_quality_score(self):
        total_rows = len(self.df)
        total_errors = sum(count for _, count in self.errors)

        score = max(0, 100 - (total_errors / (total_rows * len(self.df.columns))) * 100)
        return round(score, 2)

    def run_all(self):
        self.validate_email()
        self.validate_age()
        self.validate_salary()
        self.validate_nulls()

        return {
            "errors": self.errors,
            "quality_score": self.generate_quality_score()
        }