import re
import shutil
from collections import Counter
from datetime import date
from pathlib import Path

import fitz

INPUT_FOLDER = Path("input")
OUTPUT_FOLDER = Path("output")
MIN_REPEATED_OCCURRENCES = 3
TOP_LINES_TO_CHECK = 3
BOTTOM_LINES_TO_CHECK = 3


def repair_encoding(text):
    if not any(marker in text for marker in ("Ã", "â", "ð")):
        return text
    try:
        repaired = text.encode("cp1252").decode("utf-8")
        return repaired if repaired.count("�") <= text.count("�") else text
    except UnicodeError:
        return text


def page_lines(text):
    text = repair_encoding(text.replace("\r\n", "\n").replace("\r", "\n"))
    return [line.strip() for line in text.split("\n") if line.strip()]


def repeated_page_lines(pages):
    top = Counter()
    bottom = Counter()
    for page in pages:
        lines = page_lines(page)
        top.update(lines[:TOP_LINES_TO_CHECK])
        bottom.update(lines[-BOTTOM_LINES_TO_CHECK:])
    headers = {line for line, count in top.items() if count >= MIN_REPEATED_OCCURRENCES}
    footers = {line for line, count in bottom.items() if count >= MIN_REPEATED_OCCURRENCES}
    return headers, footers


def clean_page(text, headers, footers, kept_furniture):
    lines = page_lines(text)
    content = []
    for index, line in enumerate(lines):
        at_edge = index < TOP_LINES_TO_CHECK or index >= len(lines) - BOTTOM_LINES_TO_CHECK
        if at_edge and (line in headers or line in footers):
            if line in kept_furniture:
                continue
            kept_furniture.add(line)
        if re.fullmatch(r"\d{1,4}", line):
            continue
        content.append(line)
    return content


def is_heading(line):
    return bool(
        re.match(r"^(?:CHAPTER|Chapter)\s+\d+(?:\s*[:.]|\s+)", line)
        or re.match(r"^(?:Epilogue|Index|Preface|Acknowledgments)\b", line)
    )


def join_paragraph_lines(lines):
    output = []
    for line in lines:
        if is_heading(line) or line.startswith(("Figure ", "Table ", "• ", "- ", "* ")):
            output.append(line)
        elif output and output[-1] and not is_heading(output[-1]):
            output[-1] += " " + line
        else:
            output.append(line)
    return output


def markdown_lines(lines):
    result = []
    for line in join_paragraph_lines(lines):
        chapter = re.match(r"^CHAPTER\s+(\d+)\s+(.+)$", line)
        chapter_colon = re.match(r"^Chapter\s+(\d+)\s*:\s*(.+)$", line)
        if chapter:
            result.append(f"# Chapter {chapter.group(1)}: {chapter.group(2).strip()}")
        elif chapter_colon:
            result.append(f"# Chapter {chapter_colon.group(1)}: {chapter_colon.group(2).strip()}")
        elif re.match(r"^(?:Epilogue|Index|Preface|Acknowledgments)\b", line):
            result.append(f"## {line}")
        elif line.startswith("• "):
            result.append("- " + line[2:])
        else:
            result.append(line)
    return result


def split_chapters(lines):
    sections = []
    current = None
    for line in lines:
        match = re.match(r"^# Chapter (\d+):\s*(.+)$", line)
        if match:
            if current:
                sections.append(current)
            current = {"number": int(match.group(1)), "title": match.group(2).strip(), "lines": [line]}
        elif current:
            current["lines"].append(line)
    if current:
        sections.append(current)
    return sections


def safe_name(value):
    value = re.sub(r"[^A-Za-z0-9 -]+", "", value).strip()
    return re.sub(r"\s+", "-", value).lower()


def frontmatter(title, source_name, chapter):
    return [
        "---",
        f'title: "{title}"',
        'author: "Chip Huyen"',
        f'source_file: "{source_name}"',
        'file_type: "pdf"',
        f'chapter: "Chapter {chapter}"',
        f'converted_date: "{date.today().isoformat()}"',
        "---",
        "",
    ]


def main():
    pdf_files = list(INPUT_FOLDER.glob("*.pdf"))
    if not pdf_files:
        raise SystemExit("ERROR: No PDF file found in the input folder.")

    pdf_path = pdf_files[0]
    document = fitz.open(pdf_path)
    raw_pages = [page.get_text("text") for page in document]
    headers, footers = repeated_page_lines(raw_pages)
    kept_furniture = set()
    all_lines = []
    for raw_page in raw_pages:
        all_lines.extend(clean_page(raw_page, headers, footers, kept_furniture))

    cleaned_lines = markdown_lines(all_lines)
    chapters = split_chapters(cleaned_lines)
    if not chapters:
        raise SystemExit("ERROR: No chapter headings were detected.")

    title = "AI Engineering: Building Applications with Foundation Models"
    book_dir = OUTPUT_FOLDER / "client-sample"
    if book_dir.exists():
        shutil.rmtree(book_dir)
    chapters_dir = book_dir / "chapters"
    chapters_dir.mkdir(parents=True, exist_ok=True)

    index_lines = [f"# {title}", "", "Converted from the source PDF for retrieval workflows.", "", "## Chapters", ""]
    for chapter in chapters:
        filename = f"chapter-{chapter['number']:02d}-{safe_name(chapter['title'])}.md"
        body = frontmatter(title, repair_encoding(pdf_path.name), chapter["number"])
        body.extend(chapter["lines"])
        (chapters_dir / filename).write_text("\n".join(body) + "\n", encoding="utf-8")
        index_lines.append(f"- [Chapter {chapter['number']}: {chapter['title']}](chapters/{filename})")

    (book_dir / "index.md").write_text("\n".join(index_lines) + "\n", encoding="utf-8")
    report = [
        "# Conversion Quality Report",
        "",
        f"- Source: `{pdf_path.name}`",
        f"- Pages: {len(raw_pages)}",
        f"- Chapters: {len(chapters)}",
        f"- Repeated page headers detected: {len(headers)}",
        f"- Repeated page footers detected: {len(footers)}",
        "- OCR: not run; source text was extractable with PyMuPDF",
        "- Notes: tables and figures remain text-based and may need manual review.",
    ]
    (book_dir / "quality-report.md").write_text("\n".join(report) + "\n", encoding="utf-8")
    print(f"Created {len(chapters)} chapter files in {book_dir}")


if __name__ == "__main__":
    main()
