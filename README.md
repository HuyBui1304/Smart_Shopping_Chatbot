# Smart Shopping Chatbot Data

Project này dùng notebook để xem dữ liệu sản phẩm, làm sạch, chuẩn hóa và xuất kết quả vào `processed/`.

Hiện tại project chưa train model. Notebook `code/data_preprocessing.ipynb` là nơi chính để đọc dữ liệu, kiểm tra dữ liệu và tạo dataset sạch cho các bước tiếp theo như tìm kiếm sản phẩm, RAG hoặc chuẩn bị fine-tuning chatbot.

## Cấu trúc project

```text
.
├── data/                         # CSV gốc
├── code/
│   ├── data_preprocessing.ipynb   # Notebook chính để xem, làm sạch và export dữ liệu
│   ├── create_finetune_qa.ipynb # Tạo Q&A fine-tune theo tỷ lệ 80% template, 20% Groq API
│   └── train_qwen2_5_colab.ipynb # Notebook Colab để fine-tune Qwen2.5 bằng QLoRA
├── processed/                    # Dữ liệu sau xử lý
│   ├── products_clean.csv
│   ├── products_clean.jsonl
│   ├── product_specs_long.csv
│   ├── product_specs_long.jsonl
│   ├── category_counts.csv
│   └── processing_report.json
└── requirements.txt
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

## Xem và xử lý dữ liệu

Mở notebook:

```bash
python3 -m jupyter notebook code/data_preprocessing.ipynb
```

Chạy toàn bộ cell trong notebook để đọc CSV từ `data/`, làm sạch dữ liệu và xuất file vào `processed/`.

Nếu muốn chạy lại notebook từ terminal:

```bash
python3 -m jupyter nbconvert --to notebook --execute code/data_preprocessing.ipynb --inplace
```

Lệnh này sẽ execute `code/data_preprocessing.ipynb` và cập nhật lại các file trong `processed/`.

## Tạo Q&A Fine-tune 80/20

Mở notebook:

```bash
python3 -m jupyter notebook code/create_finetune_qa.ipynb
```

Notebook tạo cặp câu hỏi - câu trả lời từ `processed/products_clean.csv` theo tỷ lệ:

- 80% sinh bằng template, không gọi API.
- 20% sinh bằng Groq API để dữ liệu tự nhiên hơn.

Mặc định phần API chưa chạy. Nếu muốn bật 20% Groq API, set API key:

```bash
export GROQ_API_KEY="your_groq_api_key"
```

Sau đó trong notebook đổi:

```python
RUN_API = True
```

Notebook sẽ lưu dataset ra:

```text
processed/finetune_qa_80_20.jsonl
```

## File đầu ra

Các file chính:

- `processed/products_clean.csv`: bảng sản phẩm sạch dạng CSV, mỗi dòng là một sản phẩm và có `product_id`.
- `processed/products_clean.jsonl`: bảng sản phẩm sạch dạng JSON Lines.
- `processed/product_specs_long.csv`: bảng thông số kỹ thuật dạng dài, tham chiếu sản phẩm bằng `product_id`.
- `processed/product_specs_long.jsonl`: thông số kỹ thuật dạng dài ở JSON Lines.
- `processed/category_counts.csv`: thống kê số sản phẩm theo danh mục.
- `processed/processing_report.json`: báo cáo quá trình xử lý.
