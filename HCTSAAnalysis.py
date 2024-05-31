import numpy as np
import pandas as pd
import json
import pyarrow.parquet as pq
from operations_map import OPERATIONS_MAP

class HCTSAAnalysis:
    def __init__(self, config):
        self.config = config

    def run_analysis(self, series):
        results = {}
        for func_name, param_sets in self.config.items():
            func = OPERATIONS_MAP.get(func_name)
            if func:
                if isinstance(param_sets, list):
                    for params in param_sets:
                        param_str = '_'.join(f"{k}_{v}" for k, v in params.items())
                        result_key = f"{func_name}_{param_str}"
                        try:
                            results[result_key] = func(series, **params)
                        except Exception as e:
                            results[result_key] = np.nan  # Use np.nan for errors
                else:
                    try:
                        results[func_name] = func(series, **param_sets)
                    except Exception as e:
                        results[func_name] = np.nan  # Use np.nan for errors
                        print(func_name)
                        print(f"Error: {str(e)}")
            else:
                results[func_name] = np.nan  # Use np.nan for missing functions
        return results

def load_config(path):
    with open(path, 'r') as file:
        return json.load(file)

def flatten_dict(d, parent_key='', sep='_'):
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)

# Load configuration
config_path = 'config.json'
config = load_config(config_path)

# Read parquet file
input_file = 'initial_tests.parquet'
df = pd.read_parquet(input_file)

# Separate the columns to be processed and the columns to be included in the final output
unprocessed_columns = df.iloc[:, :3]
processed_columns = df.iloc[:, 3:303]

# Initialize the analysis class
analysis = HCTSAAnalysis(config)

# Process each series in the processed_columns DataFrame
all_results = []
for index, row in processed_columns.iterrows():
    series = row.to_numpy()  # Assuming each row is a series
    results = analysis.run_analysis(series)
    results['index'] = index  # Add the index to the results for reference
    flattened_results = flatten_dict(results)  # Flatten the results dictionary
    all_results.append(flattened_results)

# Convert the flattened results to a DataFrame
results_df = pd.DataFrame(all_results)

# Merge the unprocessed columns with the results
final_df = pd.concat([unprocessed_columns.reset_index(drop=True), results_df], axis=1)

# # Save the final DataFrame to a new parquet file
# output_parquet_file = 'analysis_results.parquet'
# final_df.to_parquet(output_parquet_file, index=False)

# Save the final DataFrame to a CSV file
output_csv_file = 'analysis_results.csv'
final_df.to_csv(output_csv_file, index=False)
