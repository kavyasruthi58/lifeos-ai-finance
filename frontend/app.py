import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import plotly.graph_objects as go
import os
import re
from io import BytesIO

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors

st.set_page_config(
    page_title="LifeOS Finance",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="expanded",
)

PRIMARY = "#0F3D4C"
MUTED = "#667085"

CHART_COLORS = [
    "#0F3D4C", "#0F766E", "#64748B", "#94A3B8",
    "#475569", "#334155", "#2E7D6B", "#6B7280",
]

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    color: #101828;
}

#MainMenu, footer, header {
    visibility: hidden;
}

.main .block-container {
    padding: 2rem 2.4rem 3rem;
    max-width: 1500px;
}

section[data-testid="stSidebar"] {
    background: #F8FAFC;
    border-right: 1px solid #D0D5DD;
}

/* Selectbox */
section[data-testid="stSidebar"] [data-baseweb="select"] > div {
    border: 1.5px solid #D0D5DD !important;
    border-radius: 10px !important;
    background-color: #FFFFFF !important;
    box-shadow: none !important;
    transition: border-color 0.15s ease !important;
}

section[data-testid="stSidebar"] [data-baseweb="select"] > div:focus-within {
    border-color: #0F3D4C !important;
    box-shadow: 0 0 0 3px rgba(15, 61, 76, 0.08) !important;
}

/* Date input */
section[data-testid="stSidebar"] [data-testid="stDateInput"] [data-baseweb="input"] {
    border: 1.5px solid #D0D5DD !important;
    border-radius: 10px !important;
    background-color: #FFFFFF !important;
    box-shadow: none !important;
}

section[data-testid="stSidebar"] [data-testid="stDateInput"] input {
    border: none !important;
    background-color: #FFFFFF !important;
    color: #101828 !important;
    font-size: 13px !important;
}

/* File uploader */
section[data-testid="stSidebar"] [data-testid="stFileUploader"] section {
    border: 1.5px dashed #D0D5DD !important;
    border-radius: 12px !important;
    background-color: #FFFFFF !important;
    transition: border-color 0.15s ease !important;
}

section[data-testid="stSidebar"] [data-testid="stFileUploader"] section:hover {
    border-color: #0F3D4C !important;
    background-color: #F0F9FF !important;
}

/* Multiselect container */
section[data-testid="stSidebar"] [data-baseweb="select"][aria-expanded] > div,
section[data-testid="stSidebar"] [data-testid="stMultiSelect"] [data-baseweb="select"] > div {
    border: 1.5px solid #D0D5DD !important;
    border-radius: 10px !important;
    background-color: #FFFFFF !important;
    box-shadow: none !important;
    min-height: 42px !important;
    padding: 4px 6px !important;
}

/* Multiselect tags — replace salmon/red with teal brand color */
section[data-testid="stSidebar"] [data-baseweb="tag"] {
    background-color: #0F3D4C !important;
    border-radius: 6px !important;
    margin: 2px !important;
    padding: 2px 6px !important;
    border: none !important;
}

section[data-testid="stSidebar"] [data-baseweb="tag"] span {
    color: #FFFFFF !important;
    font-size: 12px !important;
    font-weight: 600 !important;
    font-family: 'Inter', sans-serif !important;
}

/* Tag close (×) button */
section[data-testid="stSidebar"] [data-baseweb="tag"] button,
section[data-testid="stSidebar"] [data-baseweb="tag"] [role="button"] {
    color: rgba(255,255,255,0.75) !important;
    background: transparent !important;
}

section[data-testid="stSidebar"] [data-baseweb="tag"] button:hover {
    color: #FFFFFF !important;
}

/* Sidebar label text */
section[data-testid="stSidebar"] label {
    font-size: 13px !important;
    font-weight: 600 !important;
    color: #344054 !important;
    margin-bottom: 4px !important;
}

h1, h2 {
    color: #101828 !important;
    font-weight: 800 !important;
}

h3 {
    font-size: 12px !important;
    font-weight: 700 !important;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    color: #667085 !important;
    margin-bottom: 0.75rem !important;
}

hr {
    border: none;
    border-top: 1px solid #D0D5DD;
    margin: 1.75rem 0;
}

[data-testid="metric-container"] {
    background: #FFFFFF;
    border: 1px solid #D0D5DD;
    border-radius: 14px;
    padding: 1.25rem 1.5rem !important;
    box-shadow: 0 1px 3px rgba(16, 24, 40, 0.08);
}

[data-testid="metric-container"] label {
    font-size: 11px !important;
    font-weight: 700 !important;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    color: #667085 !important;
}

