import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Crypto Market Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom styling
st.markdown(
    """
    <style>
    .metric-card {
        background: linear-gradient(135deg, #1f7a2d 0%, #0e1117 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .metric-value {
        font-size: 28px;
        font-weight: bold;
        margin: 10px 0;
    }
    .metric-label {
        font-size: 14px;
        opacity: 0.8;
    }
    .positive {
        color: #00ff41;
    }
    .negative {
        color: #ff4141;
    }
    @media (max-width: 768px) {
        .metric-card {
            padding: 15px;
            margin-bottom: 10px;
        }
        .metric-value {
            font-size: 24px;
        }
    }
    .stButton>button {
        background: linear-gradient(135deg, #1f7a2d, #0e1117);
        color: white;
        border: none;
        border-radius: 5px;
        padding: 10px 20px;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #0e1117, #1f7a2d);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Load data
@st.cache_data
def load_data():
    features_df = pd.read_csv("data/processed/crypto_features_clean.csv")
    clusters_df = pd.read_csv("data/processed/coin_clusters.csv")
    forecast_df = pd.read_csv("data/processed/all_coins_forecast.csv")
    return features_df, clusters_df, forecast_df

@st.cache_data
def calculate_market_stats(features_df, clusters_df):
    features_df['Date'] = pd.to_datetime(features_df['Date'])
    latest_data = features_df.groupby('coin').tail(1)
    latest_data = pd.merge(latest_data, clusters_df[['coin', 'cluster']], on='coin')
    
    # Market averages
    market_avg = features_df.groupby('Date').agg({
        'Close': 'mean',
        'log_return': 'mean',
        'vol_7d': 'mean'
    }).reset_index()
    
    return latest_data, market_avg

@st.cache_data
def calculate_risk_metrics(features_df):
    risk_df = features_df.groupby('coin').agg({
        'log_return': ['mean', 'std'],
        'vol_7d': 'mean'
    }).reset_index()
    risk_df.columns = ['coin', 'avg_return', 'std_return', 'avg_vol']
    risk_df['sharpe_ratio'] = risk_df['avg_return'] / risk_df['std_return']
    risk_df['var_95'] = risk_df['avg_return'] - 1.645 * risk_df['std_return']  # 95% VaR
    return risk_df

features_df, clusters_df, all_forecast_df = load_data()
features_df['Date'] = pd.to_datetime(features_df['Date'])

# Sidebar menu
st.sidebar.title("💼 Crypto Market Dashboard")
page = st.sidebar.radio("Chọn trang", ["📊 Tổng Quan Thị Trường", "🔍 Phân Tích Chi Tiết"])

# ==================== HOME PAGE ====================
if page == "📊 Tổng Quan Thị Trường":
    st.title("📊 Tổng Quan Thị Trường Crypto")
    
    # Loading data with spinner
    with st.spinner("Đang tải dữ liệu thị trường..."):
        latest_data, market_avg = calculate_market_stats(features_df, clusters_df)
        risk_df = calculate_risk_metrics(features_df)
    
    # Filters and Refresh
    col1, col2, col3 = st.columns([2, 2, 1])
    with col1:
        cluster_filter = st.multiselect(
            "Lọc theo Cluster:",
            options=sorted(latest_data['cluster'].unique()),
            default=sorted(latest_data['cluster'].unique()),
            format_func=lambda x: {0: "Blue Chip", 1: "Stablecoins", 2: "Altcoins"}.get(x, f"Cluster {x}")
        )
    with col2:
        date_range = st.date_input(
            "Khoảng thời gian:",
            value=(features_df['Date'].min().date(), features_df['Date'].max().date()),
            key="date_filter"
        )
    with col3:
        if st.button("🔄 Refresh Data"):
            st.cache_data.clear()
            st.rerun()
    
    # Apply filters
    filtered_data = latest_data[latest_data['cluster'].isin(cluster_filter)]
    filtered_features = features_df[
        (features_df['Date'] >= pd.to_datetime(date_range[0])) & 
        (features_df['Date'] <= pd.to_datetime(date_range[1]))
    ]
    
    # 1. MARKET OVERVIEW - Các chỉ số chính
    st.subheader("1️⃣ Chỉ Số Thị Trường Chính")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_coins = len(filtered_data['coin'].unique())
        st.metric("Tổng Coins", total_coins)
    
    with col2:
        avg_price = filtered_data['Close'].mean()
        st.metric("Giá Trung Bình", f"${avg_price:,.2f}")
    
    with col3:
        avg_return = filtered_data['log_return'].mean()
        st.metric("Return TB", f"{avg_return:.4f}")
    
    with col4:
        avg_vol = filtered_data['vol_7d'].mean()
        st.metric("Volatility TB", f"{avg_vol:.4f}")
    
    # 2. TOP STOCKS
    st.subheader("2️⃣ Top Coins Hôm Nay")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.write("**🟢 Top Tăng Mạnh (Return)**")
        top_gainers = filtered_data.nlargest(5, 'log_return')[['coin', 'log_return', 'Close']]
        top_gainers_display = top_gainers.copy()
        top_gainers_display['Return %'] = (top_gainers_display['log_return'] * 100).round(2)
        st.dataframe(
            top_gainers_display[['coin', 'Return %']].rename(columns={'coin': 'Coin'}),
            use_container_width=True, hide_index=True
        )
    
    with col2:
        st.write("**🔴 Top Giảm Mạnh (Return)**")
        top_losers = filtered_data.nsmallest(5, 'log_return')[['coin', 'log_return', 'Close']]
        top_losers_display = top_losers.copy()
        top_losers_display['Return %'] = (top_losers_display['log_return'] * 100).round(2)
        st.dataframe(
            top_losers_display[['coin', 'Return %']].rename(columns={'coin': 'Coin'}),
            use_container_width=True, hide_index=True
        )
    
    with col3:
        st.write("**📊 Top Khối Lượng Giao Dịch**")
        top_volume = filtered_data.nlargest(5, 'Volume')[['coin', 'Volume']]
        top_volume_display = top_volume.copy()
        top_volume_display['Volume'] = (top_volume_display['Volume'] / 1e9).round(2)
        st.dataframe(
            top_volume_display.rename(columns={'Volume': 'Volume (B)'}).rename(columns={'coin': 'Coin'}),
            use_container_width=True, hide_index=True
        )
    
    # 3. MARKET CHART - Biểu đồ giá trung bình theo ngày
    st.subheader("3️⃣ Biểu Đồ Thị Trường Tổng Thể")
    
    # Tính giá trung bình của tất cả coins theo ngày (filtered)
    filtered_market_avg = filtered_features.groupby('Date').agg({
        'Close': 'mean',
        'log_return': 'mean',
        'vol_7d': 'mean'
    }).reset_index()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Giá Trung Bình Thị Trường**")
        fig_line = px.line(
            filtered_market_avg,
            x='Date', y='Close',
            title='Giá TB Thị Trường (Crypto)',
            labels={'Close': 'Giá TB (USD)', 'Date': 'Ngày'}
        )
        fig_line.update_layout(
            plot_bgcolor="#0e1117",
            paper_bgcolor="#0e1117",
            font_color="#fafafa",
            height=400
        )
        fig_line.update_traces(mode='lines', line=dict(width=2), hovertemplate='Ngày: %{x}<br>Giá: $%{y:.2f}')
        st.plotly_chart(fig_line, use_container_width=True)
    
    with col2:
        st.write("**Return Trung Bình Thị Trường**")
        fig_return = px.line(
            filtered_market_avg,
            x='Date', y='log_return',
            title='Return Log TB Thị Trường',
            labels={'log_return': 'Log Return', 'Date': 'Ngày'}
        )
        fig_return.update_layout(
            plot_bgcolor="#0e1117",
            paper_bgcolor="#0e1117",
            font_color="#fafafa",
            height=400
        )
        fig_return.update_traces(mode='lines', line=dict(width=2), hovertemplate='Ngày: %{x}<br>Return: %{y:.4f}')
        st.plotly_chart(fig_return, use_container_width=True)
    
    # ADDITIONAL MARKET ANALYSIS CHARTS
    st.subheader("3.1 Biểu Đồ Phân Tích Thị Trường")
    
    # Volatility and Volume Trends
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Volatility Trend**")
        fig_vol = px.line(
            filtered_market_avg,
            x='Date', y='vol_7d',
            title='Xu Hướng Volatility Thị Trường',
            labels={'vol_7d': 'Volatility (7d)', 'Date': 'Ngày'}
        )
        fig_vol.update_layout(
            plot_bgcolor="#0e1117",
            paper_bgcolor="#0e1117",
            font_color="#fafafa",
            height=350
        )
        fig_vol.update_traces(mode='lines', line=dict(color='#ff6b6b', width=2))
        st.plotly_chart(fig_vol, use_container_width=True)
    
    with col2:
        # Volume trend (using filtered data)
        volume_trend = filtered_features.groupby('Date')['Volume'].sum().reset_index()
        st.write("**Volume Trend**")
        fig_volume = px.line(
            volume_trend,
            x='Date', y='Volume',
            title='Xu Hướng Khối Lượng Giao Dịch',
            labels={'Volume': 'Tổng Khối Lượng', 'Date': 'Ngày'}
        )
        fig_volume.update_layout(
            plot_bgcolor="#0e1117",
            paper_bgcolor="#0e1117",
            font_color="#fafafa",
            height=350
        )
        fig_volume.update_traces(mode='lines', line=dict(color='#1e90ff', width=2))
        st.plotly_chart(fig_volume, use_container_width=True)
    
    # Return Distribution and Risk-Return Scatter
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Return Trend Theo Coin**")
        # Show return trends for top 5 coins
        top_coins = filtered_data.nlargest(5, 'Close')['coin'].tolist()
        return_trend_data = filtered_features[filtered_features['coin'].isin(top_coins)]
        
        fig_return_trend = px.line(
            return_trend_data,
            x='Date', y='log_return',
            color='coin',
            title='Xu Hướng Return Top 5 Coins',
            labels={'log_return': 'Log Return', 'Date': 'Ngày', 'coin': 'Coin'}
        )
        fig_return_trend.update_layout(
            plot_bgcolor="#0e1117",
            paper_bgcolor="#0e1117",
            font_color="#fafafa",
            height=350
        )
        fig_return_trend.update_traces(mode='lines', line=dict(width=2))
        st.plotly_chart(fig_return_trend, use_container_width=True)
    
    with col2:
        st.write("**Volatility Theo Coin**")
        # Show volatility trends for top 5 coins
        vol_trend_data = filtered_features[filtered_features['coin'].isin(top_coins)]
        
        fig_vol_trend = px.line(
            vol_trend_data,
            x='Date', y='vol_7d',
            color='coin',
            title='Xu Hướng Volatility Top 5 Coins',
            labels={'vol_7d': 'Volatility (7d)', 'Date': 'Ngày', 'coin': 'Coin'}
        )
        fig_vol_trend.update_layout(
            plot_bgcolor="#0e1117",
            paper_bgcolor="#0e1117",
            font_color="#fafafa",
            height=350
        )
        fig_vol_trend.update_traces(mode='lines', line=dict(width=2))
        st.plotly_chart(fig_vol_trend, use_container_width=True)
    
    # 4. WATCHLIST - Danh sách theo dõi
    st.subheader("4️⃣ Danh Sách Theo Dõi")
    
    watchlist_coins = st.multiselect(
        "Chọn coins để theo dõi:",
        sorted(features_df['coin'].unique()),
        default=['Bitcoin', 'Ethereum', 'Cardano']
    )
    
    if watchlist_coins:
        watchlist_data = filtered_data[filtered_data['coin'].isin(watchlist_coins)][
            ['coin', 'Close', 'log_return', 'vol_7d', 'cluster']
        ].sort_values('Close', ascending=False)
        
        watchlist_display = watchlist_data.copy()
        watchlist_display['Return %'] = (watchlist_display['log_return'] * 100).round(3)
        watchlist_display['Close'] = watchlist_display['Close'].round(2)
        watchlist_display['Volatility'] = watchlist_display['vol_7d'].round(4)
        
        st.dataframe(
            watchlist_display[['coin', 'Close', 'Return %', 'Volatility', 'cluster']].rename(columns={
                'coin': 'Coin',
                'Close': 'Giá Hiện Tại',
                'Return %': 'Return (%)',
                'Volatility': 'Vol (7d)',
                'cluster': 'Cluster'
            }),
            use_container_width=True, hide_index=True
        )
    
    # 5. QUICK SEARCH - Thanh tìm kiếm
    st.subheader("6️⃣ Tìm Kiếm Nhanh")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        search_coin = st.selectbox(
            "Tìm kiếm coin:",
            sorted(features_df['coin'].unique()),
            key='search'
        )
    
    if search_coin:
        coin_info = latest_data[latest_data['coin'] == search_coin].iloc[0]
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Giá", f"${coin_info['Close']:,.2f}")
        with col2:
            st.metric("Return", f"{coin_info['log_return']:.4f}")
        with col3:
            st.metric("Volatility", f"{coin_info['vol_7d']:.4f}")
        with col4:
            st.metric("Cluster", f"#{int(coin_info['cluster'])}")
    
    # 6. MARKET NEWS (Simulated)
    st.subheader("5️⃣ Tin Tức Thị Trường Crypto")
    
    news_items = [
        {
            "title": "Bitcoin tăng 2.9% trong 30 ngày tới",
            "description": "Dự báo ARIMA cho thấy Bitcoin sẽ tăng từ $34,235 lên $35,228",
            "date": "2021-07-07"
        },
        {
            "title": "Ethereum và TOP 5 coins lên sàn",
            "description": "Các blue chip cryptocurrencies dẫn đầu thị trường với return trung bình +0.53%",
            "date": "2021-07-06"
        },
        {
            "title": "Stablecoins ổn định trong biến động thị trường",
            "description": "Tether và USD Coin duy trì giá ổn định với volatility chỉ 1.96% - 5.32%",
            "date": "2021-07-05"
        },
        {
            "title": "Altcoins có cơ hội tăng trưởng",
            "description": "14 altcoins xây dựng momentum, Prophet model dự báo tăng +4.35% trong 30 ngày",
            "date": "2021-07-04"
        }
    ]
    
    for news in news_items:
        st.info(f"**{news['title']}**\n\n{news['description']}\n\n*{news['date']}*")
    
    # 7. TRADING SUMMARY
    st.subheader("7️⃣ Tóm Tắt Giao Dịch Thị Trường")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        total_volume = filtered_data['Volume'].sum()
        st.metric(
            "Tổng Khối Lượng Giao Dịch",
            f"${total_volume/1e12:.2f}T" if total_volume > 1e12 else f"${total_volume/1e9:.2f}B"
        )
    
    with col2:
        total_marketcap = filtered_data['Marketcap'].sum()
        st.metric(
            "Tổng Vốn Hóa Thị Trường",
            f"${total_marketcap/1e12:.2f}T" if total_marketcap > 1e12 else f"${total_marketcap/1e9:.2f}B"
        )
    
    with col3:
        total_coins_tracked = len(filtered_data)
        st.metric("Tổng Coins Theo Dõi", total_coins_tracked)
    
    # MARKET INSIGHTS
    st.subheader("Nhận Xét Thị Trường")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Phân Bổ Theo Clusters:**")
        cluster_dist = clusters_df['cluster'].value_counts().sort_index()
        cluster_names = {0: "Blue Chip", 1: "Stablecoins", 2: "Altcoins"}
        
        fig_cluster = px.pie(
            values=cluster_dist.values,
            names=[cluster_names[i] for i in cluster_dist.index],
            title="Phân Bổ Coins Theo Nhóm"
        )
        fig_cluster.update_layout(
            plot_bgcolor="#0e1117",
            paper_bgcolor="#0e1117",
            font_color="#fafafa"
        )
        st.plotly_chart(fig_cluster, use_container_width=True)
    
    with col2:
        st.write("**Cluster Insights:**")
        for cluster_id in sorted(clusters_df['cluster'].unique()):
            cluster_coins = clusters_df[clusters_df['cluster'] == cluster_id]
            avg_return = filtered_data[filtered_data['coin'].isin(cluster_coins['coin'])]['log_return'].mean()
            avg_vol = filtered_data[filtered_data['coin'].isin(cluster_coins['coin'])]['vol_7d'].mean()
            
            st.write(f"**Cluster {cluster_id} - {cluster_names[cluster_id]}:**")
            st.write(f"  • Coins: {len(cluster_coins)}")
            st.write(f"  • Avg Return: {avg_return:.4f}")
            st.write(f"  • Avg Volatility: {avg_vol:.4f}")
            st.write("")
    
    # RISK METRICS SECTION
    st.subheader("Chỉ Số Rủi Ro & Hiệu Suất")
    
    # Merge risk metrics with filtered data
    risk_display = pd.merge(filtered_data[['coin', 'cluster']], risk_df, on='coin')
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Top Sharpe Ratio (Hiệu suất/Rủi ro cao nhất)**")
        top_sharpe = risk_display.nlargest(5, 'sharpe_ratio')[['coin', 'sharpe_ratio', 'avg_return', 'std_return']]
        top_sharpe_display = top_sharpe.copy()
        top_sharpe_display['Sharpe'] = top_sharpe_display['sharpe_ratio'].round(3)
        top_sharpe_display['Return'] = (top_sharpe_display['avg_return'] * 100).round(2)
        top_sharpe_display['Volatility'] = (top_sharpe_display['std_return'] * 100).round(2)
        st.dataframe(
            top_sharpe_display[['coin', 'Sharpe', 'Return', 'Volatility']].rename(columns={'coin': 'Coin'}),
            use_container_width=True, hide_index=True
        )
    
    with col2:
        st.write("**VaR 95% (Rủi ro cao nhất)**")
        top_var = risk_display.nsmallest(5, 'var_95')[['coin', 'var_95', 'avg_return', 'std_return']]
        top_var_display = top_var.copy()
        top_var_display['VaR 95%'] = (top_var_display['var_95'] * 100).round(2)
        top_var_display['Return'] = (top_var_display['avg_return'] * 100).round(2)
        top_var_display['Volatility'] = (top_var_display['std_return'] * 100).round(2)
        st.dataframe(
            top_var_display[['coin', 'VaR 95%', 'Return', 'Volatility']].rename(columns={'coin': 'Coin'}),
            use_container_width=True, hide_index=True
        )
    
    # CORRELATION HEATMAP
    st.subheader("Ma Trận Tương Quan Giá")
    
    # Calculate correlation matrix for selected coins
    selected_coins = filtered_data['coin'].unique()[:10]  # Limit to 10 coins for readability
    corr_data = filtered_features[filtered_features['coin'].isin(selected_coins)]
    corr_pivot = corr_data.pivot(index='Date', columns='coin', values='Close')
    correlation_matrix = corr_pivot.corr()
    
    fig_heatmap = px.imshow(
        correlation_matrix,
        text_auto='.2f',
        aspect="auto",
        color_continuous_scale='RdBu_r',
        title="Tương Quan Giá Giữa Các Coins"
    )
    fig_heatmap.update_layout(
        plot_bgcolor="#0e1117",
        paper_bgcolor="#0e1117",
        font_color="#fafafa",
        height=500
    )
    st.plotly_chart(fig_heatmap, use_container_width=True)

# ==================== ANALYSIS PAGE ====================
else:
    st.title("🔍 Phân Tích Chi Tiết Coin")
    
    # Select coin
    coin = st.sidebar.selectbox("Chọn coin", sorted(features_df["coin"].unique()))
    
    # Filter data
    coin_data = features_df[features_df["coin"] == coin].copy()
    
    # Compute stats
    mean_return = coin_data["log_return"].mean()
    mean_vol = coin_data["vol_7d"].mean()
    latest_price = coin_data["Close"].iloc[-1]
    
    # Get cluster
    cluster_info = clusters_df[clusters_df["coin"] == coin]
    cluster_label = int(cluster_info["cluster"].iloc[0]) if not cluster_info.empty else None
    
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Giá Hiện Tại", f"${latest_price:,.2f}")
    col2.metric("Return TB", f"{mean_return:.4f}")
    col3.metric("Volatility (7d)", f"{mean_vol:.4f}")
    col4.metric("Cluster", cluster_label if cluster_label is not None else "N/A")
    
    # Price chart
    st.subheader("📈 Lịch Sử Giá")
    price_chart = px.line(
        coin_data, x="Date", y="Close",
        title=f"Giá {coin} Theo Thời Gian",
        labels={"Close": "Giá (USD)", "Date": "Ngày"}
    )
    price_chart.update_layout(
        plot_bgcolor="#0e1117",
        paper_bgcolor="#0e1117",
        font_color="#fafafa"
    )
    st.plotly_chart(price_chart, use_container_width=True)
    
    # Forecast
    st.subheader("🔮 Dự Báo Giá (30 Ngày Tới)")
    
    coin_forecast = all_forecast_df[all_forecast_df['coin'] == coin]
    
    if not coin_forecast.empty:
        recent_data = coin_data.tail(60)
        
        forecast_chart = px.line()
        forecast_chart.add_scatter(
            x=recent_data['Date'], y=recent_data['Close'],
            mode='lines', name='Lịch Sử', line=dict(color='blue')
        )
        forecast_chart.add_scatter(
            x=coin_forecast['Date'], y=coin_forecast['ARIMA_Prediction'],
            mode='lines', name='Dự Báo ARIMA', line=dict(color='red', dash='dash')
        )
        forecast_chart.add_scatter(
            x=coin_forecast['Date'], y=coin_forecast['Prophet_Prediction'],
            mode='lines', name='Dự Báo Prophet', line=dict(color='green', dash='dash')
        )
        
        forecast_chart.update_layout(
            title=f"Dự Báo Giá {coin} (Stacked Historical + Forecast)",
            xaxis_title="Ngày",
            yaxis_title="Giá (USD)",
            plot_bgcolor="#0e1117",
            paper_bgcolor="#0e1117",
            font_color="#fafafa",
            hovermode='x unified',
            height=500
        )
        st.plotly_chart(forecast_chart, use_container_width=True)
        
        # Forecast metrics
        current = coin_forecast['Current_Price'].iloc[0]
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Giá Hiện Tại", f"${current:,.2f}")
        with col2:
            arima_30d = coin_forecast['ARIMA_Prediction'].iloc[-1]
            arima_change = (arima_30d - current) / current * 100
            st.metric("ARIMA 30 Ngày", f"${arima_30d:,.2f}", f"{arima_change:+.2f}%")
        with col3:
            prophet_30d = coin_forecast['Prophet_Prediction'].iloc[-1]
            prophet_change = (prophet_30d - current) / current * 100
            st.metric("Prophet 30 Ngày", f"${prophet_30d:,.2f}", f"{prophet_change:+.2f}%")
    
    # Statistics table
    st.subheader("📊 Thống Kê Lịch Sử")
    st.dataframe(
        coin_data[["Date", "Close", "log_return", "vol_7d"]].describe().T,
        use_container_width=True
    )
    
    # Cluster insights
    if cluster_label is not None:
        st.subheader(f"🎯 Thông Tin Cluster {cluster_label}")
        
        cluster_coins = clusters_df[clusters_df["cluster"] == cluster_label]["coin"].tolist()
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Số Coins Trong Cluster", len(cluster_coins))
            st.write("**Danh Sách Coins:**")
            st.write(", ".join(cluster_coins))
        
        with col2:
            cluster_names = {
                0: "📈 Blue Chip - Các đồng tiền hàng đầu được thiết lập",
                1: "🛡️ Stablecoins - Ổn định giá, dùng cho giao dịch",
                2: "🚀 Altcoins - Cơ hội tăng trưởng cao hơn"
            }
            
            st.write(f"**{cluster_names[cluster_label]}**")
            
            if cluster_label == 0:
                st.write("""
                - Lãnh đạo thị trường (Bitcoin, Ethereum, Solana, v.v.)
                - Rủi ro trung bình, tăng trưởng ổn định
                - Áp lực từ nhà đầu tư tổ chức
                - Chiến lược: Nắm giữ lâu dài (HODL)
                """)
            elif cluster_label == 1:
                st.write("""
                - Giá ổn định (neo vào USD)
                - Volatility thấp nhất, return gần 0
                - Dùng làm phương tiện giao dịch
                - Chiến lược: Quản lý tiền mặt kỹ thuật số
                """)
            else:
                st.write("""
                - Tiềm năng tăng trưởng cao hơn Blue Chips
                - Volatility cao hơn, rủi ro cao hơn
                - Điều khiển các yếu tố sáng kiến công nghệ
                - Chiến lược: Đặt cược có chọn lọc trên dự án
                """)
