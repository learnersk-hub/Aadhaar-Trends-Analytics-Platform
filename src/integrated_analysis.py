# src/integrated_analysis.py

import pandas as pd
from config import PROCESSED_DATA_DIR, OUTPUT_TABLES_DIR

def integrated_analysis():
    enrol = pd.read_csv(PROCESSED_DATA_DIR / "enrolment_clean.csv")
    bio = pd.read_csv(PROCESSED_DATA_DIR / "biometric_clean.csv")
    demo = pd.read_csv(PROCESSED_DATA_DIR / "demographic_clean.csv")

    # ---- DERIVED TOTALS ----
    enrol["total_enrolments"] = (
        enrol["age_0_5"] +
        enrol["age_5_17"] +
        enrol["age_18_greater"]
    )

    bio["total_biometric_updates"] = (
        bio["bio_age_5_17"] +
        bio["bio_age_17_"]
    )

    demo["total_demographic_updates"] = (
        demo["demo_age_5_17"] +
        demo["demo_age_17_"]
    )

    # ---- STATE-LEVEL AGGREGATION ----
    enrol_state = enrol.groupby("state")["total_enrolments"].sum()
    bio_state = bio.groupby("state")["total_biometric_updates"].sum()
    demo_state = demo.groupby("state")["total_demographic_updates"].sum()

    integrated = pd.concat(
        [enrol_state, bio_state, demo_state],
        axis=1
    ).fillna(0)

    # ---- POLICY INDICATOR ----
    integrated["update_burden_index"] = (
        integrated["total_biometric_updates"] +
        integrated["total_demographic_updates"]
    ) / integrated["total_enrolments"]

    integrated.reset_index().to_csv(
        OUTPUT_TABLES_DIR / "integrated_indicators.csv",
        index=False
    )

    print("✅ Integrated analysis completed.")

if __name__ == "__main__":
    integrated_analysis()
