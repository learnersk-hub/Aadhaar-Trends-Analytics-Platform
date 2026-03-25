# src/load_data.py

import pandas as pd
from config import ENROLMENT_DIR, BIOMETRIC_DIR, DEMOGRAPHIC_DIR

def load_multiple_csv(folder_path):
    dfs = []
    for file in folder_path.glob("*.csv"):
        df = pd.read_csv(file)
        df["source_file"] = file.name
        dfs.append(df)
    return pd.concat(dfs, ignore_index=True)

def load_enrolment_data():
    return load_multiple_csv(ENROLMENT_DIR)

def load_biometric_data():
    return load_multiple_csv(BIOMETRIC_DIR)

def load_demographic_data():
    return load_multiple_csv(DEMOGRAPHIC_DIR)
