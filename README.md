# LifeOS AI — Personal Finance Intelligence Platform

> An AI-powered personal finance analytics platform combining machine learning, REST APIs, interactive dashboards, fraud detection, downloadable reports, and AI-generated financial insights to help users make smarter financial decisions.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Machine Learning Models](#machine-learning-models)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Running the Application](#running-the-application)
- [API Reference](#api-reference)
- [Dashboard](#dashboard)
- [Roadmap](#roadmap)

---

## Overview

LifeOS AI is a full-stack fintech analytics system that combines machine learning, backend APIs, intelligent financial insights, and interactive data visualization to deliver actionable personal finance intelligence.

The platform supports dynamic transaction uploads, fraud analysis, AI-generated recommendations, downloadable financial reports, and multi-user financial analytics. It serves as the **financial intelligence layer** of the broader LifeOS AI ecosystem — an AI platform focused on intelligent life management and behavioral analytics.

---

## Features

### 🧠 Smart Transaction Categorization

Automatically classifies transaction descriptions into meaningful categories using NLP-based machine learning.

| Input Description | Predicted Category |
|---|---|
| `DOORDASH PURCHASE` | 🍔 Food |
| `UBER TRIP` | 🚗 Transport |
| `NETFLIX PAYMENT` | 🎬 Entertainment |
| `WHOLE FOODS MARKET` | 🛒 Groceries |

**Supported categories:** Food · Groceries · Shopping · Entertainment · Transport · Health · Subscription

---

### 🔍 Fraud Detection

Detects suspicious transactions using anomaly detection, flagging:

- High-value or unusual transactions
- Purchases from unknown merchants
- Abnormal spending patterns
- Potential fraudulent activity

> ⚠️ **Example:** `UNKNOWN ONLINE PAYMENT — $950.00` → **Fraud Alert**

---

### 📈 Budget Forecasting

Predicts future spending trends to help users stay ahead of their finances:

- Monthly spending trend analysis
- Spending behavior tracking
- Budget overrun insights
- Forward-looking financial analytics

---

### 👥 Spending Pattern Analysis

Clusters users into spending profiles using unsupervised machine learning.

| Profile | Description |
|---|---|
| **High Spender** | Consistently above-average transaction amounts |
| **Food-Heavy** | Majority of spend in dining and groceries |
| **Subscription-Heavy** | High recurring monthly charges |
| **Balanced** | Evenly distributed spending behavior |

---

### 💡 AI Financial Advisor

Generates personalized financial recommendations based on spending behavior:

- Reduce shopping expenses
- Lower subscription costs
- Improve savings rate
- Detect unusual spending trends
- Suggest financial optimization strategies

---

### 📤 CSV Upload Support

Upload custom transaction datasets directly into the dashboard for real-time analysis and visualization.

---

### 📄 Downloadable Financial Reports

Generate and download:

- Transaction CSV reports
- Financial summary CSV reports
- Professional PDF financial reports

---

### 📊 Interactive Multi-User Analytics

Analyze financial behavior using:

- User-level filtering
- Date & category filtering
- Fraud-user tracking
- Dynamic dashboard updates

---

## Machine Learning Models

| Module | Algorithm |
|---|---|
| Transaction Categorization | TF-IDF + Logistic Regression |
| Fraud Detection | Isolation Forest |
| Budget Forecasting | Linear Regression |
| Spending Pattern Analysis | K-Means Clustering |
| Financial Advisor | Rule-Based AI Engine |

---

## Tech Stack

### Backend
- **FastAPI** — REST API framework
- **Uvicorn** — ASGI server
- **Python 3.9+**

### Machine Learning
- **Scikit-learn** — ML models and pipelines
- **Pandas & NumPy** — Data processing
- **Joblib** — Model serialization

### Frontend
- **Streamlit** — Interactive dashboard
- **Plotly** — Interactive visualizations

### Data & Reporting
- **Faker** — Synthetic transaction generation
- **ReportLab** — PDF report generation

---

## Project Structure

```
lifeos-ai-finance/
│
├── backend/
│   └── app/
│       └── main.py
│
├── frontend/
│   └── app.py
│
├── ml_models/
│   ├── categorizer/
│   ├── fraud_detector/
│   ├── forecaster/
│   ├── clustering/
│   └── advisor/
│
├── data/
│   ├── transactions.csv
│   └── test_upload.csv
│
├── uploads/
│
├── scripts/
│   └── generate_dataset.py
│
├── screenshots/
│
├── requirements.txt
└── README.md
```

---

## Installation

### Prerequisites

- Python 3.9+
- pip

### 1. Clone the Repository

```bash
git clone <https://github.com/kavyasruthi58/lifeos-ai-finance.git>
cd lifeos-ai-finance
```

### 2. Create a Virtual Environment

```bash
# macOS / Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python3 -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Running the Application

### Start the FastAPI Backend

```bash
python -m uvicorn backend.app.main:app --reload
```

| Resource | URL |
|---|---|
| API Base | http://127.0.0.1:8000 |
| Swagger Docs | http://127.0.0.1:8000/docs |

### Start the Streamlit Dashboard

```bash
streamlit run frontend/app.py
```

| Resource | URL |
|---|---|
| Dashboard | http://localhost:8501 |

---

## API Reference

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/predict/category` | Classify transactions |
| `POST` | `/predict/fraud` | Fraud prediction |
| `POST` | `/predict/budget` | Spending forecast |
| `GET` | `/advisor/summary` | AI recommendations |
| `GET` | `/health` | API health check |

---

## Dashboard

The Streamlit dashboard provides a complete AI-powered financial analytics experience:

- User-level financial analytics
- Interactive category & date filtering
- CSV upload support
- Spending distribution charts
- Monthly spending trend analysis
- Fraud detection alerts
- AI-generated financial recommendations
- Downloadable CSV & PDF financial reports
- Multi-user transaction analytics

### Screenshots

![Dashboard Overview](screenshots/Dashboard_1.png)
![Analytics View](screenshots/Dashboard_2.png)
![Detailed Report](screenshots/Dashboard_3.png)
![CSV Upload & PDF Report](screenshots/CSV_PDF.png)

---

## Roadmap

Planned enhancements for future releases:

- [ ] BERT-based NLP transaction categorization
- [ ] XGBoost fraud detection
- [ ] LSTM / Prophet time-series forecasting
- [ ] OpenAI / Groq-powered AI assistant
- [ ] PostgreSQL database integration
- [ ] Docker containerization
- [ ] AWS cloud deployment
- [ ] Apache Kafka real-time streaming pipeline
- [ ] Login & authentication system
- [ ] Multi-user role-based analytics
- [ ] Real-time fraud alerts
- [ ] AI financial chatbot

---

<div align="center">

Built as part of the **LifeOS AI** initiative — an AI ecosystem focused on intelligent life management, behavioral analytics, and human-centered AI systems.

</div>