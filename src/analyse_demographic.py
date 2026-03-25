# src/analyse_demographic.py

import pandas as pd
import matplotlib.pyplot as plt
from config import PROCESSED_DATA_DIR, OUTPUT_FIGURES_DIR, OUTPUT_TABLES_DIR

def analyse_demographic():
    df = pd.read_csv(PROCESSED_DATA_DIR / "demographic_clean.csv")

    # ---- DERIVE TOTAL DEMOGRAPHIC UPDATES ----
    df["total_demographic_updates"] = (
        df["demo_age_5_17"] +
        df["demo_age_17_"]
    )

    # ---- STATE-WISE SUMMARY ----
    state_summary = df.groupby("state")["total_demographic_updates"].sum().reset_index()
    state_summary.to_csv(
        OUTPUT_TABLES_DIR / "demographic_updates_by_state.csv",
        index=False
    )

    print("✅ Demographic analysis completed.")

if __name__ == "__main__":
    analyse_demographic()
