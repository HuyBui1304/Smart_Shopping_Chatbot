from __future__ import annotations

import argparse
import html
import json
import re
import unicodedata
from pathlib import Path
from typing import Iterable, Optional

import pandas as pd


CATEGORY_MAPPING = {
    "thong_tin_links_san_pham": "dien_thoai",
    "thong_tin_products_links": "dien_thoai",
    "thong_tin_links_laptop": "laptop",
    "thong_tin_links_pc": "pc",
    "thong_tin_links_screen": "man_hinh",
    "thong_tin_links_speaker": "loa",
    "thong_tin_links_tablet": "may_tinh_bang",
    "thong_tin_links_bluetooth": "tai_nghe_bluetooth",
    "thong_tin_links_micro": "micro",
    "thong_tin_links_accessory": "phu_kien",
}

CORE_COLUMNS = {
    "url",
    "ten_san_pham",
    "thuong_hieu",
    "gia_ban",
    "price_vnd",
    "price_status",
    "sku",
    "mo_ta_ngan",
    "category",
    "source_file",
}

OUTPUT_FILES = [
    "products_clean.csv",
    "products_clean.jsonl",
    "product_specs_long.csv",
    "product_specs_long.jsonl",
    "category_counts.csv",
    "processing_report.json",
]


def clean_text(value: object) -> str:
    if pd.isna(value):
        return ""

    text = str(value).replace("\ufeff", "")
    text = html.unescape(text)
    text = unicodedata.normalize("NFC", text)
    text = re.sub(r"\\[rnt]", " ", text)
    text = re.sub(r"[\r\n\t]+", " ", text)
    text = re.sub(r"\s{2,}", " ", text)
    return text.strip()


def normalize_column_name(name: str) -> str:
    text = clean_text(name).lower()
    text = re.sub(r"\s+", "_", text)
    text = re.sub(r"_+", "_", text)
    return text.strip("_")


def make_unique_columns(columns: Iterable[str]) -> list[str]:
    seen: dict[str, int] = {}
    unique = []

    for col in columns:
        count = seen.get(col, 0) + 1
        seen[col] = count
        unique.append(col if count == 1 else f"{col}_{count}")

    return unique


def normalize_price(value: str) -> Optional[int]:
    text = clean_text(value)
    if not text:
        return None

    lowered = text.lower()
    if lowered in {"liên hệ", "lien he", "đang cập nhật", "dang cap nhat"}:
        return None

    digits = re.sub(r"[^0-9]", "", text)
    return int(digits) if digits else None


def category_from_filename(path: Path) -> str:
    return CATEGORY_MAPPING.get(path.stem.lower(), path.stem.lower())


def read_raw_data(input_dir: Path) -> pd.DataFrame:
    csv_files = sorted(input_dir.glob("*.csv"))
    if not csv_files:
        raise FileNotFoundError(f"No CSV files found in {input_dir}")

    frames = []
    for file in csv_files:
        df = pd.read_csv(file, encoding="utf-8-sig", dtype=str, keep_default_na=False)
        df["source_file"] = file.name
        df["category"] = category_from_filename(file)
        frames.append(df)

    return pd.concat(frames, ignore_index=True, sort=False).fillna("")


def clean_raw_data(raw: pd.DataFrame) -> tuple[pd.DataFrame, int]:
    clean = raw.copy()
    clean.columns = make_unique_columns(normalize_column_name(col) for col in clean.columns)

    for col in clean.columns:
        clean[col] = clean[col].map(clean_text)

    required_cols = [
        "url",
        "ten_san_pham",
        "thuong_hieu",
        "gia_ban",
        "sku",
        "mo_ta_ngan",
        "category",
        "source_file",
    ]
    for col in required_cols:
        if col not in clean.columns:
            clean[col] = ""

    before_rows = len(clean)
    clean = clean[clean["ten_san_pham"].ne("")].copy()
    clean["price_vnd"] = clean["gia_ban"].map(normalize_price)
    clean["price_status"] = clean["price_vnd"].apply(
        lambda value: "available" if pd.notna(value) else "contact_or_missing"
    )
    clean = clean.drop_duplicates(
        subset=["url", "ten_san_pham", "sku"],
        keep="first",
    ).reset_index(drop=True)

    return clean, before_rows


