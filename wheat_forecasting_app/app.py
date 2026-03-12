# import streamlit as st
# import pandas as pd

# from model.load_model import load_all
# from model.predict import GRUPredictor
# from features.preprocess import preprocess_raw_data
# from features.feature_pipeline import build_feature_pipeline

# # ------------------------------------------------------------
# # PAGE CONFIG
# # ------------------------------------------------------------
# st.set_page_config(page_title="Wheat Price Forecasting Dashboard", layout="wide")

# # ------------------------------------------------------------
# # SIDEBAR NAVIGATION
# # ------------------------------------------------------------
# st.sidebar.title("📌 Navigation")
# page = st.sidebar.radio("Go to", ["Home", "Forecast", "Scenario Simulation", "Data Explorer", "About"])

# # ------------------------------------------------------------
# # LOAD DATA + MODEL
# # ------------------------------------------------------------
# MASTER_PATH = "data/historical/master_monthly.parquet"

# df_master = pd.read_parquet(MASTER_PATH)
# df_master["month"] = pd.to_datetime(df_master["month"])
# df_master = df_master.set_index("month")
# # FIX NAN IN MASTER DATA BEFORE SIDEBAR USES IT
# df_master["rainfall"] = df_master["rainfall"].fillna(df_master["rainfall"].mean())
# df_master["temperature"] = df_master["temperature"].fillna(df_master["temperature"].mean())
# # FIX NAN USING SEASONAL AVERAGES (REALISTIC)
# # df_master["rainfall"] = df_master["rainfall"].fillna(
# #     df_master["rainfall"].groupby(df_master.index.month).transform("mean")
# # )

# # df_master["temperature"] = df_master["temperature"].fillna(
# #     df_master["temperature"].groupby(df_master.index.month).transform("mean")
# # )
# last_row = df_master.iloc[-1]

# model, feature_scaler, target_scaler, feature_columns = load_all()

# # ------------------------------------------------------------
# # FUNCTION: SIDEBAR INPUTS (shared across pages)
# # ------------------------------------------------------------
# def get_sidebar_inputs(last_row):
#     st.sidebar.subheader("Scenario Inputs")

#     oil_price = st.sidebar.number_input("Oil Price (WTI)", value=float(last_row["oil_price"]))
#     usd_inr = st.sidebar.number_input("USD/INR", value=float(last_row["usd_inr"]))
#     rainfall = st.sidebar.number_input("Rainfall (mm)", value=float(last_row["rainfall"]))
#     conflict_events = st.sidebar.number_input("Conflict Events", value=float(last_row["conflict_events"]))
#     fertiliser_index = st.sidebar.number_input("Fertiliser Index", value=float(last_row["fertiliser_index"]))
#     temperature = st.sidebar.number_input("Temperature (°C)", value=float(last_row["temperature"]))

#     return {
#         "oil_price": oil_price,
#         "usd_inr": usd_inr,
#         "rainfall": rainfall,
#         "conflict_events": conflict_events,
#         "fertiliser_index": fertiliser_index,
#         "temperature": temperature,
#         # Keep other features unchanged
#         "gepu": last_row["gepu"],
#         "global_wheat_price": last_row["global_wheat_price"],
#         "fao_cereals": last_row["fao_cereals"],
#     }

# # ------------------------------------------------------------
# # PAGE 1 — HOME
# # ------------------------------------------------------------
# if page == "Home":
#     st.title("🌾 Wheat Price Forecasting Dashboard")

#     st.markdown("""
#     Welcome to the **India Wheat Price Forecasting Dashboard**.  
#     This tool uses a **GRU deep learning model** trained on economic, climatic, and global market indicators to forecast next‑month wheat prices.

#     ### 🔍 What this dashboard offers
#     - **Forecast**: Predict next‑month wheat prices using real‑time inputs  
#     - **Scenario Simulation**: Test shocks like oil spikes, rainfall drops, or currency depreciation  
#     - **Data Explorer**: Visualise historical trends  
#     - **About**: Learn how the model works  

#     ### 📘 Who is this for?
#     - Students  
#     - Researchers  
#     - Policymakers  
#     - Farmers  
#     - Anyone curious about food price forecasting  

#     ### 📊 Key Drivers of Wheat Prices
#     - Global wheat prices  
#     - Oil prices (transportation cost)  
#     - Rainfall (crop yield)  
#     - Conflict events (supply chain disruption)  
#     - USD/INR exchange rate  
#     - Fertiliser index  
#     - Temperature  
#     """)

#     st.subheader("Recent Wheat Price Trend")
#     st.line_chart(df_master["india_price"].tail(36))

