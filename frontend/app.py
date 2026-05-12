import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os
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
# ── Load data ──────────────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "transactions.csv")
df = pd.read_csv(DATA_PATH)
df["amount"] = pd.to_numeric(df["amount"], errors="coerce").fillna(0)
df["date"] = pd.to_datetime(df["date"], errors="coerce")
df["is_fraud"] = pd.to_numeric(df["is_fraud"], errors="coerce").fillna(0).astype(int)
# ── Sidebar filters ────────────────────────────────────────────────────────────
st.sidebar.title("💳 LifeOS Filters")
fraud_users = sorted(df[df["is_fraud"] == 1]["user_id"].unique())
st.sidebar.markdown("### 🚨 Users With Fraud")
if fraud_users:
    st.sidebar.info(", ".join(fraud_users))
else:
    st.sidebar.success("No fraud users found")
st.sidebar.divider()
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
# ── Header ─────────────────────────────────────────────────────────────────────
col_title, col_badge = st.columns([5, 1])
with col_title:
    st.markdown("## 💳 LifeOS Finance")
    st.markdown(
        f"<p style='color:#888780; font-size:14px; margin-top:-0.5rem;'>"
        f"Personal spending dashboard · Last 12 months · User {selected_user}</p>",
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
saving_target = cat_totals.iloc[0] * 0.10
monthly_average = total_spending / 12
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