# pipeline_steps.py

from sklearn.base import BaseEstimator, TransformerMixin

# Import processing functions
from data_cleaning import (
    load_csv_files,
    record_retention,
    remove_missing_gpa,
    combine_enrolled_and_gpa,
    clean_demographic_data,
    online_classes,
    pell_grant_cleansing,
    hs_matriculation_feature
)

# Define the pipeline step classes here
class LoadCSVFiles(BaseEstimator, TransformerMixin):
    def __init__(self, folder_path):
        self.folder_path = folder_path

    def fit(self, X=None, y=None):
        return self

    def transform(self, X=None):
        return load_csv_files(self.folder_path)

class RecordRetention(BaseEstimator, TransformerMixin):
    def __init__(self, semesters, years):
        self.semesters = semesters
        self.years = years

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return record_retention(X, semesters=self.semesters, years=self.years)

class RemoveMissingGPA(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return remove_missing_gpa(X)

class CombineEnrolledAndGPA(BaseEstimator, TransformerMixin):
    def __init__(self, gpa_data):
        self.gpa_data = gpa_data

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return combine_enrolled_and_gpa(X, self.gpa_data)

class CleanDemographicData(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return clean_demographic_data(X)

class OnlineClasses(BaseEstimator, TransformerMixin):
    def __init__(self, crhr_data):
        self.crhr_data = crhr_data

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return online_classes(self.crhr_data, X)

class PellGrantCleansing(BaseEstimator, TransformerMixin):
    def __init__(self, pell_data):
        self.pell_data = pell_data

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return pell_grant_cleansing(self.pell_data, X)

class HSMatriculationFeature(BaseEstimator, TransformerMixin):
    def __init__(self, hs_data):
        self.hs_data = hs_data

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return hs_matriculation_feature(self.hs_data, X)

