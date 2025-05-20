import pandas as pd
from io import StringIO

def parse_csv(file_storage):
    df = pd.read_csv(file_storage)
    return df
