# DataSummary.py modification
from flask import jsonify
from controllers import Data_Analysis as da
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))


def data_summary():
    # Adjust the file path as necessary
    file_path = "C:/Users/vbodavul/Downloads/archive (2)/merged_and_cleaned_tripdata.csv"
    metrics_by_type = da.calculate_metrics_by_type(file_path)
    return jsonify(metrics_by_type)

