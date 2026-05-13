import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os
from io import BytesIO

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="LifeOS Finance",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=DM+Mono:wght@400;500&display=swap');

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
    }

    #MainMenu, footer, header { visibility: hidden; }

    .main .block-container {
        padding: 2rem 3rem 3rem;
        max-width: 1400px;
    }

    [data-testid="metric-container"] {
        background: #F8F8F7;
        border: 1px solid #E8E7E2;
        border-radius: 12px;
        padding: 1.25rem 1.5rem !important;
    }

    [data-testid="metric-container"] label {
        font-size: 11px !important;
        font-weight: 500 !important;
        letter-spacing: 0.07em;
        text-transform: uppercase;
        color: #888780 !important;
    }

    [data-testid="metric-container"] [data-testid="stMetricValue"] {
        font-size: 28px !important;
        font-weight: 600 !important;
        color: #1A1A18 !important;
    }

    [data-testid="stMetricDelta"] {
        font-size: 12px !important;
    }

    hr {
        border: none;
        border-top: 1px solid #E8E7E2;
        margin: 1.75rem 0;
    }

    h3 {
        font-size: 11px !important;
        font-weight: 500 !important;
        letter-spacing: 0.07em;
        text-transform: uppercase;
        color: #888780 !important;
        margin-bottom: 0.75rem !important;
    }

    [data-testid="stDataFrame"] {
        border: 1px solid #E8E7E2 !important;
        border-radius: 10px !important;
        overflow: hidden;
    }

    [data-testid="stAlert"] {
        border-radius: 10px !important;
        font-size: 14px !important;
    }

    .js-plotly-plot {
        border-radius: 12px;
    }
