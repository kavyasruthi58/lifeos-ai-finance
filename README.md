LifeOS AI — Personal Finance Intelligence Platform

An AI-powered personal finance analytics platform combining machine learning, REST APIs, interactive dashboards, fraud detection, downloadable reports, and AI-generated financial insights to help users make smarter financial decisions.

⸻

Table of Contents

* Overview￼
* Features￼
* Machine Learning Models￼
* Tech Stack￼
* Project Structure￼
* Installation￼
* Running the Application￼
* API Reference￼
* Dashboard￼
* Dashboard Screenshots￼
* Roadmap￼

⸻

Overview

LifeOS AI is a full-stack fintech analytics system that combines machine learning, backend APIs, intelligent financial insights, and interactive data visualization to deliver actionable personal finance intelligence.

The platform supports dynamic transaction uploads, fraud analysis, AI-generated recommendations, downloadable financial reports, and multi-user financial analytics. It serves as the financial intelligence layer of the broader LifeOS AI ecosystem — an AI platform focused on intelligent life management and behavioral analytics.

⸻

Features

Smart Transaction Categorization

Automatically classifies transaction descriptions into meaningful categories using NLP-based machine learning.

Input Description	Predicted Category
DOORDASH PURCHASE	Food
UBER TRIP	Transport
NETFLIX PAYMENT	Entertainment
WHOLE FOODS MARKET	Groceries

Supported categories:
Food · Groceries · Shopping · Entertainment · Transport · Health · Subscription

⸻

Fraud Detection

Detects suspicious transactions using anomaly detection, flagging:

* High-value or unusual transactions
* Purchases from unknown merchants
* Abnormal spending patterns
* Potential fraudulent activity

Example: UNKNOWN ONLINE PAYMENT — $950.00 → ⚠️ Fraud Alert

⸻

Budget Forecasting

Predicts future spending trends to help users stay ahead of their finances:

* Monthly spending trend analysis
* Spending behavior tracking
* Budget overrun insights
* Forward-looking financial analytics

⸻

Spending Pattern Analysis

Clusters users into spending profiles using unsupervised machine learning.

Profile	Description
High Spender	Consistently above-average transaction amounts
Food-Heavy	Majority of spend in dining and groceries
Subscription-Heavy	High recurring monthly charges
Balanced	Evenly distributed spending behavior

⸻

AI Financial Advisor

Generates personalized financial recommendations based on spending behavior:

* Reduce shopping expenses
* Lower subscription costs
* Improve savings rate
* Detect unusual spending trends
* Suggest financial optimization strategies

⸻

CSV Upload Support

Users can upload custom transaction datasets directly into the dashboard for real-time analysis and visualization.

⸻

Downloadable Financial Reports

Generate downloadable:

* Transaction CSV reports
* Financial summary CSV reports
* Professional PDF financial reports

⸻

Interactive Multi-User Analytics

Analyze financial behavior using:

* User-level filtering
* Date filtering
* Category filtering
* Fraud-user tracking
* Dynamic dashboard updates

⸻

Machine Learning Models

Module	Algorithm
Transaction Categorization	TF-IDF + Logistic Regression
Fraud Detection	Isolation Forest
Budget Forecasting	Linear Regression
Spending Pattern Analysis	K-Means Clustering
Financial Advisor	Rule-Based AI Engine

⸻

Tech Stack

Backend

* FastAPI — REST API framework
* Uvicorn — ASGI server
* Python 3.9+

Machine Learning

* Scikit-learn — ML models and pipelines
* Pandas & NumPy — Data processing
* Joblib — Model serialization

Frontend

* Streamlit — Interactive dashboard
* Plotly — Interactive visualizations

Data Generation

* Faker — Synthetic transaction generation

Reporting & Utilities

* ReportLab — PDF report generation

⸻

Project Structure

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

⸻

Installation

Prerequisites

* Python 3.9+
* pip

⸻

Clone Repository

git clone <your-repository-url>
cd lifeos-ai-finance

⸻

Create Virtual Environment

python3 -m venv venv
source venv/bin/activate

Windows:

venv\Scripts\activate

⸻

Install Dependencies

pip install -r requirements.txt

⸻

Running the Application

Start FastAPI Backend

python -m uvicorn backend.app.main:app --reload

API:
http://127.0.0.1:8000

Swagger Docs:
http://127.0.0.1:8000/docs

⸻

Start Streamlit Dashboard

streamlit run frontend/app.py

Dashboard:
http://localhost:8501

⸻

API Reference

Method	Endpoint	Description
POST	/predict/category	Classify transactions
POST	/predict/fraud	Fraud prediction
POST	/predict/budget	Spending forecast
GET	/advisor/summary	AI recommendations
GET	/health	API health check

⸻

Dashboard

The Streamlit dashboard provides a complete AI-powered financial analytics experience:

* User-level financial analytics
* Interactive category filtering
* CSV upload support
* Spending distribution charts
* Monthly spending trend analysis
* Fraud detection alerts
* AI-generated financial recommendations
* Downloadable CSV reports
* Downloadable PDF financial reports
* Multi-user transaction analytics

⸻

Dashboard Screenshots
![Dashboard_1.png](screenshots/Dashboard_1.png)
![Dashboard_2.png](screenshots/Dashboard_2.png)
![Dashboard_3.png](screenshots/Dashboard_3.png)




CSV Upload Feature & PDF Financial Report
![CSV_PDF.png](screenshots/CSV_PDF.png)


⸻

Roadmap

Planned future enhancements:

* BERT-based NLP categorization
* XGBoost fraud detection
* LSTM / Prophet forecasting
* OpenAI / Groq-powered AI assistant
* PostgreSQL database integration
* Docker containerization
* AWS deployment
* Apache Kafka streaming pipeline
* Login authentication system
* Multi-user role-based analytics
* Real-time fraud alerts
* AI financial chatbot

⸻

Built as part of the LifeOS AI initiative — an AI ecosystem focused on intelligent life management, behavioral analytics, and human-centered AI systems.

: