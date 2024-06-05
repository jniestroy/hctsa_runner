import pandas as pd
import numpy as np
import psycopg2

# Import custom operations from hctsa
from Operations.DN_Mean import DN_Mean
from Operations.DN_Median import DN_Median
from Operations.DN_STD import DN_STD

OPERATIONS_MAP = {
    'DN_Mean': DN_Mean,
    'DN_Median': DN_Median,
    'DN_STD': DN_STD
}

class DBDataLoader:
    def __init__(self, host, port, user, password, dbname):
        self.connection = psycopg2.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            dbname=dbname
        )
        self.cursor = self.connection.cursor()
        self.operations_config = {}

    def load_data(self, start_time, end_time, columns):
        query = f"""
        SELECT time, {', '.join(columns)}
        FROM sensor_data
        WHERE time BETWEEN '{start_time}' AND '{end_time}'
        """
        self.cursor.execute(query)
        data = pd.DataFrame(self.cursor.fetchall(), columns=['time'] + columns)
        return data

    def set_operations(self, operations_config):
        self.operations_config = operations_config

    def run_operations(self, data):
        results = {}
        # Map the string keys to actual function references

        for column in data.columns[1:]:  # Skip the time column
            column_results = {}
            for operation_name, params in self.operations_config.items():
                operation = OPERATIONS_MAP.get(operation_name)
                if operation:
                    try:
                        # Assuming each operation function can handle pandas Series and optional params
                        result = operation(data[column], **params)
                        column_results[operation_name] = result
                    except Exception as e:
                        column_results[operation_name] = f"Error: {str(e)}"
                else:
                    column_results[operation_name] = "Operation not found"
            results[column] = column_results
        return results


    def save_results(self, results):
        # Implement saving logic, potentially to another QuestDB table
        pass

    def close(self):
        self.connection.close()

class TimeSeriesSample:

    def __init__(self, data, legnth = 60, interval = 5):
        """
        data: pandas df hopefully of time length and time between rows of interval
        length: Length of total time sample in seconds normally 60
        interval: time between samples
        """
        self.legnth = legnth
        self.interval = interval
        self.rows = legnth // interval

        if data.nrows != self.rows:
            self.data = self.impute_ts(data)
    
    def impute_ts(self, data):
        """Fill in missing data such that the data goes from start to 
        """
        pass



# Example Usage
db_loader = DBDataLoader('localhost', 8812, 'admin', 'quest', 'qdb')
db_loader.set_operations({
    'DN_Mean': {},  
    'DN_STD': {},
    'DN_Median':{}  
})
data = db_loader.load_data('2024-04-16', '2024-04-17', ['tag1', 'tag2', 'tag3'])
results = db_loader.run_operations(data)
# db_loader.save_results(results)
# db_loader.close()
print(results)



# A loader that takes in all data from start to end datetimes

# A x minute ts data set sampled every x seconds upon which algorithms can be run

# A builder that can convert the full data set into y x minute samples stored somehwere in the loader