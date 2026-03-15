# Dự Án Khai Phá Dữ Liệu: Phân Tích Phân Cụm Tiền Điện Tử

Dự án này triển khai một quy trình khai phá dữ liệu có thể tái tạo để phân tích hành vi giá của tiền điện tử thông qua phân cụm không giám sát. Chúng tôi sử dụng dữ liệu lịch sử hàng ngày từ 23 loại tiền điện tử để xác định các mẫu và nhóm các đồng tiền tương tự dựa trên lợi suất, biến động và vốn hóa thị trường.

## Mục Tiêu

- Thực hiện phân tích khám phá dữ liệu (EDA) trên dữ liệu tiền điện tử.
- Xây dựng các đặc trưng kỹ thuật (lợi suất log, biến động lăn, trung bình động).
- Áp dụng phân cụm KMeans để nhóm các đồng tiền.
- Phân tích kết quả phân cụm và rút ra thông tin chi tiết.
- Phát triển bảng điều khiển tương tác bằng Streamlit để trực quan hóa.

## Cấu Trúc Dự Án

```
DATA_MINING_PROJECT/
├── data/
│   ├── raw/                 # Tệp CSV thô của tiền điện tử
│   └── processed/           # Dữ liệu đã xử lý và kết quả phân cụm
├── notebooks/               # Jupyter notebooks cho từng giai đoạn
│   ├── 01_eda.ipynb         # Khám phá dữ liệu ban đầu
│   ├── 02_preprocess_feature.ipynb  # Kỹ thuật đặc trưng
│   ├── 03_mining_clustering.ipynb   # Phân cụm KMeans
│   └── 04_results_analysis.ipynb    # Phân tích kết quả
├── src/                     # Mô-đun Python có thể tái sử dụng
│   └── data/
│       └── loader.py        # Trình tải dữ liệu
├── app.py                   # Bảng điều khiển Streamlit
├── REPORT.md                # Báo cáo dự án chi tiết (tiếng Việt)
├── README.md                # Tài liệu này
└── requirements.txt         # Danh sách phụ thuộc Python
```

## Cài Đặt

### Yêu Cầu Hệ Thống
- Python 3.8+
- Jupyter Notebook hoặc JupyterLab
- Git (để sao chép kho lưu trữ)

### Các Bước Cài Đặt

1. **Sao Chép Kho Lưu Trữ**:
   ```bash
   git clone <repository-url>
   cd DATA_MINING_PROJECT
   ```

2. **Tạo Môi Trường Ảo** (Khuyến nghị):
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Trên Windows
   ```

3. **Cài Đặt Các Phụ Thuộc**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Chuẩn Bị Dữ Liệu**:
   - Đảm bảo các tệp CSV thô nằm trong `data/raw/`
   - Chạy notebook `01_eda.ipynb` để xác minh tải dữ liệu

## Sử Dụng

### Chạy Các Notebook
1. Khởi động Jupyter:
   ```bash
   jupyter notebook
   ```

2. Mở và chạy tuần tự các notebook:
   - `01_eda.ipynb`: Khám phá dữ liệu và trực quan hóa ban đầu
   - `02_preprocess_feature.ipynb`: Tạo đặc trưng và lưu vào Parquet
   - `03_mining_clustering.ipynb`: Thực hiện phân cụm và đánh giá phương pháp khuỷu tay
   - `04_results_analysis.ipynb`: Phân tích cụm và tạo bảng tóm tắt

### Chạy Bảng Điều Khiển
```bash
streamlit run app.py
```
Truy cập `http://localhost:8501` để xem bảng điều khiển tương tác với:
- Bộ chọn đồng tiền
- Biểu đồ giá lịch sử
- Thống kê cụm
- Bảng dữ liệu

## Công Nghệ Sử Dụng

- **Python**: Ngôn ngữ chính
- **Pandas & NumPy**: Xử lý dữ liệu
- **Scikit-learn**: Phân cụm, chuẩn hóa, PCA
- **Matplotlib & Seaborn**: Trực quan hóa tĩnh
- **Plotly**: Biểu đồ tương tác
- **Streamlit**: Bảng điều khiển web
- **Jupyter Notebook**: Phát triển và trình bày
- **Parquet**: Lưu trữ dữ liệu hiệu quả

## Kết Quả Chính

- **Phân Cụm**: 3 cụm dựa trên lợi suất, biến động và vốn hóa
  - Cụm 0: Đồng tiền lớn với biến động vừa phải (Bitcoin, Ethereum)
  - Cụm 1: Đồng tiền nhỏ với biến động cao (Aave, ChainLink)
  - Cụm 2: Đồng tiền trung bình với biến động thấp (Litecoin, Stellar)

- **Thông Tin Chi Tiết**: Phân đoạn thị trường tự nhiên, hướng dẫn đa dạng hóa danh mục

## Đóng Góp

1. Fork kho lưu trữ
2. Tạo nhánh tính năng (`git checkout -b feature/AmazingFeature`)
3. Cam kết thay đổi (`git commit -m 'Add some AmazingFeature'`)
4. Push lên nhánh (`git push origin feature/AmazingFeature`)
5. Mở Pull Request

## Giấy Phép

Dự án này được phân phối dưới giấy phép MIT. Xem tệp `LICENSE` để biết thêm chi tiết.

## Liên Hệ

Nếu bạn có câu hỏi hoặc góp ý, vui lòng mở issue trên GitHub hoặc liên hệ qua email.

---

**Lưu Ý**: Dự án này dành cho mục đích giáo dục và nghiên cứu. Không sử dụng cho tư vấn đầu tư tài chính.
