# Processed Dataset

Folder này chứa dữ liệu sản phẩm đã được đọc từ `data/`, làm sạch, chuẩn hóa và xuất ra để dùng cho các bước tiếp theo như phân tích, tìm kiếm, RAG hoặc chuẩn bị train chatbot sau này.

## Tóm tắt xử lý

- Tổng dòng dữ liệu gốc: `3037`
- Số sản phẩm sau làm sạch: `3014`
- Số dòng bị loại: `23`
- Số dòng thông số kỹ thuật dạng dài: `30265`

Các bước xử lý chính:

- Đọc toàn bộ file CSV trong folder `data/`
- Chuẩn hóa encoding UTF-8
- Làm sạch ký tự BOM, HTML entity, xuống dòng, tab và khoảng trắng thừa
- Chuẩn hóa tên cột về dạng chữ thường, nối bằng `_`
- Thêm cột `category` dựa trên tên file nguồn
- Chuẩn hóa giá bán sang số ở cột `price_vnd`
- Gắn trạng thái giá vào `price_status`
- Xóa dòng thiếu tên sản phẩm
- Xóa sản phẩm trùng theo `url`, `ten_san_pham`, `sku`
- Gom các thông số kỹ thuật thành `specs_text` và `specs_json`
- Tách thông số kỹ thuật sang bảng dạng dài `product_specs_long`

## Danh sách file

### `products_clean.csv`

File CSV chính sau xử lý. Mỗi dòng tương ứng với một sản phẩm đã làm sạch.

Nên dùng file này khi cần mở bằng Excel, pandas, hoặc kiểm tra dữ liệu dạng bảng.

Các cột:

- `url`: Link sản phẩm.
- `ten_san_pham`: Tên sản phẩm.
- `thuong_hieu`: Thương hiệu sản phẩm.
- `gia_ban`: Giá bán gốc từ dữ liệu crawl, ví dụ `Liên hệ`.
- `price_vnd`: Giá bán đã chuẩn hóa về số VND. Nếu giá không có hoặc là `Liên hệ` thì để trống.
- `price_status`: Trạng thái giá. `available` là có giá số, `contact_or_missing` là chưa có giá hoặc cần liên hệ.
- `sku`: Mã sản phẩm.
- `mo_ta_ngan`: Mô tả ngắn của sản phẩm.
- `category`: Danh mục đã chuẩn hóa, ví dụ `dien_thoai`, `laptop`, `phu_kien`.
- `source_file`: File CSV gốc chứa sản phẩm.
- `specs_text`: Toàn bộ thông số kỹ thuật được gom thành một chuỗi dễ đọc.
- `specs_json`: Toàn bộ thông số kỹ thuật ở dạng JSON object.

### `products_clean.jsonl`

Nội dung giống `products_clean.csv`, nhưng ở định dạng JSON Lines.

Mỗi dòng là một JSON object của một sản phẩm. File này phù hợp hơn cho pipeline xử lý dữ liệu, indexing, vector database, RAG hoặc các bước chuẩn bị dữ liệu cho model.

Ví dụ mục đích dùng:

- Nạp từng dòng vào hệ thống tìm kiếm.
- Tạo document cho chatbot RAG.
- Parse thông số từ `specs_json` dễ hơn so với CSV.

### `product_specs_long.csv`

File thông số kỹ thuật ở dạng dài. Mỗi dòng là một thông số của một sản phẩm.

Nên dùng file này khi cần lọc, thống kê hoặc so sánh thông số giữa nhiều sản phẩm.

Các cột:

- `url`: Link sản phẩm.
- `sku`: Mã sản phẩm.
- `ten_san_pham`: Tên sản phẩm.
- `category`: Danh mục sản phẩm.
- `spec_name`: Tên thông số, ví dụ `dung_lượng_ram`, `kích_thước_màn_hình`, `chipset`.
- `spec_value`: Giá trị của thông số.

Ví dụ mục đích dùng:

- Lọc tất cả sản phẩm có `spec_name = dung_lượng_ram`.
- So sánh màn hình, RAM, chipset, pin giữa các sản phẩm.
- Tạo bộ lọc sản phẩm theo thông số.

### `product_specs_long.jsonl`

Nội dung giống `product_specs_long.csv`, nhưng ở định dạng JSON Lines.

File này tiện cho xử lý bằng code, import vào database hoặc đưa vào pipeline indexing.

### `category_counts.csv`

File thống kê số lượng sản phẩm theo danh mục.

Các cột:

- `category`: Tên danh mục đã chuẩn hóa.
- `product_count`: Số sản phẩm trong danh mục đó.

Số lượng hiện tại:

- `dien_thoai`: 921
- `laptop`: 675
- `phu_kien`: 359
- `tai_nghe_bluetooth`: 301
- `man_hinh`: 291
- `may_tinh_bang`: 178
- `loa`: 151
- `pc`: 82
- `micro`: 56

### `processing_report.json`

File báo cáo quá trình xử lý.

Nội dung gồm:

- `input_files`: Danh sách file CSV đầu vào.
- `raw_rows`: Tổng số dòng ban đầu.
- `clean_rows`: Số dòng sau khi làm sạch.
- `removed_rows`: Số dòng bị loại.
- `spec_rows`: Số dòng thông số kỹ thuật sau khi tách dạng dài.
- `categories`: Thống kê sản phẩm theo danh mục.
- `output_files`: Danh sách file đầu ra trong folder `processed/`.

## Gợi ý sử dụng

Dùng `products_clean.csv` hoặc `products_clean.jsonl` làm bảng sản phẩm chính.

Dùng `product_specs_long.csv` hoặc `product_specs_long.jsonl` khi cần tìm kiếm, lọc, so sánh theo từng thông số kỹ thuật.

Dùng `processing_report.json` để kiểm tra nhanh dữ liệu đã xử lý ra sao và có bao nhiêu dòng được giữ lại.
