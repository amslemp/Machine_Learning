# main_pipeline.py
from sklearn.pipeline import Pipeline
from pathlib import Path
from pipeline_steps import (
    LoadCSVFiles,
    RecordRetention,
    RemoveMissingGPA,
    CombineEnrolledAndGPA,
    CleanDemographicData,
    OnlineClasses,
    PellGrantCleansing,
    HSMatriculationFeature
)
from data_cleaning import load_csv_files

def main():
    config = {
        "enrollment_folder": Path.cwd().parent / "Files/Enrollment",
        "gpa_folder": Path.cwd().parent / "Files/GPA and CrHrs",
        "pell_folder": Path.cwd().parent / "Files/Pell and Loan",
        "online_folder": Path.cwd().parent / "Files/Location",
        "high_school_folder": Path.cwd().parents[1] / "Enrollments/High School Enrollments/Files",
        "semesters": ['201980', '202080', '202180', '202280', '202380'],
        "years": [19, 20, 21, 22, 23],
        "output_path": Path("data/processed/FA19 - FA23 Demographic Cleaned Dataset.csv")
    }

    # Load supporting data (e.g., GPA, Pell, etc.)
    gpa_data = load_csv_files(config["gpa_folder"])
    pell_data = load_csv_files(config["pell_folder"])
    crhr_data = load_csv_files(config["online_folder"])
    hs_data = load_csv_files(config["high_school_folder"])

    # Define the pipeline
    pipeline = Pipeline([
        ("load_enrollment_data", LoadCSVFiles(config["enrollment_folder"])),
        ("record_retention", RecordRetention(config["semesters"], config["years"])),
        ("remove_missing_gpa", RemoveMissingGPA()),
        ("combine_enrolled_and_gpa", CombineEnrolledAndGPA(gpa_data)),
        ("clean_demographic_data", CleanDemographicData()),
        ("online_classes", OnlineClasses(crhr_data)),
        ("pell_grant_cleansing", PellGrantCleansing(pell_data)),
        ("hs_matriculation_feature", HSMatriculationFeature(hs_data))
    ])

    # Execute the pipeline
    final_dataset = pipeline.fit_transform(None)

    # Save the final dataset
    config["output_path"].parent.mkdir(parents=True, exist_ok=True)
    final_dataset.to_csv(config["output_path"], index=False)

if __name__ == "__main__":
    main()
