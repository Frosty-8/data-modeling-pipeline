from src.ingestion.fake_data_generator import FakeDataGenerator
from src.cleaning.data_cleaner import DataCleaner
from src.validation.data_validator import DataValidator
from src.utils.logger import setup_logger
from src.database.db_handler import DatabaseHandler
from src.utils.config_loader import ConfigLoader

from src.feature_engineering.feature_builder import FeatureBuilder
from src.models.train import Trainer
from src.analysis.sql_analysis import SQLAnalyzer
from config.paths import PROCESSED_DATA_PATH

from src.models.evaluate import evaluate
from src.models.predict import predict
import joblib
import os

class DataPipeline:
    def __init__(self):
        self.logger = setup_logger()
        self.config = ConfigLoader().config

    def run(self):
        config_loader = ConfigLoader()
        
        self.logger.info("Pipeline started.....")

        generator = FakeDataGenerator(1000)
        raw_df = generator.generate()
        generator.save(raw_df)
        self.logger.info("Data generated......")

        cleaner = DataCleaner(raw_df)
        clean_df = (
            cleaner.clean_names()
                   .clean_email()
                   .clean_age()
                   .clean_salary()
                   .clean_dates()
                   .clean_department()
                   .remove_duplicates()
                   .get_clean_data()
        )

        self.logger.info("Data cleaned.....")
        
        data_config = config_loader.get("data")
        validation_config = config_loader.get("validation")

        validator = DataValidator(clean_df, validation_config)
        report = validator.run_all()

        self.logger.info(f"Validation Errors: {report['errors']}")
        self.logger.info(f"Data Quality scores: {report['quality_score']}%")

        self.logger.info("Saving the data to Processed directory")
        clean_df.to_csv(PROCESSED_DATA_PATH)

        db = DatabaseHandler()
        db.save(clean_df)
        self.logger.info("Data saved to database")

        self.logger.info("✅ Pipeline executed successfully!")
        self.logger.info(f"✅ Pipeline done | Quality Score: {report['quality_score']}%")

        self.logger.info("Feature engineering")
        # Step 1: Separate target FIRST (clean separation)
        target_col = "Department"
        y = clean_df[target_col]

        X_raw = clean_df.drop(columns=[target_col])

        # Step 2: Apply feature engineering ONLY on X
        builder = FeatureBuilder(X_raw)

        X = (
            builder.create_features()
                .encode()
                .get_data()
        )

        print(y.value_counts())

        # ---------------- TRAIN ---------------- #
        self.logger.info("Training model")
        trainer = Trainer(X,y)
        model, X_test, y_test = trainer.train()

        # ---------------- EVALUATE ---------------- #
        self.logger.info("Evaluating model")
        metrics = evaluate(model, X_test, y_test)

        self.logger.info(f"Model Accuracy: {metrics['accuracy']}")
        self.logger.info(f"Classification Report:\n{metrics['report']}")

        # ---------------- PREDICT ---------------- #
        self.logger.info("Running sample predictions")

        sample_input = X_test.head(5)
        predictions = predict(model, sample_input)

        self.logger.info(f"Sample Predictions: {predictions}")

        # ---------------- SAVE PREDICTIONS TO DB ---------------- #
        self.logger.info("Saving predictions to database")

        pred_df = X_test.copy()
        pred_df["Actual"] = y_test.values
        pred_df["Predicted"] = model.predict(X_test)

        db.save(pred_df, table_name="predictions")

        self.logger.info("Predictions saved to database")

        # ---------------- SAVE MODEL ---------------- #
        self.logger.info("Saving model")

        os.makedirs("artifacts", exist_ok=True)
        joblib.dump(model, "artifacts/model.pkl")

        self.logger.info("Model saved successfully")

        # ---------------- SQL Analysis ---------------- #
        self.logger.info("SQL Analysis")

        analyzer = SQLAnalyzer(db)
        print(analyzer.accuracy())
        print(analyzer.confusion_matrix())