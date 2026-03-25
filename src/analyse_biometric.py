# src/analyse_biometric.py

import pandas as pd
import matplotlib.pyplot as plt
from config import PROCESSED_DATA_DIR, OUTPUT_FIGURES_DIR, OUTPUT_TABLES_DIR

def analyse_biometric():
    df = pd.read_csv(PROCESSED_DATA_DIR / "biometric_clean.csv")

    # ---- DERIVE TOTAL BIOMETRIC UPDATES ----
    df["total_biometric_updates"] = (
        df["bio_age_5_17"] +
        df["bio_age_17_"]
    )

    # ---- STATE-WISE SUMMARY ----
    state_updates = df.groupby("state")["total_biometric_updates"].sum().reset_index()
    state_updates.to_csv(
        OUTPUT_TABLES_DIR / "biometric_updates_by_state.csv",
        index=False
    )

    # ---- TOP STATES PLOT ----
    top_states = state_updates.sort_values(
        "total_biometric_updates", ascending=False
    ).head(10)

    plt.figure()
    plt.bar(top_states["state"], top_states["total_biometric_updates"])
    plt.xticks(rotation=45, ha="right")
    plt.title("Top States by Biometric Updates")
    plt.tight_layout()
    plt.savefig(OUTPUT_FIGURES_DIR / "biometric_top_states.png")
    plt.close()

    print("✅ Biometric analysis completed.")

if __name__ == "__main__":
    analyse_biometric()