</style>
""", unsafe_allow_html=True)

# ── Paths ──────────────────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "transactions.csv")
UPLOADS_DIR = os.path.join(BASE_DIR, "uploads")

os.makedirs(UPLOADS_DIR, exist_ok=True)

REQUIRED_COLUMNS = [
    "transaction_id",
    "user_id",
    "date",
    "description",
    "amount",
    "merchant",
    "category",
    "is_fraud"
]

# ── Helper functions ───────────────────────────────────────────────────────────
def clean_data(dataframe):
    dataframe = dataframe.copy()

    dataframe["amount"] = pd.to_numeric(dataframe["amount"], errors="coerce").fillna(0)
    dataframe["date"] = pd.to_datetime(dataframe["date"], errors="coerce")
    dataframe["is_fraud"] = (
        pd.to_numeric(dataframe["is_fraud"], errors="coerce")
        .fillna(0)
        .astype(int)
    )

    dataframe["user_id"] = dataframe["user_id"].astype(str)
    dataframe["description"] = dataframe["description"].astype(str)
    dataframe["merchant"] = dataframe["merchant"].astype(str)
    dataframe["category"] = dataframe["category"].astype(str)

    dataframe = dataframe.dropna(subset=["date"])

    return dataframe


def validate_dataset(dataframe):
    missing_columns = [
        column for column in REQUIRED_COLUMNS
        if column not in dataframe.columns
    ]

    if missing_columns:
        return False, missing_columns

    return True, []


def generate_pdf_report(
    selected_user,
    data_source_label,
    total_spending,
    transaction_count,
    avg_txn,
    top_category,
    top_category_pct,
    fraud_count,
    monthly_average,
    saving_target
):
    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=28
    )

    styles = getSampleStyleSheet()
    elements = []

    title = Paragraph(
        f"<b>LifeOS AI Financial Report — {selected_user}</b>",
        styles["Title"]
    )

    elements.append(title)
    elements.append(Spacer(1, 20))

    subtitle = Paragraph(
        f"Data Source: {data_source_label}",
        styles["BodyText"]
    )

    elements.append(subtitle)
    elements.append(Spacer(1, 20))

    summary_data = [
        ["Metric", "Value"],
        ["Selected User", selected_user],
        ["Total Spending", f"${total_spending:,.2f}"],
        ["Total Transactions", str(transaction_count)],
        ["Average Transaction", f"${avg_txn:,.2f}"],
        ["Top Spending Category", top_category],
        ["Top Category Percentage", f"{top_category_pct:.1f}%"],
        ["Fraud Transactions", str(fraud_count)],
        ["Estimated Monthly Average", f"${monthly_average:,.2f}"],
        ["Potential Savings", f"${saving_target:,.2f}"],
    ]

    table = Table(summary_data, colWidths=[230, 230])

    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1D9E75")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 1, colors.HexColor("#DDDDDD")),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("BACKGROUND", (0, 1), (-1, -1), colors.whitesmoke),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))

    elements.append(table)
    elements.append(Spacer(1, 25))

    recommendation = Paragraph(
        f"""
        <b>AI Recommendation:</b><br/><br/>
        The highest spending category is <b>{top_category}</b>, accounting for
        <b>{top_category_pct:.1f}%</b> of total spending.
        Reducing spending in <b>{top_category}</b> by 10% could save approximately
        <b>${saving_target:,.2f}</b> during the selected period.
        """,
        styles["BodyText"]
    )

    elements.append(recommendation)
    elements.append(Spacer(1, 20))

    if fraud_count > 0:
        fraud_note = Paragraph(
            f"""
            <b>Fraud Alert:</b><br/><br/>
            This report detected <b>{fraud_count}</b> flagged transaction(s).
            Please review the fraud alerts section in the dashboard and verify these
            transactions with your bank or financial institution.
            """,
            styles["BodyText"]
        )
        elements.append(fraud_note)

    doc.build(elements)

    pdf = buffer.getvalue()
    buffer.close()

    return pdf


# ── Sidebar upload + filters ───────────────────────────────────────────────────
st.sidebar.title("💳 LifeOS Filters")

st.sidebar.markdown("### 📤 Upload Transactions")

uploaded_file = st.sidebar.file_uploader(
    "Upload CSV file",
    type=["csv"]
)

if uploaded_file is not None:
    uploaded_df = pd.read_csv(uploaded_file)

    is_valid, missing_columns = validate_dataset(uploaded_df)

    if not is_valid:
        st.sidebar.error(
            "Uploaded CSV is missing required columns: "
            + ", ".join(missing_columns)
        )
        st.stop()

    df = clean_data(uploaded_df)

    uploaded_file_path = os.path.join(UPLOADS_DIR, uploaded_file.name)
    df.to_csv(uploaded_file_path, index=False)

    st.sidebar.success("Uploaded CSV loaded successfully")
    data_source_label = f"Uploaded file: {uploaded_file.name}"

    with st.expander("Uploaded Dataset Preview"):
        st.dataframe(df.head(10), use_container_width=True)

else:
    df = pd.read_csv(DATA_PATH)
    df = clean_data(df)
    data_source_label = "Default demo dataset"

st.sidebar.caption(data_source_label)

st.sidebar.divider()

# ── Fraud users list ───────────────────────────────────────────────────────────
fraud_users = sorted(df[df["is_fraud"] == 1]["user_id"].unique())

st.sidebar.markdown("### 🚨 Users With Fraud")

if fraud_users:
    st.sidebar.info(", ".join(fraud_users))
else:
    st.sidebar.success("No fraud users found")

st.sidebar.divider()

# ── User filter ────────────────────────────────────────────────────────────────
selected_user = st.sidebar.selectbox(
    "Select User",
    sorted(df["user_id"].unique())
)

user_df = df[df["user_id"] == selected_user].copy()

min_date = user_df["date"].min()
max_date = user_df["date"].max()

date_range = st.sidebar.date_input(
    "Select Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

if isinstance(date_range, tuple) and len(date_range) == 2:
    start_date, end_date = date_range
    user_df = user_df[
        (user_df["date"].dt.date >= start_date) &
        (user_df["date"].dt.date <= end_date)
    ]

selected_categories = st.sidebar.multiselect(
    "Select Categories",
    sorted(user_df["category"].unique()),
    default=sorted(user_df["category"].unique())
)

if selected_categories:
    user_df = user_df[user_df["category"].isin(selected_categories)]

if user_df.empty:
    st.warning("No transactions found for the selected filters.")
    st.stop()

# ── Derived stats ──────────────────────────────────────────────────────────────
total_spending = user_df["amount"].sum()
transaction_count = len(user_df)
avg_txn = total_spending / transaction_count if transaction_count else 0

cat_totals = user_df.groupby("category")["amount"].sum().sort_values(ascending=False)
top_category = cat_totals.index[0]
top_category_pct = (cat_totals.iloc[0] / total_spending * 100) if total_spending else 0

fraud_df = user_df[user_df["is_fraud"] == 1]

saving_target = cat_totals.iloc[0] * 0.10
monthly_average = total_spending / 12

# ── Header ─────────────────────────────────────────────────────────────────────
col_title, col_badge = st.columns([5, 1])

with col_title:
    st.markdown("## 💳 LifeOS Finance")
    st.markdown(
        f"<p style='color:#888780; font-size:14px; margin-top:-0.5rem;'>"
        f"Personal spending dashboard · User {selected_user} · {data_source_label}</p>",
        unsafe_allow_html=True,
    )

with col_badge:
    if len(fraud_df) > 0:
        st.markdown(
            f"<div style='margin-top:1.1rem; text-align:right;'>"
            f"<span style='background:#FCEBEB; color:#791F1F; font-size:12px; "
            f"padding:4px 12px; border-radius:20px; font-weight:500;'>"
            f"⚠ {len(fraud_df)} fraud alert{'s' if len(fraud_df)>1 else ''}</span></div>",
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            "<div style='margin-top:1.1rem; text-align:right;'>"
            "<span style='background:#EAF3DE; color:#27500A; font-size:12px; "
            "padding:4px 12px; border-radius:20px; font-weight:500;'>"
            "✓ No fraud</span></div>",
            unsafe_allow_html=True,
        )

st.divider()

# ── Key metrics ────────────────────────────────────────────────────────────────
m1, m2, m3, m4 = st.columns(4)

m1.metric("Total Spending", f"${total_spending:,.2f}")

m2.metric(
    "Transactions",
    f"{transaction_count}",
    delta=f"avg ${avg_txn:.0f} / txn",
    delta_color="off",
)

m3.metric(
    "Top Category",
    top_category,
    delta=f"{top_category_pct:.0f}% of spend",
    delta_color="off",
)

m4.metric(
    "Fraud Detected",
    f"{len(fraud_df)} txn{'s' if len(fraud_df) != 1 else ''}",
    delta="Review flagged items below" if len(fraud_df) else "All clear",
    delta_color="inverse" if len(fraud_df) else "off",
)

st.divider()

# ── Category charts ────────────────────────────────────────────────────────────
chart_col, bar_col = st.columns([1, 1.6])

category_data = cat_totals.reset_index()
category_data.columns = ["category", "amount"]

COLORS = [
    "#1D9E75", "#185FA5", "#534AB7", "#888780", "#639922",
    "#D85A30", "#D4537E", "#BA7517", "#E24B4A"
]

with chart_col:
    st.markdown("### Spending distribution")

    fig_donut = go.Figure(go.Pie(
        labels=category_data["category"],
        values=category_data["amount"],
        hole=0.62,
        marker=dict(
            colors=COLORS[:len(category_data)],
            line=dict(color="#ffffff", width=3)
        ),
        textinfo="none",
        hovertemplate="<b>%{label}</b><br>$%{value:,.2f} (%{percent})<extra></extra>",
    ))

    fig_donut.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        showlegend=True,
        height=280,
    )

    st.plotly_chart(fig_donut, use_container_width=True)

with bar_col:
    st.markdown("### Amount by category")

    fig_bar = go.Figure(go.Bar(
        x=category_data["amount"],
        y=category_data["category"],
        orientation="h",
        marker=dict(
            color=COLORS[:len(category_data)],
            line=dict(width=0),
        ),
        text=[f"${v:,.0f}" for v in category_data["amount"]],
        textposition="outside",
        hovertemplate="<b>%{y}</b><br>$%{x:,.2f}<extra></extra>",
    ))

    fig_bar.update_layout(
        margin=dict(l=0, r=60, t=0, b=0),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
        yaxis=dict(showgrid=False, autorange="reversed"),
        height=280,
        showlegend=False,
    )

    st.plotly_chart(fig_bar, use_container_width=True)

st.divider()

# ── Monthly spending trend ─────────────────────────────────────────────────────
st.markdown("### Monthly spending trend")

monthly_data = (
    user_df
    .dropna(subset=["date"])
    .groupby(user_df["date"].dt.to_period("M"))["amount"]
    .sum()
    .reset_index()
)

monthly_data["date"] = monthly_data["date"].astype(str)

fig_line = go.Figure()

fig_line.add_trace(go.Scatter(
    x=monthly_data["date"],
    y=monthly_data["amount"],
    mode="lines+markers",
    line=dict(color="#185FA5", width=3),
    marker=dict(size=8),
    hovertemplate="<b>%{x}</b><br>$%{y:,.2f}<extra></extra>"
))

fig_line.update_layout(
    height=320,
    margin=dict(l=0, r=0, t=10, b=0),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=dict(showgrid=False, title="Month"),
    yaxis=dict(showgrid=True, gridcolor="#ECEBE7", title="Spending"),
    font=dict(family="DM Sans", size=12, color="#5F5E5A"),
    showlegend=False,
)

st.plotly_chart(fig_line, use_container_width=True)

st.divider()

# ── Recent transactions ────────────────────────────────────────────────────────
st.markdown("### Recent transactions")

df_display = user_df.sort_values("date", ascending=False).copy()

df_display["Amount"] = df_display["amount"].apply(lambda x: f"${x:,.2f}")
df_display["Category"] = df_display["category"]
df_display["Status"] = df_display["is_fraud"].apply(
    lambda x: "🚨 Flagged" if x == 1 else "✓ OK"
)

st.dataframe(
    df_display[[
        "transaction_id",
        "user_id",
        "date",
        "description",
        "Amount",
        "merchant",
        "Category",
        "Status"
    ]].head(25),
    use_container_width=True,
    hide_index=True,
    height=400,
)

st.divider()

# ── Fraud alerts ───────────────────────────────────────────────────────────────
st.markdown("### Fraud alerts")

if len(fraud_df) > 0:
    st.error(
        f"**{len(fraud_df)} fraudulent transaction{'s' if len(fraud_df)>1 else ''} detected.** "
        "Review the records below and contact your bank immediately.",
        icon="🚨",
    )

    fraud_display = fraud_df.copy()
    fraud_display["Amount"] = fraud_display["amount"].apply(lambda x: f"${x:,.2f}")

    st.dataframe(
        fraud_display[[
            "transaction_id",
            "user_id",
            "date",
            "description",
            "Amount",
            "merchant",
            "category"
        ]],
        use_container_width=True,
        hide_index=True,
    )
else:
    st.success("No fraudulent transactions detected for this user.", icon="✅")

st.divider()

# ── AI Advisor ─────────────────────────────────────────────────────────────────
st.markdown("### AI advisor")

adv_col, _ = st.columns([3, 1])

with adv_col:
    st.markdown(
        f"""
        <div style="background:#F8F8F7; border:1px solid #E8E7E2; border-radius:12px;
                    padding:1.25rem 1.5rem; font-size:14px; line-height:1.7; color:#2C2C2A;">
            <p style="margin:0 0 0.75rem;">
                User <strong>{selected_user}</strong> spent
                <strong>${total_spending:,.2f}</strong> across
                <strong>{transaction_count}</strong> transactions in the selected period.
            </p>
            <p style="margin:0 0 0.75rem;">
                Estimated monthly average spending is
                <strong>${monthly_average:,.2f}</strong>.
            </p>
            <p style="margin:0 0 0.75rem;">
                The highest-spend category is <strong>{top_category}</strong>,
                accounting for <strong>{top_category_pct:.0f}%</strong> of total spending.
            </p>
            <div style="background:#EAF3DE; border-left:3px solid #3B6D11;
                        border-radius:0 8px 8px 0; padding:0.75rem 1rem; margin-top:0.75rem;
                        color:#173404; font-size:13px;">
                <strong>Recommendation:</strong> Reducing {top_category} spending by 10%
                could save approximately <strong>${saving_target:,.2f}</strong>
                in the selected period.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.divider()

