import pandas as pd
import numpy as np
import os

print("=" * 80)
print("KIỂM TRA TOÀN BỘ CHỨC NĂNG DỰ ÁN")
print("=" * 80)

# 1. Kiểm tra dữ liệu
print("\n[1] KIỂM TRA DỮ LIỆU")
print("-" * 80)

try:
    features_df = pd.read_csv('data/processed/crypto_features_clean.csv')
    print(f"✅ crypto_features_clean.csv: {features_df.shape[0]} rows, {features_df.shape[1]} columns")
    print(f"   - Coins: {features_df['coin'].nunique()} coins")
    print(f"   - Date range: {features_df['Date'].min()} to {features_df['Date'].max()}")
except Exception as e:
    print(f"❌ Error loading features: {e}")

try:
    clusters_df = pd.read_csv('data/processed/coin_clusters.csv')
    print(f"\n✅ coin_clusters.csv: {clusters_df.shape[0]} rows")
    print(f"   - Clusters: {sorted(clusters_df['cluster'].unique())}")
    for c in sorted(clusters_df['cluster'].unique()):
        count = len(clusters_df[clusters_df['cluster'] == c])
        print(f"     Cluster {c}: {count} coins")
except Exception as e:
    print(f"❌ Error loading clusters: {e}")

try:
    forecast_df = pd.read_csv('data/processed/bitcoin_forecast.csv')
    print(f"\n✅ bitcoin_forecast.csv: {forecast_df.shape[0]} rows")
except Exception as e:
    print(f"❌ Error loading forecast: {e}")

try:
    comparison_df = pd.read_csv('data/processed/model_comparison.csv')
    print(f"\n✅ model_comparison.csv: {comparison_df.shape[0]} coins compared")
except Exception as e:
    print(f"❌ Error loading model comparison: {e}")

# 2. Kiểm tra matching giữa features và clusters
print("\n\n[2] KIỂM TRA MATCHING DỮ LIỆU")
print("-" * 80)

features_coins = set(features_df['coin'].unique())
clusters_coins = set(clusters_df['coin'].unique())

print(f"Coins in features: {len(features_coins)}")
print(f"Coins in clusters: {len(clusters_coins)}")
print(f"Coins match: {features_coins == clusters_coins}")

if features_coins == clusters_coins:
    print("✅ Tất cả coins được match đúng!")
else:
    missing = features_coins - clusters_coins
    extra = clusters_coins - features_coins
    if missing:
        print(f"❌ Missing from clusters: {missing}")
    if extra:
        print(f"❌ Extra in clusters: {extra}")

# 3. Kiểm tra Bitcoin và Ethereum
print("\n\n[3] KIỂM TRA DỮ LIỆU THIẾT YẾU")
print("-" * 80)

btc_data = features_df[features_df['coin'] == 'Bitcoin']
print(f"Bitcoin data points: {len(btc_data)}")

btc_cluster = clusters_df[clusters_df['coin'] == 'Bitcoin']
if not btc_cluster.empty:
    print(f"Bitcoin cluster: {int(btc_cluster['cluster'].iloc[0])} ✅")

eth_cluster = clusters_df[clusters_df['coin'] == 'Ethereum']
if not eth_cluster.empty:
    print(f"Ethereum cluster: {int(eth_cluster['cluster'].iloc[0])} ✅")

# 4. Test forecasting
print("\n\n[4] KIỂM TRA DỰ BÁO")
print("-" * 80)

forecast_data = pd.read_csv('data/processed/bitcoin_forecast.csv')
print(f"Forecast dates: {forecast_data['Date'].min()} to {forecast_data['Date'].max()}")
print(f"ARIMA predictions: {forecast_data['ARIMA_Prediction'].notna().sum()}/{len(forecast_data)}")
print(f"Prophet predictions: {forecast_data['Prophet_Prediction'].notna().sum()}/{len(forecast_data)}")

if (forecast_data['ARIMA_Prediction'].notna().sum() == len(forecast_data) and 
    forecast_data['Prophet_Prediction'].notna().sum() == len(forecast_data)):
    print("✅ Cả hai model đều có dự báo đầy đủ")

# 5. Test model comparison
print("\n\n[5] KIỂM TRA SO SÁNH MÔ HÌNH")
print("-" * 80)

comparison = pd.read_csv('data/processed/model_comparison.csv')
print("So sánh MAE:")
for _, row in comparison.iterrows():
    print(f"  {row['Coin']:15} | ARIMA: {row['ARIMA_MAE']:10.2f} | Prophet: {row['Prophet_MAE']:10.2f}")

avg_arima_mae = comparison['ARIMA_MAE'].mean()
avg_prophet_mae = comparison['Prophet_MAE'].mean()
print(f"\nAverage MAE: ARIMA={avg_arima_mae:.2f}, Prophet={avg_prophet_mae:.2f}")
if avg_prophet_mae < avg_arima_mae:
    print(f"✅ Prophet tốt hơn ARIMA")

# 6. Cluster insights
print("\n\n[6] KIỂM TRA CLUSTER INSIGHTS")
print("-" * 80)

for cluster_id in sorted(clusters_df['cluster'].unique()):
    cluster_coins = clusters_df[clusters_df['cluster'] == cluster_id]
    print(f"\nCluster {cluster_id}: {len(cluster_coins)} coins")
    print(f"  Coins: {', '.join(cluster_coins['coin'].tolist())}")
    print(f"  Avg Return: {cluster_coins['log_return'].mean():.6f}")
    print(f"  Avg Volatility: {cluster_coins['vol_7d'].mean():.6f}")

# 7. Summary
print("\n\n" + "=" * 80)
print("KẾT LUẬN KIỂM TRA")
print("=" * 80)

checks = {
    "Dữ liệu crypto features": len(features_df) > 0,
    "Dữ liệu clusters": len(clusters_df) > 0,
    "Dữ liệu dự báo": len(forecast_df) > 0,
    "Dữ liệu so sánh model": len(comparison_df) > 0,
    "Match coins": features_coins == clusters_coins,
    "Dữ liệu Bitcoin": len(btc_data) > 0,
    "Cluster Bitcoin": not btc_cluster.empty,
    "Dự báo ARIMA": (forecast_df['ARIMA_Prediction'].notna().sum() == len(forecast_df)),
    "Dự báo Prophet": (forecast_df['Prophet_Prediction'].notna().sum() == len(forecast_df)),
}

all_good = True
for check_name, result in checks.items():
    status = "✅" if result else "❌"
    print(f"{status} {check_name}")
    if not result:
        all_good = False

print("\n" + "=" * 80)
if all_good:
    print("✅ TẤT CẢ CHỨC NĂNG HOẠT ĐỘNG BÌNH THƯỜNG - SẴN SÀNG DEMO!")
else:
    print("⚠️ CÓ MỘT SỐ VẤN ĐỀ CẦN SỬA!")
print("=" * 80)
