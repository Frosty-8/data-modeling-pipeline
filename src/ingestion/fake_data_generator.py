from faker import Faker
import pandas as pd
import random
from datetime import datetime, timedelta
from config.paths import RAW_DATA_PATH

fake = Faker()

class FakeDataGenerator:
    def __init__(self, num_records=1000):
        self.num_records = num_records

    def _generate_department(self, age, salary, experience):
        """
        Create REALISTIC patterns so ML model can learn
        """

        # Core logic (learnable patterns)
        if salary is not None:
            if salary > 90000:
                return "IT"
            elif salary > 60000:
                return "SALES"
            else:
                return "HR"

        # Fallback using experience
        if experience is not None:
            if experience > 8:
                return "IT"
            elif experience > 3:
                return "SALES"

        return "HR"

    def generate(self):
        data = []

        for _ in range(self.num_records):

            # ---------------- CLEAN BASE VALUES ---------------- #
            age = random.randint(18, 60)
            salary = random.randint(30000, 120000)

            join_date = fake.date_between(start_date='-10y', end_date='today')
            experience = (datetime.now().date() - join_date).days / 365

            department = self._generate_department(age, salary, experience)

            record = {
                "Name": fake.name(),
                "Email": fake.email(),
                "Age": age,
                "Salary": salary,
                "Join_Date": join_date,
                "Department": department
            }

            # ---------------- ADD NOISE (REALISTIC) ---------------- #

            # Missing values
            if random.random() < 0.1:
                record["Name"] = None

            if random.random() < 0.15:
                record["Email"] = "invalid_email"

            if random.random() < 0.1:
                record["Age"] = random.choice([None, "unknown"])

            if random.random() < 0.1:
                record["Salary"] = random.choice([None, "N/A"])

            if random.random() < 0.1:
                record["Join_Date"] = "32-13-2020"

            # Dirty categorical values
            if random.random() < 0.1:
                record["Department"] = random.choice(
                    ["it", "Hr", "sales", None]
                )

            data.append(record)

        df = pd.DataFrame(data)

        # ---------------- DUPLICATES ---------------- #
        df = pd.concat([df, df.sample(int(0.05 * len(df)))], ignore_index=True)

        return df

    def save(self, df, path=None):
        if path is None:
            path = RAW_DATA_PATH

        path.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(path, index=False)