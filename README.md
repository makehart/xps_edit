# XPS Text Scanner & Modifier

A Python application to scan, list, and modify text inside **XPS (XML Paper Specification) files**. This tool extracts text from `<Glyphs UnicodeString="..."/>` elements, allowing you to search and replace text in **fixed-layout XPS documents**.

## 🔥 Features
- **List all text strings** inside an XPS file with an index.
- **Modify a specific text entry** by its index.
- **Repackage the modified XPS file** after changes.
- Uses **XML parsing** to edit text efficiently.

## How It Works
Extracts the .XPS file (which is actually a ZIP archive).
Parses .fpage XML files to find <Glyphs> elements.
Lists text inside UnicodeString attributes.
Replaces selected text and repackages the XPS file.

1️⃣ List all text entries:
python script.py myfile.xps --list

2️⃣ Replace a text entry (by index):
python script.py myfile.xps --replace 2 "New Text"

