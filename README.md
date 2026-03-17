# 📊 Crypto Market Dashboard - Phân Tích & Dự Báo Tiền Điện Tử

Dự án khai phá dữ liệu toàn diện về thị trường tiền điện tử, kết hợp phân tích phân cụm, dự báo giá và bảng điều khiển tương tác. Sử dụng dữ liệu lịch sử từ 23 đồng tiền điện tử để cung cấp insights về hành vi thị trường, phân loại rủi ro và dự đoán giá tương lai.

## ✨ Tính Năng Chính

### 🔍 Phân Tích Khám Phá Dữ Liệu (EDA)
- Phân tích phân phối lợi suất và biến động
- Ma trận tương quan giá giữa các đồng tiền
- Xu hướng giá và khối lượng theo thời gian

### 🛠️ Kỹ Thuật Đặc Trưng & Tiền Xử Lý
- **Lợi suất log hàng ngày**: `log_return = log(Close / Close.shift(1))`
- **Biến động lăn 7 ngày**: Độ lệch chuẩn rolling volatility
- **Trung bình động**: MA 7 ngày và 30 ngày
- **Nhãn xu hướng**: Phân loại up/down/flat trends
- **Chế độ biến động**: High/Low volatility regimes

### 🎯 Phân Cụm KMeans (k=3)
- **Thuật toán**: KMeans với StandardScaler normalization
- **Đánh giá**: Elbow method và silhouette analysis
- **Trực quan hóa**: PCA 2D plots và cluster profiles
- **Clusters**:
  - **Blue Chip**: Bitcoin, Ethereum, BinanceCoin (ổn định, vốn hóa cao)
  - **Stablecoins**: Tether, USD Coin (biến động thấp)
  - **Altcoins**: Cardano, Solana, ChainLink (tăng trưởng cao, rủi ro cao)

### 🔮 Dự Báo Giá Thời Gian (Time Series Forecasting)
- **Models**: ARIMA(5,1,0) và Facebook Prophet
- **Đánh giá**: MAE, RMSE, MAPE metrics
- **Coverage**: Dự báo 30 ngày cho tất cả 23 coins
- **So sánh**: Model comparison và accuracy analysis

### 📈 Bảng Điều Khiển Tương Tác (Streamlit Dashboard)

#### 🏠 Trang Tổng Quan Thị Trường
1. **Chỉ số chính**: Tổng coins, giá TB, return TB, volatility TB
2. **Top coins**: Gainers, losers, highest volume
3. **Biểu đồ thị trường**: Price & return trends
4. **Phân tích bổ sung**:
   - Volatility trend
   - Volume trend
   - Return trends theo top 5 coins
   - Volatility trends theo top 5 coins
5. **Watchlist**: Multi-select coins với metrics
6. **Quick search**: Tìm kiếm coin nhanh
7. **Trading summary**: Tổng volume, market cap
8. **Risk metrics**: Sharpe ratio, VaR 95%
9. **Correlation heatmap**: Ma trận tương quan giá

#### 🔍 Trang Phân Tích Chi Tiết
- **Coin selection**: Dropdown chọn coin
- **Price charts**: Lịch sử giá với Plotly
- **Forecast visualization**: ARIMA vs Prophet (30 ngày)
- **Statistics**: Thống kê lịch sử chi tiết
- **Cluster insights**: Thông tin cụm với chiến lược đầu tư

## 🏗️ Cấu Trúc Dự Án

```
DATA_MINING_PROJECT/
├── data/
│   ├── raw/                 # CSV files gốc (23 coins)
│   └── processed/           # Dữ liệu đã xử lý
│       ├── crypto_features_clean.csv    # Features (36,921 rows)
│       ├── coin_clusters.csv            # Cluster assignments
│       └── all_coins_forecast.csv       # Forecast data (690 records)
├── notebooks/               # Jupyter notebooks
│   ├── 01_eda.ipynb                    # Exploratory Data Analysis
│   ├── 02_preprocess_feature.ipynb     # Feature Engineering
│   ├── 03_mining_clustering.ipynb      # KMeans Clustering
│   ├── 04_results_analysis.ipynb       # Results & Insights
│   └── 05_forecasting.ipynb            # Time Series Forecasting
├── src/                     # Python modules
│   └── data/
│       ├── __init__.py
│       └── loader.py        # Data loading utilities
├── app.py                   # Streamlit dashboard
├── requirements.txt         # Python dependencies
├── README.md               # Documentation (this file)
└── REPORT.md               # Detailed project report
```