# ── Downloadable Financial Reports ─────────────────────────────────────────────
st.markdown("### Download financial report")

report_df = user_df.sort_values("date", ascending=False).copy()

report_df["amount"] = report_df["amount"].round(2)
report_df["status"] = report_df["is_fraud"].apply(
    lambda x: "Fraud Flagged" if x == 1 else "Normal"
)

summary_report = pd.DataFrame({
    "Metric": [
        "Selected User",
        "Data Source",
        "Total Spending",
        "Total Transactions",
        "Average Transaction Amount",
        "Top Spending Category",
        "Top Category Percentage",
        "Fraud Transactions",
        "Estimated Monthly Average",
        "Potential Savings by Reducing Top Category 10%"
    ],
    "Value": [
        selected_user,
        data_source_label,
        f"${total_spending:,.2f}",
        transaction_count,
        f"${avg_txn:,.2f}",
        top_category,
        f"{top_category_pct:.1f}%",
        len(fraud_df),
        f"${monthly_average:,.2f}",
        f"${saving_target:,.2f}"
    ]
})

csv_report = report_df.to_csv(index=False).encode("utf-8")
summary_csv = summary_report.to_csv(index=False).encode("utf-8")

pdf_report = generate_pdf_report(
    selected_user=selected_user,
    data_source_label=data_source_label,
    total_spending=total_spending,
    transaction_count=transaction_count,
    avg_txn=avg_txn,
    top_category=top_category,
    top_category_pct=top_category_pct,
    fraud_count=len(fraud_df),
    monthly_average=monthly_average,
    saving_target=saving_target
)

col_download1, col_download2, col_download3 = st.columns(3)

with col_download1:
    st.download_button(
        label="⬇️ Download Transaction Report CSV",
        data=csv_report,
        file_name=f"{selected_user}_transaction_report.csv",
        mime="text/csv"
    )

with col_download2:
    st.download_button(
        label="⬇️ Download Financial Summary CSV",
        data=summary_csv,
        file_name=f"{selected_user}_financial_summary.csv",
        mime="text/csv"
    )

with col_download3:
    st.download_button(
        label="📄 Download Financial Report PDF",
        data=pdf_report,
        file_name=f"{selected_user}_financial_report.pdf",
        mime="application/pdf"
    )

st.success(
    "Reports are ready. You can download the detailed transaction report, financial summary, and PDF report."
)