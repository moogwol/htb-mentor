
from pathlib import Path
from pypdf import PdfReader

from database.writeups import add_writeup


def extract_content(file_path):
    """Extract text from PDF or Markdown files."""

    file_path = Path(file_path)

    if file_path.suffix.lower() == ".pdf":
        reader = PdfReader(file_path)
        content = "\n\n".join(
            page.extract_text() or ""
            for page in reader.pages
        )

    elif file_path.suffix.lower() in [".md", ".txt"]:
        content = file_path.read_text(encoding="utf-8")

    else:
        raise ValueError("Unsupported file format.")

    if not content.strip():
        raise ValueError("No text could be extracted from the file.")

    return content


def import_writeup(machine_id, file_path, title, source=None, db_path=None):
    """Import a walkthrough into the knowledge base."""

    content = extract_content(file_path)

    return add_writeup(
        machine_id=machine_id,
        title=title,
        content=content,
        source=source,
        db_path=db_path
    )