# # ------------------------------------------------------------
# # PAGE 2 — FORECAST
# # ------------------------------------------------------------
# elif page == "Forecast":
#     st.title("📈 Wheat Price Forecast")

#     live_dict = get_sidebar_inputs(last_row)

#     df_raw = preprocess_raw_data(MASTER_PATH, live_dict)
#     df_features = build_feature_pipeline(df_raw)

#     predictor = GRUPredictor(model, feature_scaler, target_scaler, feature_columns)
#     result = predictor.predict(df_features)

#     col1, col2 = st.columns(2)

#     with col1:
#         st.metric("Next Month Price (₹/Quintal)", f"{result['predicted_price']:.2f}")

#     with col2:
#         st.metric("Predicted Return", f"{result['predicted_return']:.4f}")

#     st.subheader("📉 Historical Price Trend")
#     st.line_chart(df_raw["india_price"])

#     st.markdown("""
#     ### 🧠 How to interpret this forecast
#     - A **positive return** means prices are expected to rise  
#     - A **negative return** means prices may fall  
#     - The model considers **36 engineered features**, including lags, rolling averages, volatility, and global indicators  
#     """)

# # ------------------------------------------------------------
# # PAGE 3 — SCENARIO SIMULATION
# # ------------------------------------------------------------
# elif page == "Scenario Simulation":
#     st.title("⚡ Scenario Simulation")

#     st.markdown("""
#     Test how shocks affect next‑month wheat prices.  
#     Choose a scenario below to see the impact.
#     """)

#     live_dict = get_sidebar_inputs(last_row)

#     scenario = st.selectbox("Choose a scenario", [
#         "Oil Spike (+40%)",
#         "Rainfall Drop (-30%)",
#         "INR Depreciation (+10%)",
#         "Conflict Surge (+50%)",
#         "Temperature Heatwave (+3°C)"
#     ])

#     shock_dict = live_dict.copy()

#     if scenario == "Oil Spike (+40%)":
#         shock_dict["oil_price"] *= 1.4
#     elif scenario == "Rainfall Drop (-30%)":
#         shock_dict["rainfall"] *= 0.7
#     elif scenario == "INR Depreciation (+10%)":
#         shock_dict["usd_inr"] *= 1.1
#     elif scenario == "Conflict Surge (+50%)":
#         shock_dict["conflict_events"] *= 1.5
#     elif scenario == "Temperature Heatwave (+3°C)":
#         shock_dict["temperature"] += 3

#     df_shock = preprocess_raw_data(MASTER_PATH, shock_dict)
#     df_shock_features = build_feature_pipeline(df_shock)

#     predictor = GRUPredictor(model, feature_scaler, target_scaler, feature_columns)
#     shock_result = predictor.predict(df_shock_features)

#     st.metric("Scenario Forecasted Price", f"{shock_result['predicted_price']:.2f}")

#     st.markdown("""
#     ### 📘 Interpretation
#     - This shows how a **single shock** affects next‑month wheat prices  
#     - Useful for **policy analysis**, **risk assessment**, and **market planning**  
#     """)

# # ------------------------------------------------------------
# # PAGE 4 — DATA EXPLORER
# # ------------------------------------------------------------
# elif page == "Data Explorer":
#     st.title("🔎 Data Explorer")

#     st.markdown("Explore historical trends across key variables.")

#     selected_cols = st.multiselect(
#         "Choose variables to plot",
#         df_master.columns.tolist(),
#         default=["india_price", "oil_price", "usd_inr"]
#     )

#     st.line_chart(df_master[selected_cols].tail(120))

# # ------------------------------------------------------------
# # PAGE 5 — ABOUT
# # ------------------------------------------------------------
# elif page == "About":
#     st.title("ℹ️ About This Project")

#     st.markdown("""
#     This dashboard forecasts India wheat prices using a **GRU neural network** trained on:
#     - global wheat prices  
#     - oil prices  
#     - rainfall  
#     - conflict events  
#     - fertiliser index  
#     - temperature  
#     - FAO cereals index  
#     - GEPU index  

#     ### 🎯 Model Goal
#     To provide **transparent**, **interpretable**, and **scenario‑driven** wheat price forecasts.

#     ### 📉 Why GRU?
#     GRUs handle:
#     - long‑term dependencies  
#     - seasonality  
#     - lagged effects  
#     - noisy economic signals  

#     ### 🧩 Limitations
#     - Forecasts are **probabilistic**, not guarantees  
#     - Extreme shocks may behave unpredictably  
#     - Model depends on data quality  
#     """)

# import streamlit as st
# import pandas as pd

# from model.load_model import load_all
# from model.predict import GRUPredictor
# from features.preprocess import preprocess_raw_data
# from features.feature_pipeline import build_feature_pipeline
# from utils.api_client import fetch_fred_latest