def make_product_outputs(clean: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    spec_columns = [col for col in clean.columns if col not in CORE_COLUMNS]

    def row_specs(row: pd.Series) -> dict[str, str]:
        specs = {}
        for col in spec_columns:
            value = row.get(col, "")
            if value:
                specs[col] = value
        return specs

    products = clean.copy()
    products["specs_json"] = products.apply(
        lambda row: json.dumps(row_specs(row), ensure_ascii=False),
        axis=1,
    )
    products["specs_text"] = products["specs_json"].map(
        lambda value: "; ".join(f"{key}: {val}" for key, val in json.loads(value).items())
    )

    products_clean = products[
        [
            "url",
            "ten_san_pham",
            "thuong_hieu",
            "gia_ban",
            "price_vnd",
            "price_status",
            "sku",
            "mo_ta_ngan",
            "category",
            "source_file",
            "specs_text",
            "specs_json",
        ]
    ].copy()

    spec_rows = []
    for _, row in products_clean.iterrows():
        specs = json.loads(row["specs_json"])
        for spec_name, spec_value in specs.items():
            spec_rows.append(
                {
                    "url": row["url"],
                    "sku": row["sku"],
                    "ten_san_pham": row["ten_san_pham"],
                    "category": row["category"],
                    "spec_name": spec_name,
                    "spec_value": spec_value,
                }
            )

    specs_long = pd.DataFrame(
        spec_rows,
        columns=["url", "sku", "ten_san_pham", "category", "spec_name", "spec_value"],
    )
    return products_clean, specs_long


def write_outputs(
    products_clean: pd.DataFrame,
    specs_long: pd.DataFrame,
    input_files: list[str],
    before_rows: int,
    output_dir: Path,
) -> dict:
    output_dir.mkdir(parents=True, exist_ok=True)

    products_clean.to_csv(output_dir / "products_clean.csv", index=False, encoding="utf-8-sig")
    products_clean.to_json(
        output_dir / "products_clean.jsonl",
        orient="records",
        lines=True,
        force_ascii=False,
    )

    specs_long.to_csv(output_dir / "product_specs_long.csv", index=False, encoding="utf-8-sig")
    specs_long.to_json(
        output_dir / "product_specs_long.jsonl",
        orient="records",
        lines=True,
        force_ascii=False,
    )

    category_counts = (
        products_clean["category"]
        .value_counts()
        .rename_axis("category")
        .reset_index(name="product_count")
    )
    category_counts.to_csv(output_dir / "category_counts.csv", index=False, encoding="utf-8-sig")

    report = {
        "input_files": input_files,
        "raw_rows": int(before_rows),
        "clean_rows": int(len(products_clean)),
        "removed_rows": int(before_rows - len(products_clean)),
        "spec_rows": int(len(specs_long)),
        "categories": category_counts.to_dict(orient="records"),
        "output_files": OUTPUT_FILES,
    }

    with (output_dir / "processing_report.json").open("w", encoding="utf-8") as file:
        json.dump(report, file, ensure_ascii=False, indent=2)

    return report


def run_preprocessing(input_dir: Path, output_dir: Path) -> dict:
    raw = read_raw_data(input_dir)
    clean, before_rows = clean_raw_data(raw)
    products_clean, specs_long = make_product_outputs(clean)
    input_files = sorted(path.name for path in input_dir.glob("*.csv"))
    return write_outputs(products_clean, specs_long, input_files, before_rows, output_dir)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Clean and normalize product CSV data.")
    parser.add_argument("--input", type=Path, default=Path("data"), help="Input CSV folder.")
    parser.add_argument("--output", type=Path, default=Path("processed"), help="Output folder.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    report = run_preprocessing(args.input, args.output)
    print(f"Clean rows: {report['clean_rows']}")
    print(f"Spec rows: {report['spec_rows']}")
    print(f"Saved outputs to: {args.output.resolve()}")


if __name__ == "__main__":
    main()
