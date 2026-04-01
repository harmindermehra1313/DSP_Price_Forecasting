# DSP_Price_Forecasting

A Forecasting platform to predict upcoming wheat prices.

# 🌾 India Wheat Price Forecasting Dashboard

A Streamlit-based forecasting system that predicts **next‑month India wheat prices** using a **GRU deep learning model**, enriched with **live economic indicators** from the FRED API and robust fallback mechanisms.

This dashboard supports:
- 📈 Forecasting  
- ⚡ Scenario simulation  
- 🔎 Data exploration  
- 📡 Live data diagnostics  
- 🧠 GRU-based time‑series modelling  

---

> **From original README:**  
> "A Streamlit-based forecasting system that predicts **next‑month India wheat prices** using a **GRU deep learning model**, enriched with **live economic indicators** from the FRED API and robust fallback mechanisms."  
> "This dashboard supports: - 📈 Forecasting - ⚡ Scenario simulation - 🔎 Data exploration - 📡 Live data diagnostics - 🧠 GRU-based time‑series modelling"

---

## 🚀 What’s new in this version

- Cleaned and expanded **installation** and **run** instructions.  
- Clear **screenshot checklist** for dissertation figures (what to capture).  
- Full **project structure** included for reproducibility.  
- Guidance on **image citation** and figure captioning for your report.  
- Minor wording and formatting improvements for clarity.

---

## Features

### 1. Live + Fallback Hybrid Data System
The app fetches real-time values from the **FRED API**:
- WTI Oil Price (`DCOILWTICO`)  
- USD/INR Exchange Rate (`DEXINUS`)  
- Fertiliser Index (`PCU3253132531`)

If live data is unavailable, the system automatically falls back to the **latest historical dataset values**.

### 2. GRU Deep Learning Model
The model is trained on:
- Global wheat prices  
- Oil prices  
- Rainfall  
- Temperature  
- Conflict events  
- Fertiliser index  
- FAO cereals index  
- GEPU index

Feature engineering includes:
- Lags  
- Rolling windows  
- Volatility  
- Scaling  
- Temporal structure

### 3. Multi‑Page Streamlit Dashboard
- **Home** – Overview + recent trends  
- **Forecast** – Predict next‑month wheat price (prediction card, inputs, interpretation, historical chart)  
- **Scenario Simulation** – Apply shocks and compare baseline vs scenario  
- **Data Explorer** – Visualise historical variables and inspect recent data row  
- **Live Data Status** – See live vs fallback values with timestamps  
- **About** – Project summary and usage notes

---

## Installation

**Requirements**
- Python 3.9+  
- `venv` or other virtual environment recommended

**Install**
```bash
# create and activate virtual environment
python -m venv venv
# macOS / Linux
source venv/bin/activate
# Windows
venv\Scripts\activate

# install dependencies
pip install -r wheat_forecasting_app/requirements.txt
```
**Run the app**
```bash
cd "D:\UWE YEAR 3\Digital Systems Project\App\DSP_Price_Forecasting\wheat_forecasting_app"
streamlit run app.py
```

**Files you must keep in place**

- data/historical/master_monthly.parquet — historical dataset used for fallbacks and baseline.

- model/ — saved model and scaler files loaded by model.load_model.load_all.

- wheat_forecasting_app/.env — API keys (FRED) and environment variables.

- wheat_forecasting_app/assets/ — optional images and CSS used by the app.

**Project Structure**
```
D:.
│   README.md
│
├───.devcontainer
│       devcontainer.json
│
├───Traning files
│       cnn_lstm_model_20260310_193606.keras
│       merge_datasets_03_03.ipynb
│       merge_datasets_03_03.pdf
│       Testing_model.ipynb
│       Training10_03-cnn-lstm.ipynb
│       Training10_03-GRU.ipynb
│       Training_LSTM.ipynb
│
└───wheat_forecasting_app
    │   .env
    │   .gitignore
    │   app.py
    │   requirements.txt
    │
    ├───api
    │   │   forecast_api.py
    │   │
    │   └───__pycache__
    │
    ├───assets
    │   │   logo.png
    │   │
    │   ├───css
    │   │       styles.css
    │   │
    │   └───images
    ├───config
    │   │   api_keys.py
    │   │   settings.py
    │
    ├───data
    │   ├───historical
    │   │       master_monthly.parquet
    │   │
    │   └───live_cache
    │           latest_values.json
    │
    ├───features
    │   │   compute_lags.py
    │   │   compute_rolling.py
    │   │   compute_volatility.py
    │   │   feature_pipeline.py
    │   │   preprocess.py
    │
    ├───model
    │   │   feature_columns.json
    │   │   feature_scaler.pkl
    │   │   gru_model_20260310_194421.h5
    │   │   gru_model_20260310_194421.keras
    │   │   load_model.py
    │   │   predict.py
    │   │   target_scaler.pkl
    │
    └───utils
            api_client.py
            cache.py
            logger.py

```

**Troubleshooting**
- Model fails to load: ensure wheat_forecasting_app/model/ contains gru_model_*.keras and scaler .pkl files.

- Live API errors: check .env for valid FRED API key and network connectivity.

- Missing data file: ensure data/historical/master_monthly.parquet exists and is readable.

**Note**
For reproducibility, include the exact environment used `(Python version, requirements.txt)` and any training notebooks from `Traning files/` if you need to retrain or inspect model training steps.

## License & Ownership
Owned by ***Harminder Singh.***