# # ------------------------------------------------------------
# # PAGE CONFIG
# # ------------------------------------------------------------
# st.set_page_config(page_title="Wheat Price Forecasting Dashboard", layout="wide")

# # ------------------------------------------------------------
# # SIDEBAR NAVIGATION
# # ------------------------------------------------------------
# st.sidebar.title("📌 Navigation")
# page = st.sidebar.radio("Go to", ["Home", "Forecast", "Scenario Simulation", "Data Explorer", "About"])

# # ------------------------------------------------------------
# # LOAD DATA + MODEL
# # ------------------------------------------------------------
# MASTER_PATH = "data/historical/master_monthly.parquet"

# df_master = pd.read_parquet(MASTER_PATH)
# df_master["month"] = pd.to_datetime(df_master["month"])
# df_master = df_master.set_index("month")

# # FIX NAN USING SEASONAL AVERAGES (REALISTIC)
# df_master["rainfall"] = df_master["rainfall"].fillna(
#     df_master["rainfall"].groupby(df_master.index.month).transform("mean")
# )
# df_master["temperature"] = df_master["temperature"].fillna(
#     df_master["temperature"].groupby(df_master.index.month).transform("mean")
# )

# last_row = df_master.iloc[-1]

# model, feature_scaler, target_scaler, feature_columns = load_all()

# # ------------------------------------------------------------
# # HELPERS: LIVE + FALLBACK
# # ------------------------------------------------------------
# def safe_fetch(fetch_func, fallback):
#     try:
#         val = fetch_func()
#         if val is None or pd.isna(val):
#             return fallback
#         return val
#     except Exception:
#         return fallback

# def get_live_defaults(last_row: pd.Series) -> dict:
#     # FRED series IDs
#     oil_live = lambda: fetch_fred_latest("DCOILWTICO")      # WTI oil
#     fx_live = lambda: fetch_fred_latest("DEXINUS")          # USD/INR
#     fert_live = lambda: fetch_fred_latest("PCU3253132531")  # Fertiliser index

#     return {
#         "oil_price": safe_fetch(oil_live, last_row["oil_price"]),
#         "usd_inr": safe_fetch(fx_live, last_row["usd_inr"]),
#         "fertiliser_index": safe_fetch(fert_live, last_row["fertiliser_index"]),
#         # no live APIs wired → fallback only
#         "rainfall": last_row["rainfall"],
#         "temperature": last_row["temperature"],
#         "conflict_events": last_row["conflict_events"],
#         "gepu": last_row["gepu"],
#         "global_wheat_price": last_row["global_wheat_price"],
#         "fao_cereals": last_row["fao_cereals"],
#     }

# # ------------------------------------------------------------
# # FUNCTION: SIDEBAR INPUTS (shared across pages)
# # ------------------------------------------------------------
# def get_sidebar_inputs(last_row):
#     st.sidebar.subheader("Scenario Inputs")

#     base = get_live_defaults(last_row)

#     oil_price = st.sidebar.number_input("Oil Price (WTI)", value=float(base["oil_price"]))
#     usd_inr = st.sidebar.number_input("USD/INR", value=float(base["usd_inr"]))
#     rainfall = st.sidebar.number_input("Rainfall (mm)", value=float(base["rainfall"]))
#     conflict_events = st.sidebar.number_input("Conflict Events", value=float(base["conflict_events"]))
#     fertiliser_index = st.sidebar.number_input("Fertiliser Index", value=float(base["fertiliser_index"]))
#     temperature = st.sidebar.number_input("Temperature (°C)", value=float(base["temperature"]))

#     return {
#         "oil_price": oil_price,
#         "usd_inr": usd_inr,
#         "rainfall": rainfall,
#         "conflict_events": conflict_events,
#         "fertiliser_index": fertiliser_index,
#         "temperature": temperature,
#         # Keep other features unchanged
#         "gepu": last_row["gepu"],
#         "global_wheat_price": last_row["global_wheat_price"],
#         "fao_cereals": last_row["fao_cereals"],
#     }

# # ------------------------------------------------------------
# # PAGE 1 — HOME
# # ------------------------------------------------------------
# if page == "Home":
#     st.title("🌾 Wheat Price Forecasting Dashboard")

#     st.markdown("""
#     Welcome to the **India Wheat Price Forecasting Dashboard**.  
#     This tool uses a **GRU deep learning model** trained on economic, climatic, and global market indicators to forecast next‑month wheat prices.

