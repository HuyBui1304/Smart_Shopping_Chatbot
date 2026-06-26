.PHONY: install preprocess test clean

install:
	python3 -m pip install -r requirements.txt

preprocess:
	PYTHONPATH=src python3 -m chatbot_data.preprocess --input data --output processed

test:
	PYTHONPATH=src pytest

clean:
	rm -f processed/products_clean.csv \
		processed/products_clean.jsonl \
		processed/product_specs_long.csv \
		processed/product_specs_long.jsonl \
		processed/category_counts.csv \
		processed/processing_report.json
