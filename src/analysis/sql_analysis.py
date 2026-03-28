class SQLAnalyzer:
    def __init__(self, db):
        self.db = db

    def accuracy(self):
        query = """
        SELECT 
            ROUND(
                SUM(CASE WHEN Actual = Predicted THEN 1 ELSE 0 END) * 1.0 / COUNT(*), 2
            ) AS accuracy
        FROM predictions;
        """
        return self.db.run_query(query)

    def confusion_matrix(self):
        query = """
        SELECT Actual, Predicted, COUNT(*) as count
        FROM predictions
        GROUP BY Actual, Predicted
        ORDER BY Actual;
        """
        return self.db.run_query(query)