#     ### 🔍 What this dashboard offers
#     - **Forecast**: Predict next‑month wheat prices using real‑time inputs  
#     - **Scenario Simulation**: Test shocks like oil spikes, rainfall drops, or currency depreciation  
#     - **Data Explorer**: Visualise historical trends  
#     - **About**: Learn how the model works  

#     ### 📘 Who is this for?
#     - Students  
#     - Researchers  
#     - Policymakers  
#     - Farmers  
#     - Anyone curious about food price forecasting  

#     ### 📊 Key Drivers of Wheat Prices
#     - Global wheat prices  
#     - Oil prices (transportation cost)  
#     - Rainfall (crop yield)  
#     - Conflict events (supply chain disruption)  
#     - USD/INR exchange rate  
#     - Fertiliser index  
#     - Temperature  
#     """)

#     st.subheader("Recent Wheat Price Trend")
#     st.line_chart(df_master["india_price"].tail(36))

# # ------------------------------------------------------------
# # PAGE 2 — FORECAST
# # ------------------------------------------------------------
# elif page == "Forecast":
#     st.title("📈 Wheat Price Forecast")

#     live_dict = get_sidebar_inputs(last_row)

#     df_raw = preprocess_raw_data(MASTER_PATH, live_dict)
#     df_features = build_feature_pipeline(df_raw)

#     predictor = GRUPredictor(model, feature_scaler, target_scaler, feature_columns)
#     result = predictor.predict(df_features)

#     col1, col2 = st.columns(2)

#     with col1:
#         st.metric("Next Month Price (₹/Quintal)", f"{result['predicted_price']:.2f}")

#     with col2:
#         st.metric("Predicted Return", f"{result['predicted_return']:.4f}")

#     st.subheader("📉 Historical Price Trend")
#     st.line_chart(df_raw["india_price"])

#     st.markdown("""
#     ### 🧠 How to interpret this forecast
#     - A **positive return** means prices are expected to rise  
#     - A **negative return** means prices may fall  
#     - The model considers **36 engineered features**, including lags, rolling averages, volatility, and global indicators  
#     """)

# # ------------------------------------------------------------
# # PAGE 3 — SCENARIO SIMULATION
# # ------------------------------------------------------------
# elif page == "Scenario Simulation":
#     st.title("⚡ Scenario Simulation")

#     st.markdown("""
#     Test how shocks affect next‑month wheat prices.  
#     Choose a scenario below to see the impact.
#     """)

#     live_dict = get_sidebar_inputs(last_row)

#     scenario = st.selectbox("Choose a scenario", [
#         "Oil Spike (+40%)",
#         "Rainfall Drop (-30%)",
#         "INR Depreciation (+10%)",
#         "Conflict Surge (+50%)",
#         "Temperature Heatwave (+3°C)"
#     ])

#     shock_dict = live_dict.copy()

#     if scenario == "Oil Spike (+40%)":
#         shock_dict["oil_price"] *= 1.4
#     elif scenario == "Rainfall Drop (-30%)":
#         shock_dict["rainfall"] *= 0.7
#     elif scenario == "INR Depreciation (+10%)":
#         shock_dict["usd_inr"] *= 1.1
#     elif scenario == "Conflict Surge (+50%)":
#         shock_dict["conflict_events"] *= 1.5
#     elif scenario == "Temperature Heatwave (+3°C)":
#         shock_dict["temperature"] += 3

#     df_shock = preprocess_raw_data(MASTER_PATH, shock_dict)
#     df_shock_features = build_feature_pipeline(df_shock)

#     predictor = GRUPredictor(model, feature_scaler, target_scaler, feature_columns)
#     shock_result = predictor.predict(df_shock_features)

#     st.metric("Scenario Forecasted Price", f"{shock_result['predicted_price']:.2f}")

#     st.markdown("""
#     ### 📘 Interpretation
#     - This shows how a **single shock** affects next‑month wheat prices  
#     - Useful for **policy analysis**, **risk assessment**, and **market planning**  
#     """)

# # ------------------------------------------------------------
# # PAGE 4 — DATA EXPLORER
# # ------------------------------------------------------------
# elif page == "Data Explorer":
#     st.title("🔎 Data Explorer")

#     st.markdown("Explore historical trends across key variables.")

#     selected_cols = st.multiselect(
#         "Choose variables to plot",
#         df_master.columns.tolist(),
#         default=["india_price", "oil_price", "usd_inr"]
#     )

#     st.line_chart(df_master[selected_cols].tail(120))

# # ------------------------------------------------------------
# # PAGE 5 — ABOUT
# # ------------------------------------------------------------
# elif page == "About":
#     st.title("ℹ️ About This Project")

