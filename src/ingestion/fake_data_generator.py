from faker import Faker
import pandas as pd
import random
from config.paths import RAW_DATA_PATH

fake = Faker()

class FakeDataGenerator:
    def __init__(self, num_records=1000):
        self.num_records = num_records

    def generate(self):
        data = []

        for _ in range(self.num_records):
            record = {
                "Name": fake.name() if random.random() > 0.1 else None,
                "Email": fake.email() if random.random() > 0.2 else "invalid_email",
                "Age": random.choice([fake.random_int(18, 60), None, "unknown"]),
                "Salary": random.choice([fake.random_int(30000, 120000), "N/A", None]),
                "Join_Date": fake.date() if random.random() > 0.2 else "32-13-2020",
                "Department": random.choice(["HR", "IT", "Sales", "it", "Hr", None])
            }
            data.append(record)
        
        df = pd.DataFrame(data)

        df = pd.concat([df, df.sample(50)], ignore_index=True)

        return df
    
    def save(self, df, path=None):
        if path is None:
            path = RAW_DATA_PATH

        path.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(path, index=False)