# LifeOS AI — Personal Finance Intelligence Platform

> An AI-powered personal finance analytics platform combining machine learning, REST APIs, and an interactive dashboard to help users understand spending behavior, detect fraud, and make smarter financial decisions.

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
- [Screenshots](#screenshots)
- [Roadmap](#roadmap)
- [Author](#author)

---

## Overview

LifeOS AI is a full-stack fintech analytics system that brings together machine learning, backend APIs, and data visualization to deliver actionable personal finance insights. It serves as the financial intelligence layer of the broader **LifeOS AI** ecosystem — an AI platform focused on intelligent life management and behavioral analytics.

---

## Features

### Smart Transaction Categorization
Automatically classifies transaction descriptions into meaningful categories using NLP-based machine learning.

| Input Description | Predicted Category |
|---|---|
| `DOORDASH PURCHASE` | Food |
| `UBER TRIP` | Transport |
| `NETFLIX PAYMENT` | Entertainment |
| `WHOLE FOODS MARKET` | Groceries |

Supported categories: `Food` · `Groceries` · `Shopping` · `Entertainment` · `Transport` · `Health` · `Subscription`

---

### Fraud Detection
Detects suspicious transactions using anomaly detection, flagging:
- High-value or unusual transactions
- Purchases from unknown merchants
- Abnormal spending patterns
- Potential fraudulent activity

**Example:** `UNKNOWN ONLINE PAYMENT — $950.00` → ⚠️ Fraud Alert

---

### Budget Forecasting
Predicts future spending trends to help users stay ahead of their finances:
- Monthly spending trend analysis
- Budget overrun warnings
- Forward-looking financial behavior insights

---

### Spending Pattern Analysis
Clusters users into spending profiles using unsupervised machine learning:

| Profile | Description |
|---|---|
| High Spender | Consistently above-average transaction amounts |
| Food-Heavy | Majority of spend in dining and groceries |
| Subscription-Heavy | High recurring monthly charges |
| Balanced | Evenly distributed across all categories |

---

### AI Financial Advisor
Generates personalized financial recommendations based on individual spending behavior:
- Reduce shopping expenses by 10%
- Lower subscription costs
- Improve monthly savings rate
- Flag unusual spending categories for review

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

**Backend**
- [FastAPI](https://fastapi.tiangolo.com/) — REST API framework
- [Uvicorn](https://www.uvicorn.org/) — ASGI server
- Python 3.9+

**Machine Learning**
- [Scikit-learn](https://scikit-learn.org/) — ML models and pipelines
- [Pandas](https://pandas.pydata.org/) & [NumPy](https://numpy.org/) — Data processing
- [Joblib](https://joblib.readthedocs.io/) — Model serialization

**Frontend**
- [Streamlit](https://streamlit.io/) — Interactive dashboard
- [Plotly](https://plotly.com/) — Data visualizations

**Data Generation**
- [Faker](https://faker.readthedocs.io/) — Synthetic transaction data

---

## Project Structure

```
lifeos-ai-finance/
│
├── backend/
│   └── app/
│       └── main.py               # FastAPI application and route definitions
│
├── frontend/
│   └── app.py                    # Streamlit dashboard
│
├── ml_models/
│   ├── categorizer/              # TF-IDF + Logistic Regression model
│   ├── fraud_detector/           # Isolation Forest model
│   ├── forecaster/               # Linear Regression model
│   ├── clustering/               # K-Means clustering model
│   └── advisor/                  # Rule-based financial advisor
│
├── data/
│   └── transactions.csv          # Generated transaction dataset
│
├── scripts/
│   └── generate_dataset.py       # Synthetic data generation script
│
├── screenshots/                  # Dashboard and API screenshots
├── requirements.txt
└── README.md
```

---

## Installation

### Prerequisites
- Python 3.9 or higher
- pip

### Steps

**1. Clone the repository**
```bash
git clone <your-repository-url>
cd lifeos-ai-finance
```

**2. Create and activate a virtual environment**
```bash
python3 -m venv venv
source venv/bin/activate       # macOS / Linux
venv\Scripts\activate          # Windows
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

---

## Running the Application

### Start the FastAPI Backend

```bash
python -m uvicorn backend.app.main:app --reload
```

The API will be available at: `http://127.0.0.1:8000`  
Interactive API docs (Swagger UI): `http://127.0.0.1:8000/docs`

---

### Start the Streamlit Dashboard

```bash
streamlit run frontend/app.py
```

The dashboard will be available at: `http://localhost:8501`

---

## API Reference

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/predict/category` | Classify a transaction into a spending category |
| `POST` | `/predict/fraud` | Check a transaction for fraudulent indicators |
| `POST` | `/predict/budget` | Forecast future spending based on history |
| `GET` | `/advisor/summary` | Generate personalized financial recommendations |
| `GET` | `/health` | API health check |

Full interactive documentation is available via Swagger UI at `/docs` when the backend is running.

---

## Dashboard

The Streamlit dashboard provides a complete view of personal finances:

- **Overview** — User-level spending summary and key metrics
- **Spending Distribution** — Category-wise breakdown with charts
- **Monthly Trends** — Time-series analysis of spending behavior
- **Fraud Alerts** — Real-time display of flagged transactions
- **AI Insights** — Personalized financial recommendations
- **Interactive Filters** — Filter by date range, category, and user

---

## Dashboard Screenshots
![Dashboard_1.png](screenshots/Dashboard_1.png)
![Dashboard_2.png](screenshots/Dashboard_2.png)
![Dashboard_3.png](screenshots/Dashboard_3.png)
---

## Roadmap

Planned enhancements for future releases:

- [ ] BERT-based NLP for improved transaction categorization
- [ ] XGBoost fraud detection with higher precision
- [ ] LSTM / Prophet time-series forecasting
- [ ] OpenAI / Groq-powered conversational financial advisor
- [ ] PostgreSQL database integration
- [ ] Docker containerization
- [ ] AWS cloud deployment
- [ ] Real-time streaming with Apache Kafka
- [ ] User authentication and multi-user support

---

> Built as part of the **LifeOS AI** initiative — an AI ecosystem focused on intelligent life management, behavioral analytics, and human-centered AI systems.