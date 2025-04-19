# PDF Tools App

A GUI application built with `customtkinter` to:
- Add sequential page counters to PDFs
- Extract Data Matrix codes from PDFs to CSV (using OCR and computer vision)
- Match extracted patterns with Excel/CSV sources

## Tabs

1. **Page Counter** - Add running number stamps to PDF pages.
2. **Data Matrix Extractor** - Convert PDF to images, scan for matrix codes using OCR.
3. **Pattern Finder** - Match patterns between scanned barcodes and source files.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt

2. Run the app:
```bash
python app.py
```

## Requirements

- Python 3.8+
- Tesseract, poppler, and GhostScript may be required for PDF/image operations.