[data-testid="metric-container"] [data-testid="stMetricValue"] {
    font-size: 30px !important;
    font-weight: 800 !important;
    color: #101828 !important;
}

[data-testid="stDataFrame"] {
    border: 1px solid #D0D5DD !important;
    border-radius: 12px !important;
    overflow: hidden;
}

[data-testid="stAlert"] {
    border-radius: 12px !important;
    font-size: 14px !important;
}

/* Success alerts — replace Streamlit green with brand teal */
[data-testid="stAlert"][data-baseweb="notification"][kind="positive"],
div[data-testid="stAlert"] > div[class*="success"],
div[class*="stSuccess"] > div,
[data-testid="stNotification"][kind="success"] {
    background-color: #F0F9FF !important;
    border: 1px solid #BAE6FD !important;
    color: #0F3D4C !important;
}

/* Target all green/success banners globally */
div[data-testid="stAlert"] {
    border-left: 4px solid #0F3D4C !important;
}

/* Sidebar success (CSV loaded) */
section[data-testid="stSidebar"] div[data-testid="stAlert"] {
    background-color: #F0F9FF !important;
    border-left: 4px solid #0F3D4C !important;
    color: #0F3D4C !important;
    border-radius: 10px !important;
}

/* Override the bright green background on success alerts everywhere */
[data-testid="stAlert"] [data-baseweb="notification"] {
    background-color: #F0F9FF !important;
    color: #0F3D4C !important;
}

/* Style success icon color */
[data-testid="stAlert"] svg {
    color: #0F3D4C !important;
    fill: #0F3D4C !important;
}

.js-plotly-plot {
    border-radius: 14px;
}

.risk-badge {
    background:#FEF3F2;
    color:#B42318;
    font-size:12px;
    padding:7px 14px;
    border-radius:10px;
    font-weight:700;
}

.safe-badge {
    background:#ECFDF3;
    color:#027A48;
    font-size:12px;
    padding:7px 14px;
    border-radius:10px;
    font-weight:700;
}

.info-box {
    background: #EFF8FF;
    border-left: 3px solid #175CD3;
    border-radius: 8px;
    padding: 0.9rem 1rem;
    color: #1849A9;
    font-size: 13px;
    line-height: 1.6;
}

.ai-advisor-card {
    background: #EFF6FF;
    border: 1px solid #D0D5DD;
    border-radius: 14px;
    padding: 1.25rem 1.5rem;
    font-family: 'Inter', sans-serif !important;
    font-size: 14px;
    line-height: 1.7;
    color: #0F3D4C;
    box-shadow: 0 1px 3px rgba(16, 24, 40, 0.08);
}

.ai-advisor-card p {
    font-family: 'Inter', sans-serif !important;
    margin: 0 0 0.75rem 0;
}

.ai-advisor-card strong {
    font-family: 'Inter', sans-serif !important;
    font-weight: 700;
}

.recommendation-box {
    background: #F0F9FF;
    border-left: 4px solid #0F3D4C;
    border-radius: 0 10px 10px 0;
    padding: 0.85rem 1rem;
    margin-top: 0.75rem;
    color: #0F3D4C;
    font-size: 13px;
    font-family: 'Inter', sans-serif !important;
}

[data-testid="stChatInput"] {
    background-color: #FFFFFF !important;
    border: 1.5px solid #111827 !important;
    border-radius: 14px !important;
    padding: 6px !important;
    box-shadow: none !important;
}

/* Fix red border on text input */
[data-testid="stTextInput"] input {
    border: 1.5px solid #111827 !important;
    border-radius: 10px !important;
    background-color: #FFFFFF !important;
    box-shadow: none !important;
    outline: none !important;
}

[data-testid="stTextInput"] input:focus {
    border: 1.5px solid #0F3D4C !important;
    box-shadow: 0 0 0 3px rgba(15, 61, 76, 0.1) !important;
}

[data-testid="stTextInput"] > div {
    border: none !important;
    box-shadow: none !important;
}

[data-testid="stTextInput"] [data-baseweb="input"] {
    border: 1.5px solid #111827 !important;
    border-radius: 10px !important;
    box-shadow: none !important;
}

[data-testid="stTextInput"] [data-baseweb="input"]:focus-within {
    border: 1.5px solid #0F3D4C !important;
    box-shadow: 0 0 0 3px rgba(15, 61, 76, 0.1) !important;
}

[data-testid="stChatInput"] textarea {
    background-color: #FFFFFF !important;
    color: #111827 !important;
    font-size: 15px !important;
}

[data-testid="stChatInput"] textarea::placeholder {
    color: #667085 !important;
}

