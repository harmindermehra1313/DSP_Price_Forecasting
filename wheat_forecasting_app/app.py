# app.py
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
# UI HELPERS
# ------------------------------------------------------------
def section_header(title, icon="📌"):
    st.markdown(
        f"""
        <div style="padding:10px 0; font-size:26px; font-weight:600;">
            {icon} {title}
        </div>
        """,
        unsafe_allow_html=True,
    )

def info_card(label, value, icon="📊", width="100%"):
    st.markdown(
        f"""
        <div style="
            padding:14px;
            border-radius:10px;
            background-color:#F7F9FB;
            border:1px solid #E6E9EE;
            width:{width};
            ">
            <div style="font-size:15px; color:#333; font-weight:600;">{icon} {label}</div>
            <div style="font-size:22px; color:#111; font-weight:700; margin-top:6px;">{value}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ------------------------------------------------------------
# SIDEBAR NAVIGATION
# ------------------------------------------------------------
st.sidebar.title("📌 Navigation")
page = st.sidebar.radio(
    "Go to",
    [
        "Home",
        "Forecast",
        "Scenario Simulation",
        "Data Explorer",
        "Live Data Status",
        "About",
    ],
)

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

# Load model and scalers
try:
    model, feature_scaler, target_scaler, feature_columns = load_all()
except Exception as e:
    st.error("Model failed to load. Check model files.")
    model, feature_scaler, target_scaler, feature_columns = None, None, None, None

# ------------------------------------------------------------
# LIVE + FALLBACK HELPERS
# ------------------------------------------------------------
def safe_fetch(fetch_func, fallback):
    try:
        val = fetch_func()
        if val is None or pd.isna(val):
            return fallback
        return val
    except Exception:
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

def status_badge(is_live):
    return "🟢 LIVE" if is_live else "🔴 FALLBACK"

def build_live_status_table(last_row):
    live_vals = get_live_defaults(last_row)
    rows = []
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    for key in live_vals.keys():
        live_val = live_vals[key]
        fallback_val = last_row[key]
        used_live = live_val != fallback_val

        rows.append(
            {
                "Feature": key.replace("_", " ").title(),
                "Live Value": live_val,
                "Fallback Value": fallback_val,
                "Used": "Live" if used_live else "Fallback",
                "Status": status_badge(used_live),
                "Timestamp": timestamp,
            }
        )

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
    conflict_events = st.sidebar.number_input(
        "Conflict Events", value=float(base["conflict_events"])
    )
    fertiliser_index = st.sidebar.number_input(
        "Fertiliser Index", value=float(base["fertiliser_index"])
    )
    temperature = st.sidebar.number_input(
        "Temperature (°C)", value=float(base["temperature"])
    )

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
    section_header("Wheat Price Forecasting Dashboard", "🌾")

    st.markdown("### Recent Wheat Price Trend (India)")
    st.line_chart(df_master["india_price"].tail(36))

    st.markdown("---")
    st.markdown(
        "This dashboard forecasts India wheat prices using a GRU model. Use the Forecast page to see the next-month prediction and the Scenario Simulation page to test shocks."
    )

# ------------------------------------------------------------
# PAGE — FORECAST
# ------------------------------------------------------------
elif page == "Forecast":
    section_header("Wheat Price Forecast", "📈")

    # Get inputs and run prediction
    live_dict = get_sidebar_inputs(last_row)

    df_raw = preprocess_raw_data(MASTER_PATH, live_dict)
    df_features = build_feature_pipeline(df_raw)

    predictor = GRUPredictor(model, feature_scaler, target_scaler, feature_columns)
    result = predictor.predict(df_features)

    # Top summary cards
    col1, col2, col3 = st.columns([1.2, 1.2, 1])
    with col1:
        info_card("Next Month Price (₹/Quintal)", f"₹ {result['predicted_price']:.2f}", "💰")
    with col2:
        info_card("Predicted Return", f"{result['predicted_return']:.4f}", "📈")
    with col3:
        info_card("Prediction Date", datetime.now().strftime("%Y-%m-%d"), "🗓️")

    st.markdown("---")

    # Interpretation and inputs used
    st.markdown("### Interpretation")
    st.markdown(
        f"""
        **Model prediction:** The GRU model forecasts **₹{result['predicted_price']:.2f} per quintal** for the next month.
        
        **Predicted return:** **{result['predicted_return']:.4f}** (positive indicates an expected increase).
        """
    )

    st.markdown("#### Inputs used for this prediction")
    inputs_table = pd.DataFrame(
        {
            "Feature": [
                "Oil Price (WTI)",
                "USD/INR",
                "Rainfall (mm)",
                "Temperature (°C)",
                "Conflict Events",
                "Fertiliser Index",
            ],
            "Value": [
                live_dict["oil_price"],
                live_dict["usd_inr"],
                live_dict["rainfall"],
                live_dict["temperature"],
                live_dict["conflict_events"],
                live_dict["fertiliser_index"],
            ],
        }
    )
    st.table(inputs_table)

    st.markdown("---")
    st.markdown("### Historical Price Context")
    st.line_chart(df_raw["india_price"].tail(60))

# ------------------------------------------------------------
# PAGE — SCENARIO SIMULATION
# ------------------------------------------------------------
elif page == "Scenario Simulation":
    section_header("Scenario Simulation", "⚡")

    live_dict = get_sidebar_inputs(last_row)

    scenario = st.selectbox(
        "Choose a scenario",
        [
            "Oil Spike (+40%)",
            "Rainfall Drop (-30%)",
            "INR Depreciation (+10%)",
            "Conflict Surge (+50%)",
            "Temperature Heatwave (+3°C)",
        ],
    )

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

    # Show baseline vs scenario
    baseline_price = None
    try:
        # compute baseline using current live_dict (re-run predictor)
        df_base = preprocess_raw_data(MASTER_PATH, live_dict)
        df_base_features = build_feature_pipeline(df_base)
        base_result = predictor.predict(df_base_features)
        baseline_price = base_result["predicted_price"]
    except Exception:
        baseline_price = last_row["india_price"]

    col1, col2 = st.columns(2)
    with col1:
        info_card("Baseline Next Month Price", f"₹ {baseline_price:.2f}", "📌")
    with col2:
        info_card("Scenario Forecasted Price", f"₹ {shock_result['predicted_price']:.2f}", "⚠️")

    st.markdown("### Scenario Details")
    st.markdown(f"**Scenario:** {scenario}")
    st.markdown("#### Shocked input values")
    shock_table = pd.DataFrame(
        {
            "Feature": ["Oil Price", "USD/INR", "Rainfall", "Temperature", "Conflict Events", "Fertiliser Index"],
            "Baseline": [
                live_dict["oil_price"],
                live_dict["usd_inr"],
                live_dict["rainfall"],
                live_dict["temperature"],
                live_dict["conflict_events"],
                live_dict["fertiliser_index"],
            ],
            "Shocked": [
                shock_dict["oil_price"],
                shock_dict["usd_inr"],
                shock_dict["rainfall"],
                shock_dict["temperature"],
                shock_dict["conflict_events"],
                shock_dict["fertiliser_index"],
            ],
        }
    )
    st.table(shock_table)

    st.markdown("---")
    st.markdown("### Interpretation")
    change_pct = (shock_result["predicted_price"] - baseline_price) / baseline_price * 100
    st.markdown(
        f"The scenario changes the predicted price by **{change_pct:.2f}%** compared with the baseline. "
        f"This helps assess sensitivity to the selected shock."
    )

# ------------------------------------------------------------
# PAGE — DATA EXPLORER
# ------------------------------------------------------------
elif page == "Data Explorer":
    section_header("Data Explorer", "🔎")

    selected_cols = st.multiselect(
        "Choose variables to plot",
        df_master.columns.tolist(),
        default=["india_price", "oil_price", "usd_inr"],
    )

    st.line_chart(df_master[selected_cols].tail(120))

    st.markdown("---")
    st.markdown("### Data Snapshot (most recent row)")
    st.table(df_master.tail(1).T)

# ------------------------------------------------------------
# PAGE — LIVE DATA STATUS
# ------------------------------------------------------------
elif page == "Live Data Status":
    section_header("Live Data Status Monitor", "📡")

    st.markdown(
        "This page shows whether each feature is using **live API data** or **fallback dataset values**."
    )

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
    section_header("About This Project", "ℹ️")

    st.markdown(
        """
        **Project summary**
        - Forecasts India wheat prices using a GRU neural network.
        - Inputs include economic (oil price, USD/INR), climatic (rainfall, temperature), and geopolitical indicators (conflict events).
        - Supports scenario simulation to test shocks and sensitivity.

        **How to use**
        1. Use the sidebar to set or adjust input values.
        2. Visit Forecast to see the next-month prediction and interpretation.
        3. Use Scenario Simulation to test shocks and compare with baseline.

        **Notes**
        - Live data is fetched from FRED where available; fallback values come from the historical dataset.
        - Prediction date is shown on the Forecast page.
        """
    )