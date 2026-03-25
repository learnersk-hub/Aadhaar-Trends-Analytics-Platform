# src/analyse_enrolment.py

import pandas as pd
import matplotlib.pyplot as plt
from config import PROCESSED_DATA_DIR, OUTPUT_FIGURES_DIR, OUTPUT_TABLES_DIR

def analyse_enrolment():
    df = pd.read_csv(PROCESSED_DATA_DIR / "enrolment_clean.csv")

    # ---- DERIVE TOTAL ENROLMENTS ----
    df["total_enrolments"] = (
        df["age_0_5"] +
        df["age_5_17"] +
        df["age_18_greater"]
    )

    # ---- STATE-WISE SUMMARY ----
    state_summary = df.groupby("state")["total_enrolments"].sum().reset_index()
    state_summary.to_csv(
        OUTPUT_TABLES_DIR / "enrolment_by_state.csv",
        index=False
    )

    # ---- TIME TREND ----
    df["date"] = pd.to_datetime(
    df["date"],
    dayfirst=True,
    errors="coerce"
)

    time_trend = df.groupby(df["date"].dt.to_period("M"))["total_enrolments"].sum()

    plt.figure()
    time_trend.plot()
    plt.title("Aadhaar Enrolment Trend Over Time")
    plt.xlabel("Time")
    plt.ylabel("Total Enrolments")
    plt.tight_layout()
    plt.savefig(OUTPUT_FIGURES_DIR / "enrolment_trend.png")
    plt.close()

    print("✅ Enrolment analysis completed.")

if __name__ == "__main__":
    analyse_enrolment()
