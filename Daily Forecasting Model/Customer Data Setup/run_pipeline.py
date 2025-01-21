from dashboard_pipeline import DashboardPipeline
from pathlib import Path

# Define a function to initialize and run the pipeline
def main_pipeline():
    # Parameters
    DATA_PATH = Path.cwd()/'Data'
    BANNER_DB = 'SP25_STYPE.csv'
    DASHBOARD_SETUP = '202510 Python Dashboard Setup.xlsx'
    SEMESTER_KEY = '202510'
    FIRST_DAY_ENROLLMENT = '2024-10-16'
    END_ENROLLMENT = '2025-04-30'
    FIRST_DAY_CLASS = '2025-01-21'
    LAST_DAY_YEAR = '2024-12-31'

    # Initialize the pipeline
    pipeline = DashboardPipeline(
        data_path=DATA_PATH,
        banner_db=BANNER_DB,
        dashboard_setup=DASHBOARD_SETUP,
        semester_key=SEMESTER_KEY,
        first_day_enrollment=FIRST_DAY_ENROLLMENT,
        end_enrollment=END_ENROLLMENT,
        first_day_class=FIRST_DAY_CLASS,
        last_day_year=LAST_DAY_YEAR
    )
    
    # Run the pipeline
    pipeline.run_pipeline()

# Ensure it can be executed directly as a script
if __name__ == "__main__":
    main_pipeline()
