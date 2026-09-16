# RAG Ready Markdown

`rag-ready-markdown` aims to convert text-based source content into cleaned, structured Markdown tailored for:

- RAG ingestion pipelines
- Knowledge-management systems
- Searchable internal documentation

## Repository status

Current status: documentation-only project brief. A concrete CLI/library interface is not yet implemented.
Today, this repository serves as a proposed specification for supported inputs and normalization goals.
Next milestone: implement an initial converter for `.txt` and `.md` inputs.
No runnable examples or converter acceptance tests are included yet.

## Proposed workflow

Future workflow once implemented:

1. Provide supported text-based input (`.txt` or existing `.md`).
2. Apply the planned normalization and structuring workflow to produce clean Markdown.
3. Send the cleaned Markdown output to your chunking/embedding pipeline.

## RAG-ready definition

In this repository, "RAG-ready" means Markdown output that is predictable, clean, and easy to split into semantically meaningful chunks.

## What you can do now

- Review and refine the proposed scope.
- Propose normalization and Markdown-structuring rules.
- Help define the first CLI/library converter interface.

## Planned converter behavior

- Will process supported text-based source content.
- Will normalize noisy formatting.
- Will structure content into consistent Markdown sections.
- Will output Markdown that is easier to chunk, embed, and retrieve.

Expected normalization and structuring rules include:

- Remove repeated whitespace and empty-line noise.
- Preserve heading hierarchy and section boundaries.
- Normalize list and paragraph formatting for consistent chunking.

## Proposed scope (first implementation milestone)

Supported inputs include:

- `.txt` plain text content
- existing `.md` Markdown content

Not supported in the first milestone:

- PDF inputs and other OCR-dependent document sources (including scanned documents)
