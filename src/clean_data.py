# src/clean_data.py

import pandas as pd
from load_data import (
    load_enrolment_data,
    load_biometric_data,
    load_demographic_data
)
from config import PROCESSED_DATA_DIR

def standardize_columns(df):
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )
    return df

def basic_cleaning(df):
    df = df.drop_duplicates()
    df = df.dropna(how="all")
    df = standardize_columns(df)
    return df

def clean_and_save():
    enrolment = basic_cleaning(load_enrolment_data())
    biometric = basic_cleaning(load_biometric_data())
    demographic = basic_cleaning(load_demographic_data())

    enrolment.to_csv(PROCESSED_DATA_DIR / "enrolment_clean.csv", index=False)
    biometric.to_csv(PROCESSED_DATA_DIR / "biometric_clean.csv", index=False)
    demographic.to_csv(PROCESSED_DATA_DIR / "demographic_clean.csv", index=False)

if __name__ == "__main__":
    clean_and_save()
