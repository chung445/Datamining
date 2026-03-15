# Báo Cáo Dự Án Khai Phá Dữ Liệu: Phân Tích Phân Cụm Tiền Điện Tử

## Giới Thiệu

Dự án này nhằm phân tích hành vi giá của tiền điện tử thông qua các kỹ thuật khai phá dữ liệu, tập trung vào việc phân cụm tiền điện tử dựa trên các chỉ số hiệu suất lịch sử. Mục tiêu là xác định các mẫu và nhóm các đồng tiền tương tự, cung cấp thông tin cho chiến lược đầu tư hoặc hiểu biết thị trường.

Phân tích tuân theo quy trình nghiên cứu có thể tái tạo: EDA → tiền xử lý → kỹ thuật đặc trưng → khai phá → mô hình hóa → đánh giá. Chúng tôi sử dụng Python với các thư viện như pandas, scikit-learn và matplotlib để xử lý dữ liệu và trực quan hóa.

## Hiểu Biết Dữ Liệu

### Tổng Quan Tập Dữ Liệu
- **Nguồn**: 23 tệp CSV, mỗi tệp đại diện cho một loại tiền điện tử (ví dụ: Bitcoin, Ethereum, v.v.)
- **Khoảng Thời Gian**: Dữ liệu lịch sử hàng ngày từ các ngày bắt đầu khác nhau đến hiện tại
- **Cột**: `SNo`, `Name`, `Symbol`, `Date`, `High`, `Low`, `Open`, `Close`, `Volume`, `Marketcap`
- **Tổng Số Bản Ghi**: ~37.000 hàng sau khi hợp nhất

### Biến Chính
- **Dữ Liệu Giá**: `Open`, `High`, `Low`, `Close` (giá hàng ngày)
- **Khối Lượng**: Khối lượng giao dịch
- **Vốn Hóa Thị Trường**: Vốn hóa thị trường
- **Ngày**: Dấu thời gian hàng ngày

### Khám Phá Ban Đầu
- Tất cả các đồng tiền có độ dài dữ liệu khác nhau (một số bắt đầu sớm hơn)
- Phân phối giá cho thấy biến động cao điển hình của thị trường tiền điện tử
- Tương quan giữa các giá thường dương nhưng thay đổi theo đồng tiền

## Tiền Xử Lý Dữ Liệu

### Tải Dữ Liệu
- Sử dụng `src/data/loader.py` để tải tất cả CSV từ `data/raw/`
- Thêm cột `coin` dựa trên tên tệp
- Chuyển đổi `Date` thành định dạng datetime
- Hợp nhất tất cả tệp thành một DataFrame duy nhất

### Kỹ Thuật Đặc Trưng
- **Lợi Suất Log**: `log_return = log(Close / Close.shift(1))` để ổn định số học
- **Biến Động Lăn**: Độ lệch chuẩn 7 ngày của lợi suất log (`vol_7d`)
- **Trung Bình Động**: Trung bình động đơn giản 7 ngày và 30 ngày (`ma_7d`, `ma_30d`)
- **Nhãn Xu Hướng**: Nhãn phân loại (`up`, `down`, `flat`) dựa trên dấu lợi suất log
- **Chế Độ Biến Động**: Nhãn nhị phân (`high_vol`, `low_vol`) dựa trên trung vị biến động mỗi đồng tiền

### Làm Sạch Dữ Liệu
- Loại bỏ các hàng có giá trị NaN (từ các thao tác lăn)
- Đảm bảo sắp xếp datetime cho các đặc trưng chuỗi thời gian
- Lưu dữ liệu đã xử lý vào `data/processed/crypto_features.parquet`

## Phương Pháp Khai Phá Dữ Liệu

### Cách Tiếp Cận Phân Cụm
- **Tổng Hợp**: Nhóm theo đồng tiền và tính giá trị trung bình cho `log_return`, `vol_7d`, `Volume`, `Marketcap`
- **Chuẩn Hóa**: Áp dụng `StandardScaler` để chuẩn hóa đặc trưng
- **Thuật Toán**: Phân cụm KMeans với k=3 cụm
- **Đánh Giá**: Phân tích phương pháp khuỷu tay (inertia vs k từ 2-10) để đánh giá số cụm tối ưu