[data-testid="stChatInput"] button {
    background-color: #0F3D4C !important;
    color: white !important;
    border-radius: 10px !important;
    width: 44px !important;
    height: 44px !important;
}

[data-testid="stChatInput"] button svg {
    display: none !important;
}

[data-testid="stChatInput"] button::before {
    content: "➤";
    color: white;
    font-size: 22px;
    font-weight: 700;
    transform: rotate(-35deg);
    display: inline-block;
}

.stDownloadButton button {
    border: 1.5px solid #D0D5DD !important;
    border-radius: 12px !important;
    background-color: #FFFFFF !important;
    color: #101828 !important;
    font-weight: 600 !important;
    padding: 0.65rem 1rem !important;
}

.stDownloadButton button:hover {
    border: 1.5px solid #0F3D4C !important;
    color: #0F3D4C !important;
}

/* ── Custom Chat Bubble Styles ── */
.chat-wrapper {
    display: flex;
    flex-direction: column;
    gap: 6px;
    max-height: 300px;
    overflow-y: auto;
    padding: 14px 12px;
    background: #F8FAFC;
    border: 1px solid #E4E7EC;
    border-radius: 14px;
    margin-bottom: 12px;
    scroll-behavior: smooth;
}

.chat-wrapper::-webkit-scrollbar {
    width: 4px;
}
.chat-wrapper::-webkit-scrollbar-track {
    background: transparent;
}
.chat-wrapper::-webkit-scrollbar-thumb {
    background: #D0D5DD;
    border-radius: 4px;
}

.chat-row-user {
    display: flex;
    flex-direction: column;
    align-items: flex-end;
    margin-bottom: 4px;
}

.chat-row-bot {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    margin-bottom: 4px;
}

.chat-label {
    font-size: 10px;
    font-weight: 600;
    letter-spacing: 0.04em;
    color: #9CA3AF;
    margin-bottom: 3px;
    padding: 0 4px;
    text-transform: uppercase;
}

.bubble-user {
    background: #0F3D4C;
    color: #FFFFFF;
    border-radius: 18px 18px 4px 18px;
    padding: 10px 15px;
    font-size: 13.5px;
    font-family: 'Inter', sans-serif;
    max-width: 88%;
    line-height: 1.55;
    box-shadow: 0 2px 8px rgba(15, 61, 76, 0.18);
    word-break: break-word;
}

.bubble-bot {
    background: #FFFFFF;
    color: #101828;
    border: 1px solid #E4E7EC;
    border-radius: 18px 18px 18px 4px;
    padding: 10px 15px;
    font-size: 13.5px;
    font-family: 'Inter', sans-serif;
    max-width: 88%;
    line-height: 1.55;
    box-shadow: 0 2px 6px rgba(16, 24, 40, 0.06);
    word-break: break-word;
}

.bubble-bot strong {
    color: #0F3D4C;
    font-weight: 700;
}

.chat-empty {
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 90px;
    color: #9CA3AF;
    font-size: 13px;
    font-style: italic;
}

/* Quick prompt pill buttons only */
div[data-testid="column"] .stButton > button[kind="secondary"] {
    border: 1.5px solid #D0D5DD !important;
    border-radius: 20px !important;
    background-color: #FFFFFF !important;
    color: #344054 !important;
    font-size: 12px !important;
    font-weight: 600 !important;
    padding: 0.35rem 0.75rem !important;
    transition: all 0.15s ease !important;
}

div[data-testid="column"] .stButton > button[kind="secondary"]:hover {
    border-color: #0F3D4C !important;
    color: #0F3D4C !important;
    background-color: #EFF6FF !important;
}

/* Send button */
button[data-testid="baseButton-secondary"][key="chat_send_btn"],
.stButton > button {
    border: 1.5px solid #D0D5DD !important;
    border-radius: 20px !important;
    background-color: #FFFFFF !important;
    color: #344054 !important;
    font-size: 12px !important;
    font-weight: 600 !important;
    padding: 0.35rem 0.75rem !important;
    transition: all 0.15s ease !important;
}

