# RAG Ready Markdown

`rag-ready-markdown` is intended to convert text-based source content into cleaned, structured Markdown tailored for:

- RAG ingestion pipelines
- Knowledge-management systems
- Searchable internal documentation

Current status: repository scope and workflow definition. A concrete CLI/library interface is not yet implemented.
Today, this repository serves as a specification for supported inputs and normalization goals.
Next milestone: add an initial converter implementation for `.txt` and `.md` inputs.

## Proposed workflow

1. Provide supported text-based input (`.txt` or existing `.md`).
2. Apply the repository's planned normalization and structuring workflow to produce clean Markdown.
3. Send the cleaned Markdown output to your chunking/embedding pipeline.

## What it does

- Processes supported text-based source content.
- Normalizes noisy formatting.
- Structures content into consistent Markdown sections.
- Outputs Markdown that is easier to chunk, embed, and retrieve.

## Scope

Supported inputs include:

- `.txt` plain text content
- existing `.md` Markdown content

Not supported at this time:

- PDF files (both machine-readable and image-based)
- Scanned documents and other OCR-dependent sources
