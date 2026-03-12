# DSP_Price_Forecasting
A Forecasting platform for predict upcoming wheat price

# 🌾 India Wheat Price Forecasting Dashboard

A Streamlit-based forecasting system that predicts **next‑month India wheat prices** using a **GRU deep learning model**, enriched with **live economic indicators** from the FRED API and robust fallback mechanisms.

This dashboard supports:
- 📈 Forecasting  
- ⚡ Scenario simulation  
- 🔎 Data exploration  
- 📡 Live data diagnostics  
- 🧠 GRU-based time‑series modelling  

---

## 🚀 Features

### **1. Live + Fallback Hybrid Data System**
The app fetches real-time values from the **FRED API**:
- WTI Oil Price (`DCOILWTICO`)
- USD/INR Exchange Rate (`DEXINUS`)
- Fertiliser Index (`PCU3253132531`)

If live data is unavailable, the system automatically falls back to the **latest historical dataset values**.

### **2. GRU Deep Learning Model**
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

### **3. Multi‑Page Streamlit Dashboard**
- **Home** – Overview + recent trends  
- **Forecast** – Predict next‑month wheat price  
- **Scenario Simulation** – Apply shocks (oil spike, rainfall drop, INR depreciation, etc.)  
- **Data Explorer** – Visualise historical variables  
- **Live Data Status** – See live vs fallback values with timestamps  
- **About** – Project summary  

---
Owned by HARMINDER SINGH
