import numpy as np
import pandas as pd
import json
from Python_Runner.HCTSAAnalysis import HCTSAAnalysis

class PatientData:
    def __init__(self, patient_id, config, interval_length):
        self.patient_id = patient_id
        self.patient_path = f"/patient_{patient_id}/data.csv"
        self.config = config
        self.interval_length = interval_length
        self.full_data = pd.read_csv(self.patient_path)
        self.series_data = None
        self.imputed_intervals = None
        self.non_imputed_intervals = None

    def prepare_data(self):
        """Impute data and split into intervals."""
        self.full_data['time'] = pd.to_datetime(self.full_data['time'], unit='s')
        self.full_data.set_index('time', inplace=True)
        self.series_data = self.impute_data(self.full_data)
        self.imputed_intervals, self.non_imputed_intervals = self.split_data(self.interval_length)

    def impute_data(self, data):
        """Impute missing data with a consistent frequency of 2 seconds."""
        expected_frequency = '2S'  # Expected interval of 2 seconds
        return data.resample(expected_frequency).ffill()

    def split_data(self, interval_length):
        """Split data into specified intervals."""
        interval_count = int(np.ceil(self.series_data.index.max().timestamp() - self.series_data.index.min().timestamp()) / interval_length)
        imputed_intervals = {}
        non_imputed_intervals = {}
        start_time = self.series_data.index.min()
        for i in range(interval_count):
            end_time = start_time + pd.Timedelta(seconds=interval_length)
            imputed_interval_data = self.series_data[(self.series_data.index >= start_time) & (self.series_data.index < end_time)]
            non_imputed_interval_data = self.full_data[(self.full_data.index >= start_time) & (self.full_data.index < end_time)]
            if not imputed_interval_data.empty:
                imputed_intervals[end_time] = imputed_interval_data
                non_imputed_intervals[end_time] = non_imputed_interval_data
            start_time = end_time
        return imputed_intervals, non_imputed_intervals

    def analyze_and_save(self):
        """Analyze each interval and save results."""
        self.prepare_data()
        for idx, (end_time, interval) in enumerate(self.imputed_intervals.items()):
            analysis = HCTSAAnalysis(self.config)
            results = analysis.run_analysis(interval)
            filename = f"patient_{self.patient_id}_interval_{idx+1}_results.json"
            with open(filename, 'w') as file:
                json.dump(results, file, indent=4)
            print(f"Results for Patient {self.patient_id}, Interval {idx+1} saved to {filename}")



