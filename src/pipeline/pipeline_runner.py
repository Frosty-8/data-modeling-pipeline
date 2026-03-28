from src.ingestion.fake_data_generator import FakeDataGenerator
from src.cleaning.data_cleaner import DataCleaner
from src.validation.data_validator import DataValidator
from src.utils.logger import setup_logger
from src.database.db_handler import DatabaseHandler
from src.utils.config_loader import ConfigLoader

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


        db = DatabaseHandler()
        db.save(clean_df)
        self.logger.info("Data saved to database")

        self.logger.info("✅ Pipeline executed successfully!")
        self.logger.info(f"✅ Pipeline done | Quality Score: {report['quality_score']}%")