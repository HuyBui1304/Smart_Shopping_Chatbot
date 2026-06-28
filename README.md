# Smart Shopping Chatbot

This project prepares a product catalog dataset, generates chat fine-tuning examples, trains a Qwen2.5 LoRA adapter, and runs a local shopping chatbot with lightweight product retrieval.

The current chatbot workflow combines:

- Product data from `processed/catalog.csv`
- A fine-tuned Qwen2.5 LoRA adapter in `models/shopping_chatbot_lora_adapter`
- Local keyword retrieval to provide product context at inference time

## Project Structure

```text
.
├── data/                              # Raw product CSV files
├── notebooks/
│   ├── prepare_product_catalog.ipynb    # Clean and normalize raw product data
│   ├── generate_fine_tuning_data.ipynb  # Generate fine-tuning Q&A data
│   ├── model_training_colab.ipynb       # Train the chatbot adapter on Colab
│   └── local_chatbot_inference.ipynb    # Run the local chatbot with the trained adapter
├── processed/                         # Processed datasets and generated fine-tuning data
│   ├── catalog.csv
│   ├── catalog.jsonl
│   ├── catalog_specs.csv
│   ├── catalog_specs.jsonl
│   ├── catalog_summary.csv
│   ├── data_processing_report.json
│   └── fine_tuning_dataset.jsonl
├── models/
│   └── shopping_chatbot_lora_adapter/
└── requirements.txt
```

## Setup

```bash
python3 -m pip install -r requirements.txt
```

Using a virtual environment is recommended:

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
```

## Prepare Product Data

Open:

```bash
python3 -m jupyter notebook notebooks/prepare_product_catalog.ipynb
```

This notebook reads raw CSV files from `data/`, cleans and normalizes the product catalog, and exports processed files to `processed/`.

## Generate Fine-Tuning Data

Open:

```bash
python3 -m jupyter notebook notebooks/generate_fine_tuning_data.ipynb
```

The dataset generator creates Q&A examples from `processed/catalog.csv` using an 80/20 mix:

- 80% template-generated Q&A
- 20% Groq-generated Q&A for more natural phrasing

API generation is disabled by default. To enable the Groq-generated portion, set:

```bash
export GROQ_API_KEY="your_groq_api_key"
```

Then set this in the notebook:

```python
RUN_API = True
```

The output file is:

```text
processed/fine_tuning_dataset.jsonl
```

## Train Qwen2.5 LoRA Adapter

Use the Colab notebook:

```text
notebooks/model_training_colab.ipynb
```

Upload `processed/fine_tuning_dataset.jsonl` in Colab, run the notebook, then download the trained adapter into:

```text
models/shopping_chatbot_lora_adapter/
```

The adapter is not a full model. At inference time it must be loaded together with the base model:

```text
Qwen/Qwen2.5-3B-Instruct
```

## Run Local Chatbot

Open:

```bash
python3 -m jupyter notebook notebooks/local_chatbot_inference.ipynb
```

The notebook loads:

- Base model `Qwen/Qwen2.5-3B-Instruct`
- LoRA adapter from `models/shopping_chatbot_lora_adapter`
- Product data from `processed/catalog.csv`

The first run may download the base model from Hugging Face.

## Main Outputs

- `processed/catalog.csv`: cleaned product table, one row per product with `product_id`
- `processed/catalog.jsonl`: JSON Lines version of the cleaned product table
- `processed/catalog_specs.csv`: long-format product specifications keyed by `product_id`
- `processed/catalog_specs.jsonl`: JSON Lines version of the long-format specifications
- `processed/catalog_summary.csv`: product count per category
- `processed/data_processing_report.json`: preprocessing summary
- `processed/fine_tuning_dataset.jsonl`: chat fine-tuning dataset
