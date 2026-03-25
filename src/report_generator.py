# src/report_generator.py

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
import pandas as pd


def generate_pdf_report(df: pd.DataFrame, output_path: str):
    """
    Generate an executive PDF report from Aadhaar integrated indicators.

    Parameters
    ----------
    df : pd.DataFrame
        Integrated Aadhaar indicators dataframe
    output_path : str
        Output PDF file path
    """

    # ---------------- SAFE COPY ----------------
    df = df.copy()

    # ---------------- DERIVED METRIC ----------------
    # System Health Score (computed safely if missing)
    if "system_health_score" not in df.columns:
        df["system_health_score"] = (
            100 - (40 * df["update_burden_index"])
        ).clip(0, 100)

    # ---------------- PDF SETUP ----------------
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()
    story = []

    # =========================
    # TITLE
    # =========================
    story.append(
        Paragraph(
            "<b>UIDAI Aadhaar Trends Analysis Report</b>",
            styles["Title"]
        )
    )
    story.append(Spacer(1, 0.3 * inch))

    # =========================
    # EXECUTIVE SUMMARY
    # =========================
    story.append(Paragraph("<b>Executive Summary</b>", styles["Heading2"]))
    story.append(
        Paragraph(
            """
            This report presents analytical insights derived from Aadhaar enrolment,
            biometric update, and demographic update datasets. The analysis focuses on
            identifying societal trends, operational anomalies, and system-level stress
            indicators to support informed decision-making and improvements within UIDAI.
            """,
            styles["BodyText"]
        )
    )
    story.append(Spacer(1, 0.25 * inch))

    # =========================
    # KEY NATIONAL METRICS
    # =========================
    story.append(Paragraph("<b>Key National Metrics</b>", styles["Heading2"]))

    total_enrolments = int(df["total_enrolments"].sum())
    total_bio = int(df["total_biometric_updates"].sum())
    total_demo = int(df["total_demographic_updates"].sum())
    avg_ubi = df["update_burden_index"].mean()
    avg_health = df["system_health_score"].mean()

    metrics_table = [
        ["Metric", "Value"],
        ["Total Enrolments (All States)", f"{total_enrolments:,}"],
        ["Total Biometric Updates", f"{total_bio:,}"],
        ["Total Demographic Updates", f"{total_demo:,}"],
        ["Average Update Burden Index", f"{avg_ubi:.3f}"],
        ["Average System Health Score", f"{avg_health:.1f}"],
    ]

    table = Table(metrics_table, colWidths=[3.4 * inch, 2.0 * inch])
    story.append(table)
    story.append(Spacer(1, 0.3 * inch))

    # =========================
    # KEY ANOMALIES
    # =========================
    story.append(Paragraph("<b>Key Anomalies Identified</b>", styles["Heading2"]))

    top_anomalies = df.sort_values(
        "update_burden_index", ascending=False
    ).head(5)

    for _, row in top_anomalies.iterrows():
        story.append(
            Paragraph(
                f"• <b>{row['state']}</b> shows a high update burden relative to "
                f"enrolment volume, indicating elevated operational maintenance demand.",
                styles["BodyText"]
            )
        )

    story.append(Spacer(1, 0.25 * inch))

    # =========================
    # POLICY IMPLICATIONS
    # =========================
    story.append(Paragraph("<b>Policy & System Implications</b>", styles["Heading2"]))
    story.append(
        Paragraph(
            """
            • High update burden states should be prioritized for infrastructure
              strengthening and additional staffing.<br/>
            • Regions with stable enrolment but frequent updates indicate mature Aadhaar
              penetration and require system optimization rather than outreach.<br/>
            • Continuous monitoring of normalized indicators enables early detection
              of operational stress and proactive intervention.
            """,
            styles["BodyText"]
        )
    )

    story.append(Spacer(1, 0.25 * inch))

    # =========================
    # METHODOLOGY (BRIEF)
    # =========================
    story.append(Paragraph("<b>Methodology Overview</b>", styles["Heading2"]))
    story.append(
        Paragraph(
            """
            The analysis aggregates age-segmented enrolment and update records at the
            state level. Derived indicators normalize update activity against enrolment
            volume to enable fair cross-state comparison. The System Health Score is a
            composite indicator designed to summarize system stability and stress.
            """,
            styles["BodyText"]
        )
    )

    # ---------------- BUILD PDF ----------------
    doc.build(story)
