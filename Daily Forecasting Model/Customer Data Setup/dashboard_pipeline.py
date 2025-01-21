import pandas as pd
from pathlib import Path

import warnings
warnings.filterwarnings('ignore')

from utilities import retrieve_and_open_csv_files
from preprocess import sort_reg_data_setup, set_weeks, set_days, set_final

class DashboardPipeline:
    def __init__(self, data_path, banner_db, dashboard_setup, semester_key, 
                 first_day_enrollment, end_enrollment, first_day_class, last_day_year):
        self.data_path = Path(data_path)
        self.banner_db = banner_db
        self.dashboard_setup = dashboard_setup
        self.semester_key = semester_key
        self.first_day_enrollment = first_day_enrollment
        self.end_enrollment = end_enrollment
        self.first_day_class = first_day_class
        self.last_day_year = last_day_year
        self.majr_desc_d = None

    def load_major_descriptions(self):
        majr_desc = retrieve_and_open_csv_files(self.data_path, keyword='Major Description')
        self.majr_desc_d = dict(zip(majr_desc['MAJR'], majr_desc['MAJR_DESC']))
        self.majr_desc_d['0000'] = self.majr_desc_d.pop('0')

    def process_current_registration(self):
        sp25rsts = (retrieve_and_open_csv_files(self.data_path, keyword=f'{self.semester_key} Registration')
                    .rename(columns={'StudentID': 'ID'}))
        sp25stud = (retrieve_and_open_csv_files(self.data_path, keyword=f'{self.semester_key} Enrollment')
                    .rename(columns={'STDTNO': 'ID'})[['ID', 'STYP', 'MAJR']])
        sp25 = sort_reg_data_setup(sp25rsts)
        sp25_wks = set_weeks(sp25, self.first_day_enrollment, self.end_enrollment, self.first_day_class)
        sp25_days = set_days(sp25_wks, self.first_day_enrollment, self.end_enrollment, self.first_day_class, self.last_day_year)
        sp25_final = (set_final(sp25_days, sp25stud, self.majr_desc_d)
                      .assign(TERMID=lambda df: df['TERM'].astype(str) + df['ID'])
                      [['TERM', 'ID', 'TERMID', 'PRESENT', 'WEEK', 'WEEK_NUM', 'MONTH', 'DAY',
                        'STYP', 'MAJR', 'MAJR_DESC', 'AGE', 'AGE_RANGE', 'RESD', 'RSTS', 
                        'RSTSDATE', 'ACTIVITYDATE']])
        sp25_final.to_excel(f'{self.data_path.parent}/Files/{self.dashboard_setup}', index=False, header=True)
        return sp25_final

    def update_banner_data(self, sp25_final):
        banner = (retrieve_and_open_csv_files(self.data_path.parents[1]/'Banner SQL', keyword=self.banner_db)
                  [['STUDID', 'STYPE', 'MAJR']].rename(columns={'STUDID': 'ID'}))
        combined = (sp25_final.merge(banner, on='ID', how='left')
                    .drop(['STYP', 'MAJR_x'], axis=1)
                    .rename(columns={'MAJR_y': 'MAJR'})
                    [['TERM', 'ID', 'TERMID', 'PRESENT', 'WEEK', 'WEEK_NUM', 'MONTH', 'DAY',
                      'STYPE', 'MAJR', 'MAJR_DESC', 'AGE', 'AGE_RANGE', 'RESD', 'RSTS', 
                      'RSTSDATE', 'ACTIVITYDATE']])
        combined['MAJR_DESC'] = [self.majr_desc_d.get(major) for major in combined['MAJR']]
        combined.to_excel(f'{self.data_path.parent}/Files/{self.dashboard_setup}', index=False, header=True)
        return combined

    def update_student_data(self, combined):
        combined = combined[['TERMID', 'STYPE', 'MAJR', 'MAJR_DESC']]
        student_data = retrieve_and_open_csv_files(self.data_path, keyword='SP21-SP25 Student Data')
        student_data['term'] = [i[:6] for i in student_data['TERMID']]
        search_terms = student_data['term'].unique()[:4]
        pattern = '|'.join(search_terms)
        filtered = student_data[student_data['TERMID'].str.contains(pattern, regex=True)]
        new_student_data = (pd.concat([filtered, combined])
                            .drop_duplicates('TERMID')
                            .drop('term', axis=1))
        new_student_data.to_csv(f'{self.data_path}/SP21-SP25 Student Data.csv', index=False)

    def run_pipeline(self):
        self.load_major_descriptions()
        sp25_final = self.process_current_registration()
        combined = self.update_banner_data(sp25_final)
        self.update_student_data(combined)
