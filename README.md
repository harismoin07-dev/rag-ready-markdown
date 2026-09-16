# PDF to Markdown Converter

This project converts a text-extractable PDF into cleaned, structured Markdown suitable for RAG ingestion and knowledge-management workflows.

## Run

Place a PDF in `input/`, then run:

```powershell
python convert.py
```

The converter creates a cleaned book folder in `output/` containing:

- `chapters/` with one Markdown file per chapter
- YAML frontmatter for each chapter
- `index.md` linking the chapters
- `quality-report.md` with conversion notes
- A book-specific `README.md`

## Cleanup

The pipeline removes repeated page headers and footers, standalone page numbers, broken paragraph line breaks, and common PDF encoding artifacts. It preserves chapter content, figures, tables, lists, citations, and footnotes as extracted text where possible.

## Client Sample

The shareable archive is:

`output/pdf-markdown-conversion-sample.zip`

The sample includes the cleaned chapter files, index, quality report, and documentation.

## Requirements

Install the PDF extraction dependency if needed:

```powershell
python -m pip install PyMuPDF
```

Scanned PDFs may require a separate OCR workflow using OCRmyPDF or Tesseract. Tables and figures extracted from PDFs may require manual review because their visual layout is not reconstructed automatically.
