# Trading-Tool Project

## Mô tả dự án

Tool checklist trading forex tích hợp AI cho phân tích confluence, dựa trên API MetaTrader 5 (MT5). Hỗ trợ phân tích đa khung thời gian (multi-timeframe analysis) cho các yếu tố: trend, AOI (Area of Interest), mô hình giá, và tích hợp AI để xác nhận setup và đưa ra khuyến nghị giao dịch.

- **Ngôn ngữ chính:** Python 3.10+
- **Kho dữ liệu:** MetaTrader5
- **Mục tiêu:** Tăng tính khách quan khi phân tích, đưa ra quyết định trade an toàn dựa trên confluence, có thể mở rộng AI hoặc dùng UI trên web.

## Features
- Fetch giá đa khung thời gian từ MT5: Weekly, Daily, 4H, 1H, 30m.
- Tính toán các chỉ báo kỹ thuật như EMA, zone AOI.
- Nhận diện mô hình (patterns): Break & Retest, Head & Shoulders...
- Tự động chấm điểm confluence cho từng symbol.
- Phân tích AI (tùy chọn, có thể mở rộng).
- Tích hợp watchlist động từ file YAML ngoài.
- Sẵn sàng để mở rộng giao diện web (Streamlit) trong các bước sau.

## Installation
1. Clone repo về máy:
   ```bash
   git clone https://github.com/quan0604/theperfect_trade_checklist
   cd tenrepo
   ```
2. Cài đặt môi trường:
   ```bash
   pip install -r requirements.txt
   ```
3. (Nên) Setup file `.env` cho thông tin đăng nhập MT5 hoặc chỉnh file python tương ứng.

## Usage
- **Test data fetching:**
   ```bash
   python src/data_engine.py EURUSD
   # Hoặc chạy và nhập symbol theo prompt
   ```
- **Thay đổi danh sách symbol:**
   - Chỉnh file `watchlist.yaml`, mỗi lần chạy lại sẽ tự động cập nhật danh sách.
- **(Nếu có UI)**
   ```bash
   streamlit run app.py
   ```

## Contributing
1. Fork repo trên GitHub.
2. Tạo nhánh mới: `git checkout -b feature/my-new-feature`
3. Commit & push code.
4. Mở Pull Request, điền mô tả chi tiết.
5. Chờ review merge.

## License
- MIT License (tùy chọn thay đổi, nếu bạn thích có thể dùng GPL)

## Screenshots / Demo
Nếu bạn đã có UI kiểu Streamlit rồi, nên thêm hình/chụp demo vào đây. Ví dụ:
```md
![Screenshot](screenshots/dashboard_sample.png)
```

---

**Mọi góp ý, bug report hoặc ý tưởng phát triển, hãy mở issue hoặc PR nhé!**