#     st.markdown("""
#     This dashboard forecasts India wheat prices using a **GRU neural network** trained on:
#     - global wheat prices  
#     - oil prices  
#     - rainfall  
#     - conflict events  
#     - fertiliser index  
#     - temperature  
#     - FAO cereals index  
#     - GEPU index  

#     ### 🎯 Model Goal
#     To provide **transparent**, **interpretable**, and **scenario‑driven** wheat price forecasts.

#     ### 📉 Why GRU?
#     GRUs handle:
#     - long‑term dependencies  
#     - seasonality  
#     - lagged effects  
#     - noisy economic signals  

#     ### 🧩 Limitations
#     - Forecasts are **probabilistic**, not guarantees  
#     - Extreme shocks may behave unpredictably  
#     - Model depends on data quality  
#     """)

# import streamlit as st
# import pandas as pd
# from datetime import datetime

# from model.load_model import load_all
# from model.predict import GRUPredictor
# from features.preprocess import preprocess_raw_data
# from features.feature_pipeline import build_feature_pipeline
# from utils.api_client import fetch_fred_latest

# # ------------------------------------------------------------
# # PAGE CONFIG
# # ------------------------------------------------------------
# st.set_page_config(page_title="Wheat Price Forecasting Dashboard", layout="wide")

# # ------------------------------------------------------------
# # SIDEBAR NAVIGATION
# # ------------------------------------------------------------
# st.sidebar.title("📌 Navigation")
# page = st.sidebar.radio("Go to", ["Home", "Forecast", "Scenario Simulation", "Data Explorer", "About"])

# # ------------------------------------------------------------
# # LOAD DATA + MODEL
# # ------------------------------------------------------------
# MASTER_PATH = "data/historical/master_monthly.parquet"

# df_master = pd.read_parquet(MASTER_PATH)
# df_master["month"] = pd.to_datetime(df_master["month"])
# df_master = df_master.set_index("month")

# # Seasonal imputation for climate variables
# df_master["rainfall"] = df_master["rainfall"].fillna(
#     df_master["rainfall"].groupby(df_master.index.month).transform("mean")
# )
# df_master["temperature"] = df_master["temperature"].fillna(
#     df_master["temperature"].groupby(df_master.index.month).transform("mean")
# )

# last_row = df_master.iloc[-1]

# model, feature_scaler, target_scaler, feature_columns = load_all()

# # ------------------------------------------------------------
# # LIVE + FALLBACK HELPERS
# # ------------------------------------------------------------
# def safe_fetch(fetch_func, fallback):
#     try:
#         val = fetch_func()
#         if val is None or pd.isna(val):
#             return fallback
#         return val
#     except:
#         return fallback

# def get_live_defaults(last_row):
#     oil_live = lambda: fetch_fred_latest("DCOILWTICO")
#     fx_live = lambda: fetch_fred_latest("DEXINUS")
#     fert_live = lambda: fetch_fred_latest("PCU3253132531")

#     return {
#         "oil_price": safe_fetch(oil_live, last_row["oil_price"]),
#         "usd_inr": safe_fetch(fx_live, last_row["usd_inr"]),
#         "fertiliser_index": safe_fetch(fert_live, last_row["fertiliser_index"]),

#         # fallback-only variables
#         "rainfall": last_row["rainfall"],
#         "temperature": last_row["temperature"],
#         "conflict_events": last_row["conflict_events"],
#         "gepu": last_row["gepu"],
#         "global_wheat_price": last_row["global_wheat_price"],
#         "fao_cereals": last_row["fao_cereals"],
#     }

# # ------------------------------------------------------------
# # DEBUG PANEL (LIVE vs FALLBACK)
# # ------------------------------------------------------------
# def debug_live_status(live_value, fallback_value, label):
#     st.sidebar.markdown(f"### 🔍 {label}")
#     st.sidebar.write(f"Live value: `{live_value}`")
#     st.sidebar.write(f"Fallback value: `{fallback_value}`")

#     if live_value == fallback_value:
#         st.sidebar.write("**Used:** Fallback (live unavailable)")
#     else:
#         st.sidebar.write("**Used:** Live value")

#     st.sidebar.write(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
#     st.sidebar.markdown("---")

# # ------------------------------------------------------------
# # SIDEBAR INPUTS
# # ------------------------------------------------------------
# def get_sidebar_inputs(last_row):
#     st.sidebar.subheader("Scenario Inputs")

#     base = get_live_defaults(last_row)

#     # Debug panel for each variable
#     debug_live_status(base["oil_price"], last_row["oil_price"], "Oil Price (WTI)")
#     debug_live_status(base["usd_inr"], last_row["usd_inr"], "USD/INR")
#     debug_live_status(base["fertiliser_index"], last_row["fertiliser_index"], "Fertiliser Index")

