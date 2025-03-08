import pandas as pd
import csv
import re
import unicodedata

# Function for reading CSV File
def read_csv(file_path):
    if file_path.name.endswith('.csv'):
        df = pd.read_csv(file_path, delimiter=",", encoding='utf-8', index_col=0)
    elif file_path.name.endswith('.xlsx') or file_path.name.endswith('.xls'):
        df = pd.read_excel(file_path, delimiter=";", encoding='utf-8', index_col=0)
    else:
        raise ValueError("Format doesn't supported. Please upload the file with correct format")

    return df
