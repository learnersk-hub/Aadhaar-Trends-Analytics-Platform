# app/app.py
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

import streamlit as st
import pandas as pd
from pathlib import Path
import tempfile

from src.report_generator import generate_pdf_report

# ---------------- CONFIG ----------------
BASE_DIR = Path(__file__).resolve().parent.parent
TABLES_DIR = BASE_DIR / "outputs" / "tables"
FIGURES_DIR = BASE_DIR / "outputs" / "figures"

st.set_page_config(
    page_title="Aadhaar Trends Analysis",
    layout="wide"
)

# ---------------- LOAD DATA ----------------
integrated_df = pd.read_csv(TABLES_DIR / "integrated_indicators.csv")
enrolment_state_df = pd.read_csv(TABLES_DIR / "enrolment_by_state.csv")
biometric_state_df = pd.read_csv(TABLES_DIR / "biometric_updates_by_state.csv")
demographic_state_df = pd.read_csv(TABLES_DIR / "demographic_updates_by_state.csv")

# ---------------- TITLE ----------------
st.title("Unlocking Societal Trends in Aadhaar Enrolment & Updates")

st.markdown(
    """
This dashboard presents **analytical insights derived from UIDAI Aadhaar enrolment,
biometric update, and demographic update datasets**.
The focus is on identifying **patterns, trends, anomalies, and operational indicators**
to support **informed administrative decision-making**.
"""
)

# ---------------- SIDEBAR ----------------
st.sidebar.header("Analysis Controls")

selected_state = st.sidebar.selectbox(
    "Select State for Deep Dive",
    sorted(integrated_df["state"].unique())
)

# =========================
# SECTION 1: EXECUTIVE SUMMARY
# =========================
st.header("1️⃣ National Overview")

col1, col2, col3 = st.columns(3)

col1.metric(
    "Total Enrolments (All States)",
    f"{int(integrated_df['total_enrolments'].sum()):,}"
)

col2.metric(
    "Total Biometric Updates",
    f"{int(integrated_df['total_biometric_updates'].sum()):,}"
)

col3.metric(
    "Total Demographic Updates",
    f"{int(integrated_df['total_demographic_updates'].sum()):,}"
)

st.markdown(
    """
**Interpretation:**  
This overview reflects the overall scale of Aadhaar enrolment coverage and the
ongoing data maintenance demand across the country.
"""
)

# ---------------- PDF EXPORT (NEW) ----------------
st.subheader("📄 Export Executive Report")

if st.button("Generate Executive PDF Report"):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        generate_pdf_report(integrated_df, tmp.name)

        st.success("Executive PDF report generated successfully.")

        with open(tmp.name, "rb") as f:
            st.download_button(
                label="Download PDF Report",
                data=f,
                file_name="UIDAI_Aadhaar_Trends_Analysis_Report.pdf",
                mime="application/pdf"
            )

# =========================
# SECTION 2: ENROLMENT PATTERNS
# =========================
st.header("2️⃣ Enrolment Patterns (State-wise)")

st.dataframe(
    enrolment_state_df.sort_values(
        "total_enrolments", ascending=False
    ),
    use_container_width=True
)

if (FIGURES_DIR / "enrolment_trend.png").exists():
    st.image(
        str(FIGURES_DIR / "enrolment_trend.png"),
        caption="Time-wise Aadhaar Enrolment Trend"
    )

st.markdown(
    """
**Key Insight:**  
Enrolment volumes vary significantly across states, reflecting population size,
awareness levels, and access to enrolment infrastructure.
"""
)

# =========================
# SECTION 3: UPDATE BEHAVIOUR
# =========================
st.header("3️⃣ Update Behaviour & Operational Load")

col4, col5 = st.columns(2)

with col4:
    st.subheader("Biometric Updates")
    st.dataframe(
        biometric_state_df.sort_values(
            "total_biometric_updates", ascending=False
        ),
        use_container_width=True
    )

with col5:
    st.subheader("Demographic Updates")
    st.dataframe(
        demographic_state_df.sort_values(
            "total_demographic_updates", ascending=False
        ),
        use_container_width=True
    )

st.markdown(
    """
**Interpretation:**  
High update volumes indicate continuous interaction of citizens with the Aadhaar system,
highlighting regions that may require additional operational capacity.
"""
)

# =========================
# SECTION 4: ANOMALY DETECTION
# =========================
st.header("4️⃣ Anomaly Detection via Normalized Indicator")

st.markdown(
    """
To detect anomalies beyond raw counts, a **normalized indicator** is used:
"""
)

st.code(
    "Update Burden Index = (Biometric Updates + Demographic Updates) / Total Enrolments"
)

st.dataframe(
    integrated_df.sort_values(
        "update_burden_index", ascending=False
    ),
    use_container_width=True
)

st.markdown(
    """
**How anomalies are identified:**  
States with a significantly higher **Update Burden Index** exhibit
disproportionately high update activity relative to enrolment volume.
These represent **operational stress zones** rather than population-driven effects.
"""
)

# =========================
# SECTION 5: STATE DEEP DIVE
# =========================
st.header("5️⃣ State-Level Deep Dive")

state_row = integrated_df[integrated_df["state"] == selected_state].iloc[0]

col6, col7, col8, col9 = st.columns(4)

col6.metric("State", selected_state)
col7.metric("Total Enrolments", f"{int(state_row['total_enrolments']):,}")
col8.metric(
    "Total Updates",
    f"{int(state_row['total_biometric_updates'] + state_row['total_demographic_updates']):,}"
)
col9.metric("Update Burden Index", f"{state_row['update_burden_index']:.3f}")

st.markdown(
    """
**Interpretation:**  
This state-level view helps administrators understand whether the region’s Aadhaar
ecosystem is enrolment-driven or maintenance-heavy.
"""
)

# =========================
# SECTION 6: POLICY IMPLICATIONS
# =========================
st.header("6️⃣ Policy & System Implications")

st.markdown(
    """
Based on observed patterns and anomalies, the analysis supports the following actions:

- **High Update Burden States:**  
  Prioritize infrastructure strengthening and staff allocation.

- **Low Enrolment Regions:**  
  Targeted enrolment awareness and outreach programs.

- **Temporal Spikes in Updates:**  
  Investigate policy changes, data corrections, or system-level disruptions.

- **Lifecycle Behaviour Insights:**  
  Align Aadhaar services with citizen mobility and demographic transitions.
"""
)

# ---------------- FOOTER ----------------
st.markdown("---")
st.markdown(
    """
**Note:**  
This dashboard is a **read-only analytical layer** built on reproducible,
UIDAI-provided datasets and derived indicators.  
It complements the core analysis pipeline and is intended for insight exploration
rather than raw data modification.
"""
)
