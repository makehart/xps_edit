import os
import zipfile
import xml.etree.ElementTree as ET
import shutil
import argparse

def extract_xps(xps_path, extract_path):
    """Extracts an XPS (ZIP) file to a directory."""
    with zipfile.ZipFile(xps_path, 'r') as zip_ref:
        zip_ref.extractall(extract_path)

def list_strings(extract_path):
    """Lists all UnicodeString values with an index."""
    pages_path = os.path.join(extract_path, 'Documents/1/Pages')
    if not os.path.exists(pages_path):
        print("Pages directory not found!")
        return []
    
    strings = []
    index = 0
    for file_name in os.listdir(pages_path):
        if file_name.endswith(".fpage"):
            file_path = os.path.join(pages_path, file_name)
            tree = ET.parse(file_path)
            root = tree.getroot()
            
            for glyphs in root.findall(".//{http://schemas.microsoft.com/xps/2005/06}Glyphs"):
                unicode_string = glyphs.get("UnicodeString")
                if unicode_string:
                    strings.append((file_path, glyphs, unicode_string))
                    print(f"[{index}] {unicode_string[:70]}...")
                    index += 1
    return strings

def replace_by_index(strings, index, replacement_text):
    """Replaces the UnicodeString by index."""
    if 0 <= index < len(strings):
        file_path, glyphs, _ = strings[index]
        glyphs.set("UnicodeString", replacement_text)
        tree = ET.parse(file_path)
        tree.write(file_path, encoding="utf-8", xml_declaration=True)
        print(f"Replaced text at index {index} with '{replacement_text}'")

def repackage_xps(extract_path, output_xps):
    """Creates a new XPS file from the modified extracted content."""
    shutil.make_archive(output_xps.replace('.xps', ''), 'zip', extract_path)
    shutil.move(output_xps.replace('.xps', '.zip'), output_xps)

def main():
    parser = argparse.ArgumentParser(description="Scan and modify XPS text.")
    parser.add_argument("xps_file", help="Path to the .XPS file")
    parser.add_argument("--list", action="store_true", help="List all strings")
    parser.add_argument("--replace", nargs=2, metavar=("INDEX", "TEXT"), help="Replace text at given index")
    
    args = parser.parse_args()
    extract_path = "temp_xps_extracted"
    modified_xps = "modified.xps"
    
    # Extract XPS
    extract_xps(args.xps_file, extract_path)
    
    if args.list:
        strings = list_strings(extract_path)
    elif args.replace:
        index = int(args.replace[0])
        replacement_text = args.replace[1]
        strings = list_strings(extract_path)
        replace_by_index(strings, index, replacement_text)
        repackage_xps(extract_path, modified_xps)
        print(f"Modified XPS saved as: {modified_xps}")
    
    # Cleanup
    shutil.rmtree(extract_path)

if __name__ == "__main__":
    main()