#     debug_live_status(base["rainfall"], last_row["rainfall"], "Rainfall (Fallback Only)")
#     debug_live_status(base["temperature"], last_row["temperature"], "Temperature (Fallback Only)")
#     debug_live_status(base["conflict_events"], last_row["conflict_events"], "Conflict Events (Fallback Only)")
#     debug_live_status(base["gepu"], last_row["gepu"], "GEPU (Fallback Only)")
#     debug_live_status(base["global_wheat_price"], last_row["global_wheat_price"], "Global Wheat Price (Fallback Only)")
#     debug_live_status(base["fao_cereals"], last_row["fao_cereals"], "FAO Cereals (Fallback Only)")

#     # Editable inputs
#     oil_price = st.sidebar.number_input("Oil Price (WTI)", value=float(base["oil_price"]))
#     usd_inr = st.sidebar.number_input("USD/INR", value=float(base["usd_inr"]))
#     rainfall = st.sidebar.number_input("Rainfall (mm)", value=float(base["rainfall"]))
#     conflict_events = st.sidebar.number_input("Conflict Events", value=float(base["conflict_events"]))
#     fertiliser_index = st.sidebar.number_input("Fertiliser Index", value=float(base["fertiliser_index"]))
#     temperature = st.sidebar.number_input("Temperature (°C)", value=float(base["temperature"]))

#     return {
#         "oil_price": oil_price,
#         "usd_inr": usd_inr,
#         "rainfall": rainfall,
#         "conflict_events": conflict_events,
#         "fertiliser_index": fertiliser_index,
#         "temperature": temperature,
#         "gepu": last_row["gepu"],
#         "global_wheat_price": last_row["global_wheat_price"],
#         "fao_cereals": last_row["fao_cereals"],
#     }

# # ------------------------------------------------------------
# # PAGE 1 — HOME
# # ------------------------------------------------------------
# if page == "Home":
#     st.title("🌾 Wheat Price Forecasting Dashboard")

#     st.markdown("""
#     Welcome to the **India Wheat Price Forecasting Dashboard**.
#     """)

#     st.subheader("Recent Wheat Price Trend")
#     st.line_chart(df_master["india_price"].tail(36))

# # ------------------------------------------------------------
# # PAGE 2 — FORECAST
# # ------------------------------------------------------------
# elif page == "Forecast":
#     st.title("📈 Wheat Price Forecast")

#     live_dict = get_sidebar_inputs(last_row)

#     df_raw = preprocess_raw_data(MASTER_PATH, live_dict)
#     df_features = build_feature_pipeline(df_raw)

#     predictor = GRUPredictor(model, feature_scaler, target_scaler, feature_columns)
#     result = predictor.predict(df_features)

#     col1, col2 = st.columns(2)

#     with col1:
#         st.metric("Next Month Price (₹/Quintal)", f"{result['predicted_price']:.2f}")

#     with col2:
#         st.metric("Predicted Return", f"{result['predicted_return']:.4f}")

#     st.subheader("📉 Historical Price Trend")
#     st.line_chart(df_raw["india_price"])

# # ------------------------------------------------------------
# # PAGE 3 — SCENARIO SIMULATION
# # ------------------------------------------------------------
# elif page == "Scenario Simulation":
#     st.title("⚡ Scenario Simulation")

#     live_dict = get_sidebar_inputs(last_row)

#     scenario = st.selectbox("Choose a scenario", [
#         "Oil Spike (+40%)",
#         "Rainfall Drop (-30%)",
#         "INR Depreciation (+10%)",
#         "Conflict Surge (+50%)",
#         "Temperature Heatwave (+3°C)"
#     ])

#     shock_dict = live_dict.copy()

#     if scenario == "Oil Spike (+40%)":
#         shock_dict["oil_price"] *= 1.4
#     elif scenario == "Rainfall Drop (-30%)":
#         shock_dict["rainfall"] *= 0.7
#     elif scenario == "INR Depreciation (+10%)":
#         shock_dict["usd_inr"] *= 1.1
#     elif scenario == "Conflict Surge (+50%)":
#         shock_dict["conflict_events"] *= 1.5
#     elif scenario == "Temperature Heatwave (+3°C)":
#         shock_dict["temperature"] += 3

#     df_shock = preprocess_raw_data(MASTER_PATH, shock_dict)
#     df_shock_features = build_feature_pipeline(df_shock)

#     predictor = GRUPredictor(model, feature_scaler, target_scaler, feature_columns)
#     shock_result = predictor.predict(df_shock_features)

#     st.metric("Scenario Forecasted Price", f"{shock_result['predicted_price']:.2f}")