## 🚀 Cài Đặt & Chạy

### Yêu Cầu Hệ Thống
- Python 3.8+
- 4GB RAM (recommended)
- Modern web browser

### Các Bước Cài Đặt

1. **Clone repository**:
   ```bash
   git clone <repository-url>
   cd DATA_MINING_PROJECT
   ```

2. **Tạo virtual environment**:
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   # source venv/bin/activate  # macOS/Linux
   ```

3. **Cài đặt dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Chạy dashboard**:
   ```bash
   streamlit run app.py
   ```
   Truy cập: `http://localhost:8501`

### Chạy Notebooks (Tùy chọn)
```bash
jupyter notebook
```
Mở và chạy tuần tự các notebooks từ 01 đến 05.

## 📊 Kết Quả Chính

### Phân Cụm (KMeans k=3)
- **Blue Chip (7 coins)**: Bitcoin, Ethereum, BinanceCoin, Polkadot, Solana, ChainLink, Uniswap
  - Vốn hóa cao, return ổn định, volatility trung bình
  - Chiến lược: Hold long-term (HODL)

- **Stablecoins (2 coins)**: Bitcoin, Tether
  - Volatility thấp nhất, return gần 0
  - Chiến lược: Cash management

- **Altcoins (14 coins)**: Cardano, Dogecoin, EOS, Litecoin, etc.
  - Tiềm năng tăng trưởng cao, volatility cao
  - Chiến lược: Selective betting

### Dự Báo Giá
- **Coverage**: 100% (23/23 coins)
- **Models**: ARIMA vs Prophet comparison
- **Accuracy**: Prophet có MAE thấp hơn 8.6%
- **Example**: Bitcoin $34,235 → 30 ngày: +2.9% (ARIMA), +4.35% (Prophet)

### Dashboard Features
- **Interactive filters**: Theo cluster và date range
- **Real-time calculations**: Risk metrics, correlations
- **Responsive design**: Mobile-friendly layout
- **Vietnamese interface**: Labels và explanations

## 🛠️ Công Nghệ Sử Dụng

- **Data Processing**: Pandas, NumPy
- **Machine Learning**: Scikit-learn (KMeans, StandardScaler)
- **Time Series**: Statsmodels (ARIMA), Prophet
- **Visualization**: Plotly Express, Plotly Graph Objects
- **Dashboard**: Streamlit
- **Development**: Jupyter Notebook
- **Data Storage**: CSV format

## 📈 Metrics & Performance

- **Data Points**: 36,921 records across 23 cryptocurrencies
- **Time Range**: 2013-2021
- **Forecast Accuracy**: MAE ~8.6% difference between models
- **Dashboard Load Time**: <2 seconds (with caching)
- **Memory Usage**: ~500MB peak

## 🔄 Workflow

1. **Data Collection** → Raw CSV files
2. **EDA** → Understanding patterns
3. **Preprocessing** → Feature engineering
4. **Clustering** → Market segmentation
5. **Forecasting** → Price predictions
6. **Dashboard** → Interactive visualization

## 📝 License

MIT License - See LICENSE file for details.

## 👥 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 📞 Contact

For questions or feedback about this project, please open an issue or contact the maintainers.

Nếu bạn có câu hỏi hoặc góp ý, vui lòng mở issue trên GitHub hoặc liên hệ qua email.

---

**Lưu Ý**: Dự án này dành cho mục đích giáo dục và nghiên cứu. Không sử dụng cho tư vấn đầu tư tài chính.
