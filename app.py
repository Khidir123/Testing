import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random
import time
import io

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="FinOps Automation Suite | AGC",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# THEME
# ─────────────────────────────────────────────
BG      = "#F3F4F6"
CARD    = "#FFFFFF"
TEXT    = "#111827"
MUTED   = "#6B7280"
ACCENT  = "#7C6FF0"
ACCENT2 = "#F59E0B"
TEAL    = "#34D399"
BLUE    = "#60A5FA"
PINK    = "#F472B6"
RED     = "#EF4444"

CHART_COLORS = [ACCENT, ACCENT2, TEAL, BLUE, PINK]

PLOT_LAYOUT = dict(
    plot_bgcolor=CARD,
    paper_bgcolor=CARD,
    font_family="Inter",
    font_color=TEXT,
    margin=dict(t=20, b=30, l=0, r=0),
)

# ─────────────────────────────────────────────
# CSS  — sidebar is always visible
# ─────────────────────────────────────────────
st.markdown(
    f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {{
    font-family: 'Inter', sans-serif;
}}

.stApp {{
    background: {BG};
}}

.main .block-container {{
    padding-top: 1.5rem;
    max-width: 1450px;
}}

/* ── FORCE SIDEBAR ALWAYS VISIBLE ── */
section[data-testid="stSidebar"] {{
    display: flex !important;
    visibility: visible !important;
    width: 260px !important;
    min-width: 260px !important;
    max-width: 260px !important;
    transform: none !important;
    position: relative !important;
    background: {CARD} !important;
    border-right: 1px solid #E5E7EB;
    flex-shrink: 0 !important;
}}

section[data-testid="stSidebar"] > div {{
    width: 260px !important;
}}

/* Hide the collapse arrow button */
button[data-testid="collapsedControl"],
button[kind="header"] {{
    display: none !important;
}}

section[data-testid="stSidebar"] * {{
    color: {TEXT} !important;
}}

section[data-testid="stSidebar"] .stRadio label {{
    font-size: 0.9rem !important;
}}

/* ── Hero ── */
.hero-banner {{
    background: linear-gradient(135deg, #FFFFFF 0%, #F9FAFB 100%);
    border: 1px solid #E5E7EB;
    border-radius: 24px;
    padding: 1.5rem 1.75rem;
    margin-bottom: 1.4rem;
    box-shadow: 0 10px 30px rgba(17,24,39,0.06);
    position: relative;
    overflow: hidden;
}}
.hero-banner::after {{
    content: '⚖';
    position: absolute;
    right: 1.6rem;
    top: 50%;
    transform: translateY(-50%);
    font-size: 6.5rem;
    opacity: 0.05;
    color: {ACCENT};
}}
.hero-badge {{
    display: inline-block;
    background: rgba(124,111,240,0.10);
    color: {ACCENT} !important;
    border: 1px solid rgba(124,111,240,0.22);
    border-radius: 999px;
    padding: 4px 12px;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}}
.hero-title {{
    font-size: 2rem;
    font-weight: 800;
    color: {TEXT};
    margin: 0.55rem 0 0.2rem;
    letter-spacing: -0.03em;
}}
.hero-sub {{
    color: {MUTED};
    font-size: 0.92rem;
    margin: 0;
}}

/* ── KPI cards ── */
.kpi-card {{
    background: {CARD};
    border: 1px solid #E5E7EB;
    border-radius: 18px;
    padding: 1.15rem 1.2rem;
    box-shadow: 0 8px 24px rgba(17,24,39,0.05);
    height: 155px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}}
.kpi-icon  {{ font-size: 1.4rem; margin-bottom: 0.1rem; }}
.kpi-label {{ font-size: 0.72rem; color: #9CA3AF; text-transform: uppercase; letter-spacing: 0.09em; font-weight: 700; }}
.kpi-value {{ font-size: 1.95rem; font-weight: 800; color: {TEXT}; line-height: 1; margin: 0.2rem 0; }}
.kpi-delta-pos {{ color: #059669; font-size: 0.82rem; font-weight: 600; }}
.kpi-delta-neg {{ color: {RED};   font-size: 0.82rem; font-weight: 600; }}

/* ── Section headers ── */
.section-title {{ font-size: 1.15rem; font-weight: 800; color: {TEXT}; margin-bottom: 0.15rem; }}
.section-sub   {{ font-size: 0.85rem; color: {MUTED}; margin-bottom: 0.95rem; }}

/* ── Badges ── */
.badge-pass {{ background:#D1FAE5; color:#065F46; padding:2px 11px; border-radius:999px; font-size:0.76rem; font-weight:700; }}
.badge-fail {{ background:#FEE2E2; color:#991B1B; padding:2px 11px; border-radius:999px; font-size:0.76rem; font-weight:700; }}
.badge-warn {{ background:#FEF3C7; color:#92400E; padding:2px 11px; border-radius:999px; font-size:0.76rem; font-weight:700; }}

/* ── Anomaly rows ── */
.anomaly-row {{
    background: #FFFBEB;
    border-left: 4px solid {ACCENT2};
    border-radius: 0 12px 12px 0;
    padding: 0.8rem 1rem;
    margin-bottom: 0.55rem;
    font-size: 0.88rem;
    color: {TEXT};
    border: 1px solid #FDE68A;
    border-left-width: 4px;
}}

hr {{ border: none; border-top: 1px solid #E5E7EB; margin: 1.5rem 0; }}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {{
    gap: 6px;
    background: #E5E7EB;
    border-radius: 14px;
    padding: 4px;
}}
.stTabs [data-baseweb="tab"] {{
    border-radius: 10px;
    padding: 7px 16px;
    font-size: 0.85rem;
    color: {MUTED};
    font-weight: 600;
}}
.stTabs [aria-selected="true"] {{
    background: {CARD} !important;
    color: {TEXT} !important;
}}

/* ── Buttons ── */
.stButton > button {{
    background: {ACCENT} !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    font-weight: 700 !important;
    font-size: 0.9rem !important;
    padding: 0.62rem 1.2rem !important;
    box-shadow: 0 10px 18px rgba(124,111,240,0.22);
    transition: opacity 0.15s, transform 0.15s;
}}
.stButton > button:hover {{ opacity: 0.92; transform: translateY(-1px); }}

/* ── Progress ── */
.stProgress > div > div > div {{ background: {ACCENT} !important; }}

/* ── Metrics ── */
[data-testid="metric-container"] {{
    background: {CARD};
    border-radius: 16px;
    padding: 1rem 1.1rem;
    border: 1px solid #E5E7EB;
    box-shadow: 0 8px 22px rgba(17,24,39,0.05);
}}

#MainMenu, footer, header {{ visibility: hidden; }}
</style>
""",
    unsafe_allow_html=True,
)

# ─────────────────────────────────────────────
# DATA
# ─────────────────────────────────────────────
np.random.seed(42)
random.seed(42)

DEPARTMENTS     = ["Legal Ops", "Prosecution", "Advisory", "Admin", "IT"]
VENDORS         = ["Law Library SG", "SG Courts Tech", "MCI Supplies", "AGC Facilities", "Legal Nexis"]
CATEGORIES      = ["Professional Fees", "IT Services", "Office Supplies", "Facilities", "Training"]
PAYMENT_METHODS = ["Interbank Transfer", "Cheque", "GIRO", "Corporate Card"]

def gen_transactions(n=220):
    dates   = [datetime(2025, 1, 1) + timedelta(days=random.randint(0, 364)) for _ in range(n)]
    amounts = np.abs(np.random.lognormal(8, 1.2, n)).round(2)
    dept    = [random.choice(DEPARTMENTS) for _ in range(n)]
    vendor  = [random.choice(VENDORS) for _ in range(n)]
    cat     = [random.choice(CATEGORIES) for _ in range(n)]
    method  = [random.choice(PAYMENT_METHODS) for _ in range(n)]
    amt_list = amounts.tolist()
    flags = []
    for amt in amt_list:
        flag = "Normal"
        if amt > 80000:
            flag = "⚠️ High Value"
        elif amt_list.count(amt) > 1:
            flag = "⚠️ Duplicate"
        elif random.random() < 0.04:
            flag = "⚠️ Odd Timing"
        flags.append(flag)
    df = pd.DataFrame({
        "Date": dates, "Department": dept, "Vendor": vendor,
        "Category": cat, "Amount (SGD)": amounts,
        "Payment Method": method,
        "Status": ["Approved" if random.random() > 0.15 else "Pending" for _ in range(n)],
        "Flag": flags,
    })
    df["Date"]  = pd.to_datetime(df["Date"])
    df["Month"] = df["Date"].dt.strftime("%b %Y")
    df["Week"]  = df["Date"].dt.isocalendar().week.astype(int)
    return df.sort_values("Date").reset_index(drop=True)

df = gen_transactions(220)

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown(
        "<div style='font-size:1.05rem;font-weight:800;color:#111827;margin-bottom:2px;'>⚖ FinOps Suite</div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<div style='font-size:0.8rem;color:#6B7280;margin-bottom:1rem;'>Attorney-General's Chambers</div>",
        unsafe_allow_html=True,
    )
    st.divider()

    page = st.radio(
        "Navigation",
        [
            "📊 Executive Dashboard",
            "🔍 Transaction Validator",
            "📈 Spend Analytics",
            "🤖 Report Generator",
            "🚨 Anomaly Monitor",
        ],
        label_visibility="collapsed",
    )
    st.divider()

    st.markdown(
        "<div style='font-size:0.75rem;color:#7C6FF0;font-weight:700;letter-spacing:1px;margin-bottom:0.6rem;'>FILTERS</div>",
        unsafe_allow_html=True,
    )
    sel_dept   = st.multiselect("Department", DEPARTMENTS, default=DEPARTMENTS)
    sel_cat    = st.multiselect("Category",   CATEGORIES,  default=CATEGORIES)
    date_range = st.date_input("Date Range",  value=(datetime(2025, 1, 1), datetime(2025, 12, 31)))
    st.divider()
    st.caption("Demo v3.1 · AGC Interview")

fdf = df[df["Department"].isin(sel_dept) & df["Category"].isin(sel_cat)].copy()
if isinstance(date_range, tuple) and len(date_range) == 2:
    s, e = pd.Timestamp(date_range[0]), pd.Timestamp(date_range[1])
    fdf = fdf[(fdf["Date"] >= s) & (fdf["Date"] <= e)]


# ═══════════════════════════════════════════════
# PAGE 1 — EXECUTIVE DASHBOARD
# ═══════════════════════════════════════════════
if page == "📊 Executive Dashboard":

    st.markdown("""
    <div class="hero-banner">
      <span class="hero-badge">Attorney-General's Chambers · Finance Process Transformation</span>
      <h1 class="hero-title">FinOps Automation Suite</h1>
      <p class="hero-sub">Real-time financial monitoring · Automated reporting · Anomaly detection · Workflow optimisation</p>
    </div>
    """, unsafe_allow_html=True)

    # ── 4 KPI cards ──
    total_spend  = fdf["Amount (SGD)"].sum()
    n_txn        = len(fdf)
    n_anomalies  = (fdf["Flag"] != "Normal").sum()
    avg_txn      = fdf["Amount (SGD)"].mean() if n_txn > 0 else 0
    top_vendor   = fdf.groupby("Vendor")["Amount (SGD)"].sum().idxmax() if n_txn > 0 else "—"

    c1, c2, c3, c4 = st.columns(4)
    kpis = [
        (c1, "💰", "Total Spend",       f"S${total_spend/1e6:.2f}M", "↑ 4.2% vs last year",       True),
        (c2, "🧾", "Transactions",       f"{n_txn:,}",               "↑ 12 this week",             True),
        (c3, "🚨", "Anomalies Flagged",  str(n_anomalies),           f"{n_anomalies} need review", False),
        (c4, "📊", "Avg Transaction",    f"S${avg_txn:,.0f}",        f"Across {n_txn} records",    True),
    ]
    for col, icon, label, val, delta, pos in kpis:
        with col:
            cls = "kpi-delta-pos" if pos else "kpi-delta-neg"
            st.markdown(f"""
            <div class="kpi-card">
              <div class="kpi-icon">{icon}</div>
              <div class="kpi-label">{label}</div>
              <div class="kpi-value">{val}</div>
              <div class="{cls}">{delta}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    col_a, col_b = st.columns([3, 2])

    with col_a:
        st.markdown('<div class="section-title">Monthly Spend Trend</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-sub">Automated aggregation from all department submissions</div>', unsafe_allow_html=True)
        monthly = fdf.groupby(fdf["Date"].dt.to_period("M"))["Amount (SGD)"].sum().reset_index()
        monthly["Date"] = monthly["Date"].astype(str)
        fig = px.bar(monthly, x="Date", y="Amount (SGD)",
                     color_discrete_sequence=[ACCENT], template="plotly_white")
        fig.update_traces(marker_line_width=0, marker_cornerradius=6)
        fig.update_layout(**PLOT_LAYOUT, height=320, xaxis_tickangle=-35, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    with col_b:
        st.markdown('<div class="section-title">Spend by Category</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-sub">Auto-classified via rule engine</div>', unsafe_allow_html=True)
        cat_spend = fdf.groupby("Category")["Amount (SGD)"].sum().reset_index()
        fig2 = px.pie(cat_spend, values="Amount (SGD)", names="Category",
                      color_discrete_sequence=CHART_COLORS,
                      template="plotly_white", hole=0.56)
        fig2.update_layout(**PLOT_LAYOUT, height=320, legend=dict(font_size=11))
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    # ── Department Spend: clean horizontal grouped bar ──
    st.markdown('<div class="section-title">Department Spend by Category</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Comparative breakdown across all departments</div>', unsafe_allow_html=True)

    dept_cat = fdf.groupby(["Department", "Category"])["Amount (SGD)"].sum().reset_index()
    fig3 = px.bar(
        dept_cat,
        x="Amount (SGD)",
        y="Department",
        color="Category",
        orientation="h",
        template="plotly_white",
        color_discrete_sequence=CHART_COLORS,
        barmode="group",
    )
    fig3.update_layout(
        **PLOT_LAYOUT,
        height=380,
        yaxis=dict(categoryorder="total ascending"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02,
                    xanchor="left", x=0, font_size=11),
        xaxis_title="Amount (SGD)",
        yaxis_title="",
    )
    fig3.update_traces(marker_cornerradius=4)
    st.plotly_chart(fig3, use_container_width=True)


# ═══════════════════════════════════════════════
# PAGE 2 — TRANSACTION VALIDATOR
# ═══════════════════════════════════════════════
elif page == "🔍 Transaction Validator":

    st.markdown('<div class="section-title">🔍 Automated Transaction Validator</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Simulate or upload transactions — checks duplicates, policy limits, and data integrity in real time.</div>', unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["Live Simulation", "Upload CSV"])

    with tab1:
        col1, col2, col3 = st.columns(3)
        with col1:
            txn_vendor = st.selectbox("Vendor", VENDORS)
            txn_dept   = st.selectbox("Department", DEPARTMENTS)
        with col2:
            txn_amount = st.number_input("Amount (SGD)", min_value=0.0, value=5000.0, step=100.0)
            txn_cat    = st.selectbox("Category", CATEGORIES)
        with col3:
            txn_method = st.selectbox("Payment Method", PAYMENT_METHODS)
            txn_date   = st.date_input("Transaction Date", value=datetime.today())

        if st.button("🚀 Run Validation", use_container_width=True):
            with st.spinner("Running automated validation checks…"):
                time.sleep(1.0)

            checks = []
            checks.append(
                ("✅", "Amount within policy limit (≤ S$100,000)", "PASS")
                if txn_amount <= 100000 else
                ("❌", f"Amount S${txn_amount:,.2f} exceeds single-transaction limit", "FAIL")
            )
            dup = fdf[
                (fdf["Vendor"] == txn_vendor) &
                (fdf["Amount (SGD)"].between(txn_amount * 0.97, txn_amount * 1.03)) &
                (abs((fdf["Date"] - pd.Timestamp(txn_date)).dt.days) < 7)
            ]
            checks.append(
                ("✅", "No duplicate transactions detected (±3% amount, ±7 days)", "PASS")
                if dup.empty else
                ("⚠️", f"{len(dup)} possible duplicate(s) found for this vendor/amount", "WARN")
            )
            checks.append(
                ("⚠️", "Transaction dated on a weekend — unusual timing", "WARN")
                if pd.Timestamp(txn_date).weekday() >= 5 else
                ("✅", "Transaction date is a working day", "PASS")
            )
            checks.append(
                ("❌", "Corporate Card not permitted for amounts > S$20,000", "FAIL")
                if txn_method == "Corporate Card" and txn_amount > 20000 else
                ("✅", "Payment method aligned with transaction amount", "PASS")
            )
            checks.append(("✅", f"Vendor '{txn_vendor}' is on the approved vendor register", "PASS"))

            st.markdown("#### Validation Results")
            for icon, msg, status in checks:
                badge = (
                    '<span class="badge-pass">PASS</span>' if status == "PASS" else
                    '<span class="badge-fail">FAIL</span>' if status == "FAIL" else
                    '<span class="badge-warn">WARN</span>'
                )
                st.markdown(f"{icon} {badge} &nbsp; {msg}", unsafe_allow_html=True)
                st.divider()

            passed = sum(1 for _, _, s in checks if s == "PASS")
            score  = int((passed / len(checks)) * 100)
            st.markdown(f"#### Compliance Score: `{score}/100`")
            st.progress(score / 100)

            if score == 100:
                st.success("✅ Transaction cleared for processing.")
            elif score >= 60:
                st.warning("⚠️ Transaction flagged for manual review before processing.")
            else:
                st.error("❌ Transaction rejected. Please resolve issues and resubmit.")

    with tab2:
        st.info("Upload a CSV with columns: Vendor, Department, Amount (SGD), Category, Payment Method, Date")
        uploaded = st.file_uploader("Choose file", type="csv")

        def validate_transactions(df_in, existing_df=None):
            df_v = df_in.copy()
            required_cols = ["Vendor", "Department", "Amount (SGD)", "Category", "Payment Method", "Date"]
            missing = [c for c in required_cols if c not in df_v.columns]
            if missing:
                return None, pd.DataFrame([{"Row": "", "Validation Status": "FAIL",
                                            "Issues": f"Missing columns: {', '.join(missing)}"}])
            df_v["Date"]         = pd.to_datetime(df_v["Date"], errors="coerce")
            df_v["Amount (SGD)"] = pd.to_numeric(df_v["Amount (SGD)"], errors="coerce")
            results = []
            for idx, row in df_v.iterrows():
                issues, status = [], "PASS"
                if pd.isna(row["Date"]):
                    issues.append("Invalid date"); status = "FAIL"
                if pd.isna(row["Amount (SGD)"]):
                    issues.append("Invalid amount"); status = "FAIL"
                if not pd.isna(row["Amount (SGD)"]) and row["Amount (SGD)"] > 100000:
                    issues.append("Exceeds S$100,000 limit"); status = "FAIL"
                if not pd.isna(row["Date"]) and row["Date"].weekday() >= 5:
                    issues.append("Weekend transaction")
                    if status != "FAIL": status = "WARN"
                if row["Payment Method"] == "Corporate Card" and not pd.isna(row["Amount (SGD)"]) and row["Amount (SGD)"] > 20000:
                    issues.append("Corp Card >S$20k not allowed"); status = "FAIL"
                src = existing_df if existing_df is not None else df_v
                if not pd.isna(row["Date"]) and not pd.isna(row["Amount (SGD)"]):
                    dup = src[
                        (src["Vendor"] == row["Vendor"]) &
                        (src["Amount (SGD)"].between(row["Amount (SGD)"] * 0.97, row["Amount (SGD)"] * 1.03)) &
                        ((src["Date"] - row["Date"]).abs().dt.days < 7)
                    ]
                    if len(dup) > 1:
                        issues.append("Possible duplicate")
                        if status == "PASS": status = "WARN"
                results.append({"Row": idx + 1, "Validation Status": status,
                                 "Issues": "; ".join(issues) if issues else "None"})
            return df_v, pd.DataFrame(results)

        if uploaded:
            udf = pd.read_csv(uploaded)
            validated_df, validation_df = validate_transactions(udf, fdf)
            if validated_df is None:
                st.error(validation_df.iloc[0]["Issues"])
            else:
                merged = pd.concat([validated_df.reset_index(drop=True),
                                    validation_df.reset_index(drop=True)], axis=1)
                st.dataframe(merged, use_container_width=True)
                c1v, c2v, c3v = st.columns(3)
                c1v.metric("PASS", int((validation_df["Validation Status"] == "PASS").sum()))
                c2v.metric("WARN", int((validation_df["Validation Status"] == "WARN").sum()))
                c3v.metric("FAIL", int((validation_df["Validation Status"] == "FAIL").sum()))
                st.success(f"✅ Validated {len(udf)} rows.")
                st.download_button(
                    "⬇️ Download Validated CSV",
                    merged.to_csv(index=False).encode("utf-8"),
                    "validated_agc_transactions.csv", "text/csv",
                )


# ═══════════════════════════════════════════════
# PAGE 3 — SPEND ANALYTICS
# ═══════════════════════════════════════════════
elif page == "📈 Spend Analytics":

    st.markdown('<div class="section-title">📈 Spend Analytics</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Drill-down analysis across departments, vendors, and time periods.</div>', unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["By Vendor", "Time Series", "Raw Data"])

    with tab1:
        vendor_spend = (fdf.groupby("Vendor")["Amount (SGD)"]
                        .agg(["sum","count","mean"]).reset_index())
        vendor_spend.columns = ["Vendor","Total Spend","Transactions","Avg Transaction"]
        vendor_spend = vendor_spend.sort_values("Total Spend", ascending=False)
        fig = px.bar(vendor_spend, x="Vendor", y="Total Spend", text="Transactions",
                     template="plotly_white", color_discrete_sequence=[ACCENT])
        fig.update_traces(texttemplate="%{text} txns", textposition="outside", marker_cornerradius=6)
        fig.update_layout(**PLOT_LAYOUT, height=360)
        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(
            vendor_spend.style.format({"Total Spend": "S${:,.0f}", "Avg Transaction": "S${:,.0f}"}),
            use_container_width=True,
        )

    with tab2:
        weekly = fdf.groupby(["Week","Department"])["Amount (SGD)"].sum().reset_index()
        fig2 = px.line(weekly, x="Week", y="Amount (SGD)", color="Department",
                       template="plotly_white", color_discrete_sequence=CHART_COLORS)
        fig2.update_traces(line_width=2.8)
        fig2.update_layout(**PLOT_LAYOUT, height=400, legend=dict(font_size=11))
        st.plotly_chart(fig2, use_container_width=True)

    with tab3:
        st.dataframe(
            fdf[["Date","Department","Vendor","Category","Amount (SGD)","Payment Method","Status","Flag"]]
            .sort_values("Date", ascending=False)
            .style.format({"Amount (SGD)": "S${:,.2f}"})
            .applymap(lambda v: "background-color:#FFFBEB; color:#92400E;" if "⚠️" in str(v) else ""),
            use_container_width=True, height=500,
        )
        st.download_button("⬇️ Download CSV", fdf.to_csv(index=False).encode(),
                           "agc_transactions.csv", "text/csv")


# ═══════════════════════════════════════════════
# PAGE 4 — REPORT GENERATOR
# ═══════════════════════════════════════════════
elif page == "🤖 Report Generator":

    st.markdown('<div class="section-title">🤖 Automated Report Generator</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Instantly produce structured financial reports — no manual compilation needed.</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        report_type = st.selectbox("Report Type", [
            "Monthly Expenditure Summary",
            "Vendor Payment Report",
            "Department Budget Utilisation",
            "Anomaly & Exception Report",
        ])
        period = st.selectbox("Period", ["Q1 2025","Q2 2025","Q3 2025","Q4 2025","Full Year 2025"])
    with col2:
        include_charts = st.checkbox("Include charts", value=True)
        include_raw    = st.checkbox("Include transaction detail", value=False)
        fmt = st.radio("Output Format", ["CSV", "Excel", "Markdown"])

    if st.button("⚙️ Generate Report", use_container_width=True):
        progress = st.progress(0, text="Initialising automation pipeline…")
        steps = [
            "Extracting transactions from database…",
            "Applying classification rules…",
            "Computing aggregations…",
            "Running anomaly checks…",
            "Compiling report structure…",
            "✅ Report ready!",
        ]
        for i, step in enumerate(steps):
            time.sleep(0.35)
            progress.progress(int((i + 1) / len(steps) * 100), text=step)

        st.success("✅ Report generated successfully!")
        st.markdown("---")

        total    = fdf["Amount (SGD)"].sum()
        approved = fdf.loc[fdf["Status"] == "Approved", "Amount (SGD)"].sum()
        top_dept = fdf.groupby("Department")["Amount (SGD)"].sum().idxmax() if len(fdf) > 0 else "—"
        top_vend = fdf.groupby("Vendor")["Amount (SGD)"].sum().idxmax() if len(fdf) > 0 else "—"
        flags    = (fdf["Flag"] != "Normal").sum()

        report_text = f"""# {report_type}
**Period:** {period}  |  **Generated:** {datetime.now().strftime("%d %b %Y %H:%M")}  |  **Auto-generated by FinOps Suite**

---

## Executive Summary
Total financial activity for {period} amounted to **S${total:,.2f}**, of which **S${approved:,.2f}** ({approved/total*100:.1f}%) was approved and processed.

## Key Highlights
- **Highest-spend department:** {top_dept}
- **Top vendor by payment value:** {top_vend}
- **Transactions flagged for review:** {flags} ({flags/len(fdf)*100:.1f}% of total volume)
- **Compliance rate:** {100 - flags/max(len(fdf),1)*100:.1f}%

## Department Summary
| Department | Total Spend | Transactions | % of Budget |
|---|---:|---:|---:|
"""
        dept_summ = fdf.groupby("Department").agg(
            Total=("Amount (SGD)","sum"), Count=("Amount (SGD)","count")
        ).reset_index()
        for _, row in dept_summ.iterrows():
            report_text += f"| {row['Department']} | S${row['Total']:,.0f} | {row['Count']} | {row['Total']/total*100:.1f}% |\n"

        report_text += f"""
## Compliance Notes
- {flags} transaction(s) flagged as anomalous and referred for manual review.
- All automated validations completed with zero system errors.
- Next automated report scheduled: {(datetime.now() + timedelta(days=30)).strftime("%d %b %Y")}.

---
*This report was automatically compiled by the AGC FinOps Automation Suite.*
"""
        st.markdown(report_text)

        # ── Download matches chosen format ──
        if fmt == "CSV":
            out_df = dept_summ.copy()
            out_df.columns = ["Department","Total Spend (SGD)","Transaction Count"]
            dl_data  = out_df.to_csv(index=False).encode("utf-8")
            dl_name  = "agc_report.csv"
            dl_mime  = "text/csv"
            dl_label = "⬇️ Download Report (CSV)"

        elif fmt == "Excel":
            buf = io.BytesIO()
            with pd.ExcelWriter(buf, engine="openpyxl") as writer:
                dept_summ.to_excel(writer, sheet_name="Dept Summary", index=False)
                fdf[["Date","Department","Vendor","Category","Amount (SGD)",
                     "Payment Method","Status","Flag"]].to_excel(
                    writer, sheet_name="Transactions", index=False)
            dl_data  = buf.getvalue()
            dl_name  = "agc_report.xlsx"
            dl_mime  = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            dl_label = "⬇️ Download Report (Excel)"

        else:  # Markdown
            dl_data  = report_text.encode("utf-8")
            dl_name  = "agc_report.md"
            dl_mime  = "text/markdown"
            dl_label = "⬇️ Download Report (Markdown)"

        st.download_button(dl_label, dl_data, dl_name, dl_mime)


# ═══════════════════════════════════════════════
# PAGE 5 — ANOMALY MONITOR
# ═══════════════════════════════════════════════
elif page == "🚨 Anomaly Monitor":

    st.markdown('<div class="section-title">🚨 Real-Time Anomaly Monitor</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Continuous automated scanning for unusual patterns — high values, duplicates, odd timing.</div>', unsafe_allow_html=True)

    anomalies = fdf[fdf["Flag"] != "Normal"].copy()

    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric("Flagged Transactions", len(anomalies),
                  delta=f"{len(anomalies)/max(len(fdf),1)*100:.1f}% of total")
    with m2:
        high_val = (anomalies["Flag"] == "⚠️ High Value").sum()
        st.metric("High Value Alerts", high_val)
    with m3:
        dup = (anomalies["Flag"] == "⚠️ Duplicate").sum()
        st.metric("Duplicate Alerts", dup)

    st.markdown("<hr>", unsafe_allow_html=True)

    col_left, col_right = st.columns([2, 1])

    with col_left:
        st.markdown("#### Flagged Transactions")
        for _, row in anomalies.head(12).iterrows():
            st.markdown(f"""
            <div class="anomaly-row">
              <strong>{row['Flag']}</strong> · {row['Vendor']}
              · {row['Department']}
              · <strong>S${row['Amount (SGD)']:,.2f}</strong>
              · {row['Date'].strftime('%d %b %Y')}
            </div>""", unsafe_allow_html=True)

    with col_right:
        st.markdown("#### Flag Distribution")
        flag_counts = fdf["Flag"].value_counts().reset_index()
        flag_counts.columns = ["Flag","Count"]
        flag_counts = flag_counts[flag_counts["Flag"] != "Normal"]
        fig = px.bar(flag_counts, x="Flag", y="Count",
                     color_discrete_sequence=[ACCENT2], template="plotly_white")
        fig.update_traces(marker_cornerradius=6)
        fig.update_layout(**PLOT_LAYOUT, height=280, showlegend=False, xaxis_title="")
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("#### Spend Distribution: Flagged vs Normal")
    combined = fdf.copy()
    combined["Type"] = combined["Flag"].apply(lambda x: "Flagged" if x != "Normal" else "Normal")
    fig2 = px.histogram(combined, x="Amount (SGD)", color="Type",
                        nbins=40, template="plotly_white",
                        color_discrete_map={"Normal": TEAL, "Flagged": ACCENT2},
                        barmode="overlay", opacity=0.78)
    fig2.update_layout(**PLOT_LAYOUT, height=300, legend=dict(font_size=11))
    st.plotly_chart(fig2, use_container_width=True)