#chat_send_btn, [data-testid="stButton"] button:has(+ *) {
    background-color: #0F3D4C !important;
    color: #FFFFFF !important;
    border-color: #0F3D4C !important;
    border-radius: 10px !important;
}
</style>
""", unsafe_allow_html=True)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "transactions.csv")
UPLOADS_DIR = os.path.join(BASE_DIR, "uploads")
os.makedirs(UPLOADS_DIR, exist_ok=True)

REQUIRED_COLUMNS = [
    "transaction_id", "user_id", "date", "description",
    "amount", "merchant", "category", "is_fraud"
]


def clean_data(dataframe):
    dataframe = dataframe.copy()
    dataframe["amount"] = pd.to_numeric(dataframe["amount"], errors="coerce").fillna(0)
    dataframe["date"] = pd.to_datetime(dataframe["date"], errors="coerce")
    dataframe["is_fraud"] = pd.to_numeric(dataframe["is_fraud"], errors="coerce").fillna(0).astype(int)
    dataframe["user_id"] = dataframe["user_id"].astype(str)
    dataframe["description"] = dataframe["description"].astype(str)
    dataframe["merchant"] = dataframe["merchant"].astype(str)
    dataframe["category"] = dataframe["category"].astype(str)
    dataframe = dataframe.dropna(subset=["date"])
    return dataframe


def validate_dataset(dataframe):
    missing_columns = [col for col in REQUIRED_COLUMNS if col not in dataframe.columns]
    if missing_columns:
        return False, missing_columns
    return True, []


def finance_chatbot_response(question, user_df, selected_user):
    question = question.lower()

    total_spending = user_df["amount"].sum()
    transaction_count = len(user_df)
    avg_transaction = total_spending / transaction_count if transaction_count else 0

    category_totals = user_df.groupby("category")["amount"].sum().sort_values(ascending=False)
    top_category = category_totals.index[0]
    top_amount = category_totals.iloc[0]
    fraud_df = user_df[user_df["is_fraud"] == 1]

    if "overspending" in question or "spending most" in question or "highest" in question or "biggest" in question:
        return f"You are spending the most on **{top_category}**, with **${top_amount:,.2f}** spent."

    if "fraud" in question or "suspicious" in question or "flagged" in question:
        if len(fraud_df) > 0:
            return f"I found **{len(fraud_df)} suspicious transaction(s)** for user **{selected_user}**. Please review the fraud alerts section."
        return f"No fraud transactions were detected for user **{selected_user}**."

    if "save" in question or "saving" in question or "reduce" in question:
        savings = top_amount * 0.10
        return f"Reduce **{top_category}** spending by 10%. That could save around **${savings:,.2f}**."

    if "total" in question or "spent" in question:
        return f"User **{selected_user}** spent **${total_spending:,.2f}** across **{transaction_count} transactions**."

    if "average" in question:
        return f"The average transaction amount for user **{selected_user}** is **${avg_transaction:,.2f}**."

    if "category" in question or "categories" in question:
        category_summary = "\n".join([f"- **{cat}**: ${amt:,.2f}" for cat, amt in category_totals.items()])
        return f"Here is your category-wise spending:\n\n{category_summary}"

    if "recommend" in question or "advice" in question:
        savings = top_amount * 0.10
        return f"My recommendation is to focus on **{top_category}**. Reducing it by 10% could save **${savings:,.2f}**."

    return "I can help with spending, fraud, savings, totals, averages, and category-wise financial behavior."


def generate_pdf_report(
    selected_user, data_source_label, total_spending, transaction_count,
    avg_txn, top_category, top_category_pct, fraud_count,
    monthly_average, saving_target
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

    elements.append(Paragraph(f"<b>LifeOS AI Financial Report — {selected_user}</b>", styles["Title"]))
    elements.append(Spacer(1, 20))
    elements.append(Paragraph(f"Data Source: {data_source_label}", styles["BodyText"]))
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
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor(PRIMARY)),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 1, colors.HexColor("#DDDDDD")),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("BACKGROUND", (0, 1), (-1, -1), colors.whitesmoke),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))

    elements.append(table)
    elements.append(Spacer(1, 25))

    elements.append(Paragraph(
        f"""
        <b>AI Recommendation:</b><br/><br/>
        The highest spending category is <b>{top_category}</b>, accounting for
        <b>{top_category_pct:.1f}%</b> of total spending. Reducing this category by 10%
        could save approximately <b>${saving_target:,.2f}</b>.
        """,
        styles["BodyText"]
    ))

    if fraud_count > 0:
        elements.append(Spacer(1, 20))
        elements.append(Paragraph(
            f"""
            <b>Fraud Alert:</b><br/><br/>
            This report detected <b>{fraud_count}</b> flagged transaction(s).
            Please review them carefully.
            """,
            styles["BodyText"]
        ))

    doc.build(elements)
    pdf = buffer.getvalue()
    buffer.close()
    return pdf


def render_chat_bubbles(chat_history):
    """Render custom styled chat bubbles using components.html to avoid Streamlit HTML escaping."""

    bubble_css = """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body { background: transparent; font-family: 'Inter', sans-serif; }

    .chat-wrapper {
        display: flex;
        flex-direction: column;
        gap: 6px;
        padding: 14px 12px;
        background: #F8FAFC;
        border: 1px solid #E4E7EC;
        border-radius: 14px;
        overflow-y: auto;
        max-height: 280px;
    }
    .chat-wrapper::-webkit-scrollbar { width: 4px; }
    .chat-wrapper::-webkit-scrollbar-track { background: transparent; }
    .chat-wrapper::-webkit-scrollbar-thumb { background: #D0D5DD; border-radius: 4px; }

    .chat-row-user {
        display: flex;
        flex-direction: column;
        align-items: flex-end;
        margin-bottom: 4px;
    }
    .chat-row-bot {
        display: flex;
        flex-direction: column;
        align-items: flex-start;
        margin-bottom: 4px;
    }
    .chat-label {
        font-size: 10px;
        font-weight: 600;
        letter-spacing: 0.04em;
        color: #9CA3AF;
        margin-bottom: 3px;
        padding: 0 4px;
        text-transform: uppercase;
    }
    .bubble-user {
        background: #0F3D4C;
        color: #FFFFFF;
        border-radius: 18px 18px 4px 18px;
        padding: 10px 15px;
        font-size: 13.5px;
        max-width: 88%;
        line-height: 1.55;
        box-shadow: 0 2px 8px rgba(15,61,76,0.18);
        word-break: break-word;
    }
    .bubble-bot {
        background: #FFFFFF;
        color: #101828;
        border: 1px solid #E4E7EC;
        border-radius: 18px 18px 18px 4px;
        padding: 10px 15px;
        font-size: 13.5px;
        max-width: 88%;
        line-height: 1.55;
        box-shadow: 0 2px 6px rgba(16,24,40,0.06);
        word-break: break-word;
    }
    .bubble-bot strong { color: #0F3D4C; font-weight: 700; }
    .chat-empty {
        display: flex;
        align-items: center;
        justify-content: center;
        min-height: 90px;
        color: #9CA3AF;
        font-size: 13px;
        font-style: italic;
    }
    </style>
    """

    if not chat_history:
        html = bubble_css + '<div class="chat-wrapper"><div class="chat-empty">✨ Ask me anything about your finances</div></div>'
        components.html(html, height=130, scrolling=False)
        return

    body = '<div class="chat-wrapper">'
    for role, message in chat_history:
        msg_html = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', message)
        msg_html = msg_html.replace('\n', '<br>')
        if role == "user":
            body += (
                '<div class="chat-row-user">'
                '<div class="chat-label">You</div>'
                '<div class="bubble-user">' + msg_html + '</div>'
                '</div>'
            )
        else:
            body += (
                '<div class="chat-row-bot">'
                '<div class="chat-label">🤖 LifeOS AI</div>'
                '<div class="bubble-bot">' + msg_html + '</div>'
                '</div>'
            )
    body += '</div>'

    # Auto-scroll to bottom via JS
    scroll_js = "<script>document.querySelector('.chat-wrapper').scrollTop = 99999;</script>"

    # Height grows with messages, capped at ~300px
    height = min(100 + len(chat_history) * 70, 320)
    components.html(bubble_css + body + scroll_js, height=height, scrolling=False)


# ── Sidebar ──────────────────────────────────────────────────────────────────

st.sidebar.title("💳 LifeOS Finance")
st.sidebar.markdown("### Upload Transactions")

uploaded_files = st.sidebar.file_uploader(
    "Upload CSV files",
    type=["csv"],
    accept_multiple_files=True
)

if uploaded_files:
    all_dataframes = []

    for uploaded_file in uploaded_files:
        uploaded_df = pd.read_csv(uploaded_file)
        is_valid, missing_columns = validate_dataset(uploaded_df)

        if not is_valid:
            st.sidebar.error(f"{uploaded_file.name} is missing required columns: " + ", ".join(missing_columns))
            st.stop()

        cleaned_df = clean_data(uploaded_df)
        cleaned_df.to_csv(os.path.join(UPLOADS_DIR, uploaded_file.name), index=False)
        all_dataframes.append(cleaned_df)

    df = pd.concat(all_dataframes, ignore_index=True)
    st.sidebar.markdown(
        f"<div style='background:#F0F9FF; border:1px solid #BAE6FD; border-left:4px solid #0F3D4C; "
        f"border-radius:10px; padding:0.6rem 0.9rem; color:#0F3D4C; font-size:13px; font-weight:600; margin-top:4px;'>"
        f"✅ {len(uploaded_files)} CSV file(s) loaded successfully</div>",
        unsafe_allow_html=True,
    )

    uploaded_names = ", ".join([file.name for file in uploaded_files])
    data_source_label = f"Uploaded files: {uploaded_names}"

    with st.sidebar.expander("Uploaded Dataset Preview", expanded=False):
        st.dataframe(df.head(10), use_container_width=True, height=250)
else:
    df = pd.read_csv(DATA_PATH)
    df = clean_data(df)
    data_source_label = "Default demo dataset"

st.sidebar.markdown("### Data Source")
st.sidebar.caption(data_source_label)
st.sidebar.divider()

selected_user = st.sidebar.selectbox("Select User", sorted(df["user_id"].unique()))

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

st.sidebar.markdown(
    '<div class="info-box">You can upload multiple CSV files at once. The dashboard will combine them and analyze the selected user.</div>',
    unsafe_allow_html=True
)

if user_df.empty:
    st.warning("No transactions found for the selected filters.")
    st.stop()

# ── Metrics ───────────────────────────────────────────────────────────────────

total_spending = user_df["amount"].sum()
transaction_count = len(user_df)
avg_txn = total_spending / transaction_count if transaction_count else 0

cat_totals = user_df.groupby("category")["amount"].sum().sort_values(ascending=False)
top_category = cat_totals.index[0]
top_category_pct = (cat_totals.iloc[0] / total_spending * 100) if total_spending else 0

fraud_df = user_df[user_df["is_fraud"] == 1]
saving_target = cat_totals.iloc[0] * 0.10
monthly_average = total_spending / 12

# ── Header ────────────────────────────────────────────────────────────────────

col_title, col_badge = st.columns([5, 1])

with col_title:
    st.markdown("## 💳 LifeOS Finance")
    st.markdown(
        f"<p style='color:{MUTED}; font-size:14px; margin-top:-0.5rem;'>"
        f"Personal spending dashboard · User <strong>{selected_user}</strong> · {data_source_label}</p>",
        unsafe_allow_html=True,
    )

with col_badge:
    if len(fraud_df) > 0:
        st.markdown(
            f"<div style='margin-top:1.1rem; text-align:right;'>"
            f"<span class='risk-badge'>⚠ Risk: {len(fraud_df)} flagged</span></div>",
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            "<div style='margin-top:1.1rem; text-align:right;'>"
            "<span class='safe-badge'>✓ All clear</span></div>",
            unsafe_allow_html=True,
        )

st.divider()

m1, m2, m3, m4 = st.columns(4)
m1.metric("Total Spending", f"${total_spending:,.2f}", help="Sum of all transaction amounts in the selected date range and categories.")
m2.metric("Transactions", f"{transaction_count}", delta=f"avg ${avg_txn:.0f} / txn", delta_color="off", help="Total number of transactions. Delta shows the average amount per transaction.")
m3.metric("Top Category", top_category, delta=f"{top_category_pct:.0f}% of spend", delta_color="off", help="The category with the highest total spending and its share of overall spend.")
m4.metric(
    "Fraud Detected",
    f"{len(fraud_df)} txn{'s' if len(fraud_df) != 1 else ''}",
    delta="Review required" if len(fraud_df) else "All clear",
    delta_color="inverse" if len(fraud_df) else "off",
    help="Number of transactions flagged as potentially fraudulent.",
)

st.divider()

# ── Charts ────────────────────────────────────────────────────────────────────

chart_col, bar_col = st.columns([1, 1.6])

category_data = cat_totals.reset_index()
category_data.columns = ["category", "amount"]

with chart_col:
    st.markdown("### Spending Distribution")

    fig_donut = go.Figure(go.Pie(
        labels=category_data["category"],
        values=category_data["amount"],
        hole=0.62,
        marker=dict(colors=CHART_COLORS[:len(category_data)], line=dict(color="#FFFFFF", width=3)),
        textinfo="percent",
        hovertemplate="<b>%{label}</b><br>$%{value:,.2f}<extra></extra>",
    ))
    fig_donut.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        showlegend=True,
        height=330,
        font=dict(family="Inter", size=12, color=MUTED),
    )
    st.plotly_chart(fig_donut, use_container_width=True)

with bar_col:
    st.markdown("### Amount by Category")

    fig_bar = go.Figure(go.Bar(
        x=category_data["amount"],
        y=category_data["category"],
        orientation="h",
        marker=dict(color=CHART_COLORS[:len(category_data)], line=dict(width=0)),
        text=[f"${v:,.0f}" for v in category_data["amount"]],
        textposition="outside",
        hovertemplate="<b>%{y}</b><br>$%{x:,.2f}<extra></extra>",
    ))
    fig_bar.update_layout(
        margin=dict(l=0, r=70, t=0, b=0),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(showgrid=False, showticklabels=True, zeroline=False),
        yaxis=dict(showgrid=False, autorange="reversed"),
        height=330,
        showlegend=False,
        font=dict(family="Inter", size=12, color=MUTED),
    )
    st.plotly_chart(fig_bar, use_container_width=True)

st.divider()

# ── Monthly Trend ─────────────────────────────────────────────────────────────

st.markdown("### Monthly Spending Trend")

monthly_data = (
    user_df.dropna(subset=["date"])
    .groupby(user_df["date"].dt.to_period("M"))["amount"]
    .sum()
    .reset_index()
)
monthly_data["date"] = monthly_data["date"].astype(str)

fig_line = go.Figure()

if len(monthly_data) <= 1:
    # Single month — show a bar chart instead of a flat/meaningless line
    fig_line.add_trace(go.Bar(
        x=monthly_data["date"],
        y=monthly_data["amount"],
        marker=dict(color=PRIMARY, line=dict(width=0)),
        text=[f"${v:,.0f}" for v in monthly_data["amount"]],
        textposition="outside",
        hovertemplate="<b>%{x}</b><br>$%{y:,.2f}<extra></extra>",
    ))
    fig_line.update_layout(
        annotations=[dict(
            text="Only one month of data — showing as bar chart",
            xref="paper", yref="paper",
            x=0, y=1.08, showarrow=False,
            font=dict(size=11, color=MUTED),
        )]
    )
else:
    fig_line.add_trace(go.Scatter(
        x=monthly_data["date"],
        y=monthly_data["amount"],
        mode="lines+markers+text",
        line=dict(color=PRIMARY, width=3),
        marker=dict(size=8, color=PRIMARY),
        text=[f"${v:,.0f}" for v in monthly_data["amount"]],
        textposition="top center",
        hovertemplate="<b>%{x}</b><br>$%{y:,.2f}<extra></extra>",
    ))

fig_line.update_layout(
    height=340,
    margin=dict(l=0, r=0, t=20, b=0),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=dict(showgrid=False, title="Month"),
    yaxis=dict(showgrid=True, gridcolor="#E5E7EB", title="Spending ($)"),
    font=dict(family="Inter", size=12, color=MUTED),
    showlegend=False,
)
st.plotly_chart(fig_line, use_container_width=True)

st.divider()

# ── Transactions & Fraud ──────────────────────────────────────────────────────

tx_col, fraud_col = st.columns([1.2, 1])

with tx_col:
    total_txn = len(user_df)
    shown_txn = min(10, total_txn)
    st.markdown(
        f"### Recent Transactions &nbsp;<span style='font-size:12px; font-weight:600; background:#F2F4F7; color:#344054; padding:3px 10px; border-radius:20px; vertical-align:middle;'>Showing {shown_txn} of {total_txn}</span>",
        unsafe_allow_html=True,
    )

    df_display = user_df.sort_values("date", ascending=False).copy()
    df_display["Amount"] = df_display["amount"].apply(lambda x: f"${x:,.2f}")
    df_display["Category"] = df_display["category"]
    df_display["Status"] = df_display["is_fraud"].apply(lambda x: "⚠ Flagged" if x == 1 else "✓ OK")

    st.dataframe(
        df_display[[
            "transaction_id", "user_id", "date", "description",
            "Amount", "merchant", "Category", "Status"
        ]].head(10),
        use_container_width=True,
        hide_index=True,
        height=310,
        column_config={
            "Status": st.column_config.TextColumn(
                "Status",
                help="⚠ Flagged = potential fraud detected",
            ),
        },
    )

with fraud_col:
    st.markdown("### Fraud Alerts")

    if len(fraud_df) > 0:
        st.error(
            f"{len(fraud_df)} flagged transaction(s) detected. Review the records below.",
            icon="⚠️",
        )
        fraud_display = fraud_df.copy()
        fraud_display["Amount"] = fraud_display["amount"].apply(lambda x: f"${x:,.2f}")
        st.dataframe(
            fraud_display[[
                "transaction_id", "user_id", "date", "description",
                "Amount", "merchant", "category"
            ]].head(10),
            use_container_width=True,
            hide_index=True,
            height=240,
        )
    else:
        st.markdown(
            "<div style='background:#F0F9FF; border:1px solid #BAE6FD; border-left:4px solid #0F3D4C; "
            "border-radius:12px; padding:0.85rem 1.1rem; color:#0F3D4C; font-size:14px; font-weight:500;'>"
            "✅ No flagged transactions detected for this user."
            "</div>",
            unsafe_allow_html=True,
        )

st.divider()

# ── AI Advisor ────────────────────────────────────────────────────────────────

st.markdown("### AI Advisor")

st.markdown(
    f"""
    <div class="ai-advisor-card">
        <p>
            User <strong>{selected_user}</strong> spent
            <strong>${total_spending:,.2f}</strong> across
            <strong>{transaction_count}</strong> transactions in the selected period.
        </p>
        <p>
            Estimated monthly average spending is
            <strong>${monthly_average:,.2f}</strong>.
        </p>
        <p>
            The highest-spend category is <strong>{top_category}</strong>,
            accounting for <strong>{top_category_pct:.0f}%</strong> of total spending.
        </p>
        <div class="recommendation-box">
            <strong>Recommendation:</strong> Reducing {top_category} spending by 10%
            could save approximately <strong>${saving_target:,.2f}</strong>.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.divider()

# ── Ask LifeOS AI Chat ────────────────────────────────────────────────────────

st.markdown("### Ask LifeOS AI")
st.caption("Ask questions about spending, fraud, savings, categories, or recommendations.")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Quick-prompt pill buttons + clear chat
q1, q2, q3, _, qclear = st.columns([1, 1, 1, 2, 1])

with q1:
    if st.button("💸 Overspending?", use_container_width=True, key="quick_q1"):
        q = "Where am I overspending?"
        r = finance_chatbot_response(q, user_df, selected_user)
        st.session_state.chat_history.append(("user", q))
        st.session_state.chat_history.append(("assistant", r))
        st.rerun()

with q2:
    if st.button("🚨 Fraud?", use_container_width=True, key="quick_q2"):
        q = "Do I have fraud?"
        r = finance_chatbot_response(q, user_df, selected_user)
        st.session_state.chat_history.append(("user", q))
        st.session_state.chat_history.append(("assistant", r))
        st.rerun()

with q3:
    if st.button("💰 Save money?", use_container_width=True, key="quick_q3"):
        q = "How can I save money?"
        r = finance_chatbot_response(q, user_df, selected_user)
        st.session_state.chat_history.append(("user", q))
        st.session_state.chat_history.append(("assistant", r))
        st.rerun()

with qclear:
    if st.button("🗑 Clear chat", use_container_width=True, key="clear_chat_btn"):
        st.session_state.chat_history = []
        st.rerun()

# Custom bubble chat history
render_chat_bubbles(st.session_state.chat_history)

# Inline chat input (text_input + send button) — stays right below chat bubbles
inp_col, btn_col = st.columns([6, 1])
with inp_col:
    user_question = st.text_input(
        label="chat_input",
        placeholder="Ask LifeOS AI about your financial behavior...",
        label_visibility="collapsed",
        key="chat_text_input",
    )
with btn_col:
    send_clicked = st.button("➤ Send", use_container_width=True, key="chat_send_btn")

if send_clicked and user_question.strip():
    response = finance_chatbot_response(user_question.strip(), user_df, selected_user)
    st.session_state.chat_history.append(("user", user_question.strip()))
    st.session_state.chat_history.append(("assistant", response))
    st.rerun()

st.divider()

# ── Download Reports ──────────────────────────────────────────────────────────

st.markdown("### Download Financial Reports")

report_df = user_df.sort_values("date", ascending=False).copy()
report_df["amount"] = report_df["amount"].round(2)
report_df["status"] = report_df["is_fraud"].apply(lambda x: "Fraud Flagged" if x == 1 else "Normal")

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

d1, d2, d3 = st.columns(3)

with d1:
    st.download_button(
        "Download Transaction Report CSV",
        data=csv_report,
        file_name=f"{selected_user}_transaction_report.csv",
        mime="text/csv",
        use_container_width=True,
    )

with d2:
    st.download_button(
        "Download Financial Summary CSV",
        data=summary_csv,
        file_name=f"{selected_user}_financial_summary.csv",
        mime="text/csv",
        use_container_width=True,
    )

with d3:
    st.download_button(
        "Download Financial Report PDF",
        data=pdf_report,
        file_name=f"{selected_user}_financial_report.pdf",
        mime="application/pdf",
        use_container_width=True,
    )

st.markdown(
    "<div style='background:#F0F9FF; border:1px solid #BAE6FD; border-left:4px solid #0F3D4C; "
    "border-radius:12px; padding:0.85rem 1.1rem; color:#0F3D4C; font-size:14px; font-weight:500;'>"
    "✅ Reports are ready. You can download the detailed transaction report, financial summary, and PDF report."
    "</div>",
    unsafe_allow_html=True,
)