# # ------------------------------------------------------------
# # PAGE 4 — DATA EXPLORER
# # ------------------------------------------------------------
# elif page == "Data Explorer":
#     st.title("🔎 Data Explorer")

#     selected_cols = st.multiselect(
#         "Choose variables to plot",
#         df_master.columns.tolist(),
#         default=["india_price", "oil_price", "usd_inr"]
#     )

#     st.line_chart(df_master[selected_cols].tail(120))

# # ------------------------------------------------------------
# # PAGE 5 — ABOUT
# # ------------------------------------------------------------
# elif page == "About":
#     st.title("ℹ️ About This Project")

#     st.markdown("""
#     This dashboard forecasts India wheat prices using a **GRU neural network**.
#     """)

import streamlit as st
import pandas as pd
from datetime import datetime

from model.load_model import load_all
from model.predict import GRUPredictor
from features.preprocess import preprocess_raw_data
from features.feature_pipeline import build_feature_pipeline
from utils.api_client import fetch_fred_latest

# ------------------------------------------------------------
# PAGE CONFIG
# ------------------------------------------------------------
st.set_page_config(page_title="Wheat Price Forecasting Dashboard", layout="wide")

# ------------------------------------------------------------
# SIDEBAR NAVIGATION
# ------------------------------------------------------------
st.sidebar.title("📌 Navigation")
page = st.sidebar.radio("Go to", [
    "Home",
    "Forecast",
    "Scenario Simulation",
    "Data Explorer",
    "Live Data Status",
    "About"
])

# ------------------------------------------------------------
# LOAD DATA + MODEL
# ------------------------------------------------------------
MASTER_PATH = "data/historical/master_monthly.parquet"

df_master = pd.read_parquet(MASTER_PATH)
df_master["month"] = pd.to_datetime(df_master["month"])
df_master = df_master.set_index("month")

# Seasonal imputation for climate variables
df_master["rainfall"] = df_master["rainfall"].fillna(
    df_master["rainfall"].groupby(df_master.index.month).transform("mean")
)
df_master["temperature"] = df_master["temperature"].fillna(
    df_master["temperature"].groupby(df_master.index.month).transform("mean")
)

last_row = df_master.iloc[-1]

model, feature_scaler, target_scaler, feature_columns = load_all()

# ------------------------------------------------------------
# LIVE + FALLBACK HELPERS
# ------------------------------------------------------------
def safe_fetch(fetch_func, fallback):
    try:
        val = fetch_func()
        if val is None or pd.isna(val):
            return fallback
        return val
    except:
        return fallback

def get_live_defaults(last_row):
    oil_live = lambda: fetch_fred_latest("DCOILWTICO")
    fx_live = lambda: fetch_fred_latest("DEXINUS")
    fert_live = lambda: fetch_fred_latest("PCU3253132531")

    return {
        "oil_price": safe_fetch(oil_live, last_row["oil_price"]),
        "usd_inr": safe_fetch(fx_live, last_row["usd_inr"]),
        "fertiliser_index": safe_fetch(fert_live, last_row["fertiliser_index"]),

        # fallback-only variables
        "rainfall": last_row["rainfall"],
        "temperature": last_row["temperature"],
        "conflict_events": last_row["conflict_events"],
        "gepu": last_row["gepu"],
        "global_wheat_price": last_row["global_wheat_price"],
        "fao_cereals": last_row["fao_cereals"],
    }

# ------------------------------------------------------------
# STATUS BADGE
# ------------------------------------------------------------
def status_badge(is_live):
    return "🟢 LIVE" if is_live else "🔴 FALLBACK"

# ------------------------------------------------------------
# BUILD TABLE FOR LIVE DATA STATUS PAGE
# ------------------------------------------------------------
def build_live_status_table(last_row):
    live_vals = get_live_defaults(last_row)
    rows = []
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    for key in live_vals.keys():
        live_val = live_vals[key]
        fallback_val = last_row[key]
        used_live = live_val != fallback_val

        rows.append({
            "Feature": key.replace("_", " ").title(),
            "Live Value": live_val,
            "Fallback Value": fallback_val,
            "Used": "Live" if used_live else "Fallback",
            "Status": status_badge(used_live),
            "Timestamp": timestamp
        })

    return pd.DataFrame(rows)

