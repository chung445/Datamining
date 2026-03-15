import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Crypto Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom styling
st.markdown(
    """
    <style>
    .css-1d391kg {background-color: #0e1117;}  /* Editor background */
    .stButton>button {background-color: #1f7a2d; color: white;}
    </style>
    """,
    unsafe_allow_html=True,
)

# Load data
features_df = pd.read_parquet("data/processed/crypto_features.parquet")
clusters_df = pd.read_csv("data/processed/coin_clusters.csv")

# Sidebar
st.sidebar.title("Crypto Dashboard")
st.sidebar.write(
    "Use this dashboard to explore crypto price trends and key metrics.\n\n"
    "Select a coin and view its performance, cluster assignment, and statistics."
)
st.sidebar.markdown("---")

# Select coin
coin = st.sidebar.selectbox("Select a coin", sorted(features_df["coin"].unique()))

# Filter data for selected coin
coin_data = features_df[features_df["coin"] == coin].copy()
coin_data["Date"] = pd.to_datetime(coin_data["Date"], errors="coerce")

# Compute stats directly from coin_data
mean_return = coin_data["log_return"].mean()
mean_vol = coin_data["vol_7d"].mean()
latest_price = coin_data["Close"].iloc[-1]

# Cluster info (may be missing if clustering wasn’t run yet)
cluster_info = clusters_df[clusters_df["coin"] == coin]
cluster_label = (
    int(cluster_info["cluster"].iloc[0]) if not cluster_info.empty else None
)

# Page header
st.title("Cryptocurrency Analysis Dashboard")
st.markdown(f"### {coin}")

# Metrics
col1, col2, col3, col4 = st.columns(4)
col1.metric("Latest Close", f"${latest_price:,.2f}")
col2.metric("Mean Log Return", f"{mean_return:.4f}")
col3.metric("Mean Volatility (7d)", f"{mean_vol:.4f}")
col4.metric("Cluster", cluster_label if cluster_label is not None else "N/A")

# Price chart
st.subheader("Price History")
price_chart = px.line(
    coin_data,
    x="Date",
    y="Close",
    title=f"{coin} Close Price over Time",
    labels={"Close": "Price", "Date": "Date"},
)
price_chart.update_layout(plot_bgcolor="#0e1117", paper_bgcolor="#0e1117", font_color="#fafafa")
st.plotly_chart(price_chart, use_container_width=True)

# Stats table
st.subheader("Historical Statistics")
st.dataframe(coin_data[["Date", "Close", "log_return", "vol_7d"]].describe().T)
