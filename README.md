# Chat Bot Product Data

Project này dùng để làm sạch và chuẩn hóa dữ liệu sản phẩm từ các file CSV trong `data/`, sau đó xuất dữ liệu đã xử lý vào `processed/`.

Hiện tại project chưa train model. Phần chính là data preprocessing để chuẩn bị dữ liệu sạch cho các bước sau như tìm kiếm sản phẩm, RAG hoặc fine-tuning chatbot.

## Cấu trúc project

```text
.
├── data/                         # CSV gốc
├── processed/                    # Dữ liệu sau xử lý
│   ├── README.md                 # Giải thích từng file output
│   ├── products_clean.csv
│   ├── products_clean.jsonl
│   ├── product_specs_long.csv
│   ├── product_specs_long.jsonl
│   ├── category_counts.csv
│   └── processing_report.json
├── notebooks/                    # Notebook phân tích/thử nghiệm
│   └── data_preprocessing.ipynb
├── src/chatbot_data/             # Source code chính
│   └── preprocess.py             # Script làm sạch và chuẩn hóa dữ liệu
├── tests/                        # Unit test cho preprocessing
├── Makefile                      # Lệnh chạy nhanh
├── requirements.txt              # Dependency cơ bản
└── pyproject.toml                # Cấu hình Python package
```

## Cài đặt

```bash
python3 -m pip install -r requirements.txt
```

Nếu dùng môi trường ảo:

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
```

## Chạy xử lý dữ liệu

```bash
make preprocess
```

Hoặc chạy trực tiếp:

```bash
PYTHONPATH=src python3 -m chatbot_data.preprocess --input data --output processed
```

Sau khi chạy xong, dữ liệu sạch nằm trong `processed/`.

## Kiểm tra

```bash
make test
```

Lệnh test cần cài dependency trong `requirements.txt` trước.

## File đầu ra

Xem chi tiết trong [processed/README.md](processed/README.md).

Các file chính:

- `processed/products_clean.csv`: bảng sản phẩm sạch dạng CSV.
- `processed/products_clean.jsonl`: bảng sản phẩm sạch dạng JSON Lines.
- `processed/product_specs_long.csv`: thông số kỹ thuật dạng dài.
- `processed/product_specs_long.jsonl`: thông số kỹ thuật dạng dài ở JSON Lines.
- `processed/category_counts.csv`: thống kê số sản phẩm theo danh mục.
- `processed/processing_report.json`: báo cáo quá trình xử lý.