# ------------------------------------------------------------
# SIDEBAR INPUTS
# ------------------------------------------------------------
def get_sidebar_inputs(last_row):
    st.sidebar.subheader("Scenario Inputs")

    base = get_live_defaults(last_row)

    oil_price = st.sidebar.number_input("Oil Price (WTI)", value=float(base["oil_price"]))
    usd_inr = st.sidebar.number_input("USD/INR", value=float(base["usd_inr"]))
    rainfall = st.sidebar.number_input("Rainfall (mm)", value=float(base["rainfall"]))
    conflict_events = st.sidebar.number_input("Conflict Events", value=float(base["conflict_events"]))
    fertiliser_index = st.sidebar.number_input("Fertiliser Index", value=float(base["fertiliser_index"]))
    temperature = st.sidebar.number_input("Temperature (°C)", value=float(base["temperature"]))

    return {
        "oil_price": oil_price,
        "usd_inr": usd_inr,
        "rainfall": rainfall,
        "conflict_events": conflict_events,
        "fertiliser_index": fertiliser_index,
        "temperature": temperature,
        "gepu": last_row["gepu"],
        "global_wheat_price": last_row["global_wheat_price"],
        "fao_cereals": last_row["fao_cereals"],
    }

# ------------------------------------------------------------
# PAGE — HOME
# ------------------------------------------------------------
if page == "Home":
    st.title("🌾 Wheat Price Forecasting Dashboard")

    st.subheader("Recent Wheat Price Trend")
    st.line_chart(df_master["india_price"].tail(36))

# ------------------------------------------------------------
# PAGE — FORECAST
# ------------------------------------------------------------
elif page == "Forecast":
    st.title("📈 Wheat Price Forecast")

    live_dict = get_sidebar_inputs(last_row)

    df_raw = preprocess_raw_data(MASTER_PATH, live_dict)
    df_features = build_feature_pipeline(df_raw)

    predictor = GRUPredictor(model, feature_scaler, target_scaler, feature_columns)
    result = predictor.predict(df_features)

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Next Month Price (₹/Quintal)", f"{result['predicted_price']:.2f}")

    with col2:
        st.metric("Predicted Return", f"{result['predicted_return']:.4f}")

    st.subheader("📉 Historical Price Trend")
    st.line_chart(df_raw["india_price"])

# ------------------------------------------------------------
# PAGE — SCENARIO SIMULATION
# ------------------------------------------------------------
elif page == "Scenario Simulation":
    st.title("⚡ Scenario Simulation")

    live_dict = get_sidebar_inputs(last_row)

    scenario = st.selectbox("Choose a scenario", [
        "Oil Spike (+40%)",
        "Rainfall Drop (-30%)",
        "INR Depreciation (+10%)",
        "Conflict Surge (+50%)",
        "Temperature Heatwave (+3°C)"
    ])

    shock_dict = live_dict.copy()

    if scenario == "Oil Spike (+40%)":
        shock_dict["oil_price"] *= 1.4
    elif scenario == "Rainfall Drop (-30%)":
        shock_dict["rainfall"] *= 0.7
    elif scenario == "INR Depreciation (+10%)":
        shock_dict["usd_inr"] *= 1.1
    elif scenario == "Conflict Surge (+50%)":
        shock_dict["conflict_events"] *= 1.5
    elif scenario == "Temperature Heatwave (+3°C)":
        shock_dict["temperature"] += 3

    df_shock = preprocess_raw_data(MASTER_PATH, shock_dict)
    df_shock_features = build_feature_pipeline(df_shock)

    predictor = GRUPredictor(model, feature_scaler, target_scaler, feature_columns)
    shock_result = predictor.predict(df_shock_features)

    st.metric("Scenario Forecasted Price", f"{shock_result['predicted_price']:.2f}")

# ------------------------------------------------------------
# PAGE — DATA EXPLORER
# ------------------------------------------------------------
elif page == "Data Explorer":
    st.title("🔎 Data Explorer")

    selected_cols = st.multiselect(
        "Choose variables to plot",
        df_master.columns.tolist(),
        default=["india_price", "oil_price", "usd_inr"]
    )

    st.line_chart(df_master[selected_cols].tail(120))

# ------------------------------------------------------------
# PAGE — LIVE DATA STATUS
# ------------------------------------------------------------
elif page == "Live Data Status":
    st.title("📡 Live Data Status Monitor")

    st.markdown("""
    This page shows whether each feature is using **live API data** or **fallback dataset values**.
    """)

    status_df = build_live_status_table(last_row)
    st.dataframe(status_df, use_container_width=True)

    if st.button("🔄 Test Live API Now"):
        test_df = build_live_status_table(last_row)
        st.success("Live API test completed.")
        st.dataframe(test_df, use_container_width=True)

# ------------------------------------------------------------
# PAGE — ABOUT
# ------------------------------------------------------------
elif page == "About":
    st.title("ℹ️ About This Project")

    st.markdown("""
    This dashboard forecasts India wheat prices using a **GRU neural network**.
    """)