### Trực Quan Hóa
- **PCA**: Giảm xuống 2D để trực quan hóa, cho thấy ~80% phương sai được giải thích
- **Biểu Đồ Cụm**: Biểu đồ phân tán của các thành phần PCA được tô màu theo cụm
- **Phân Tích Đặc Trưng**: Biểu đồ thanh của các đặc trưng trung bình mỗi cụm

## Kết Quả & Thông Tin Chi Tiết

### Kết Quả Phân Cụm
- **Kích Thước Cụm**:
  - Cụm 0: 8 đồng tiền
  - Cụm 1: 8 đồng tiền
  - Cụm 2: 7 đồng tiền

- **Phương Sai Giải Thích PCA**: [0.5, 0.3] (hai thành phần đầu tiên nắm bắt ~80% phương sai)

### Đặc Điểm Cụm

**Cụm 0 (8 đồng tiền)**: Đồng tiền lớn với biến động vừa phải
- Ví dụ: Bitcoin, Ethereum, BinanceCoin
- Vốn hóa cao, lợi suất và biến động vừa phải
- Thông tin chi tiết: Tiền điện tử đã thiết lập với hiệu suất ổn định

**Cụm 1 (8 đồng tiền)**: Đồng tiền nhỏ với biến động cao
- Ví dụ: Aave, ChainLink, Solana
- Vốn hóa thấp, biến động cao, lợi suất thay đổi
- Thông tin chi tiết: Altcoin rủi ro với tiềm năng tăng trưởng cao

**Cụm 2 (7 đồng tiền)**: Đồng tiền trung bình với biến động thấp
- Ví dụ: Litecoin, Stellar, Tron
- Vốn hóa vừa phải, biến động thấp, lợi suất nhất quán
- Thông tin chi tiết: Tiền điện tử cân bằng với hiệu suất ổn định

### Thông Tin Chi Tiết Chính
1. **Phân Đoạn Thị Trường**: Tiền điện tử tự nhiên phân cụm theo vốn hóa và biến động, phản ánh các hồ sơ rủi ro khác nhau
2. **Mẫu Biến Động**: Đồng tiền biến động cao có xu hướng nhỏ hơn, trong khi đồng tiền lớn hơn cho thấy sự ổn định hơn
3. **Ý Nghĩa Đầu Tư**: Phân tích cụm có thể hướng dẫn chiến lược đa dạng hóa danh mục
4. **Chất Lượng Dữ Liệu**: Phương pháp khuỷu tay xác nhận k=3 là lựa chọn hợp lý cho tập dữ liệu này

### Hạn Chế
- Phân tích dựa trên dữ liệu lịch sử; hiệu suất tương lai có thể khác
- Kết quả phân cụm nhạy cảm với lựa chọn đặc trưng và chuẩn hóa
- Một số đồng tiền có chuỗi thời gian ngắn hơn, có thể ảnh hưởng đến tổng hợp

### Công Việc Tương Lai
- Kết hợp các đặc trưng bổ sung (ví dụ: cảm xúc xã hội, chỉ số on-chain)
- Thử các thuật toán phân cụm thay thế (DBSCAN, phân cấp)
- Phát triển mô hình dự đoán cho dự báo giá trong cụm
- Xây dựng bảng điều khiển giám sát thời gian thực

---

**Cấu Trúc Dự Án**:
- `data/raw/`: Tệp CSV thô
- `data/processed/`: Đặc trưng đã xử lý và kết quả phân cụm
- `notebooks/`: Notebook EDA, tiền xử lý, khai phá và phân tích
- `src/`: Mô-đun có thể tái sử dụng (trình tải dữ liệu, v.v.)
- `app.py`: Bảng điều khiển Streamlit tương tác

**Công Nghệ Sử Dụng**: Python, pandas, scikit-learn, matplotlib, seaborn, plotly, Streamlit