import os
from docx import Document

def verify_docx():
    target_dir = r"d:\AntiGravity\«—∞°∂˜ƒ¡≈Ÿ√˜∆¿¿Â\?êÏ£º?òÎßê?Ä.doc\2024-2025"
    files = [f for f in os.listdir(target_dir) if f.endswith('.docx') and not f.startswith('~$')]
    
    if not files:
        print("No DOCX files found.")
        return

    # Pick the first one
    file_path = os.path.join(target_dir, files[0])
    print(f"Verifying: {files[0]}")
    
    try:
        doc = Document(file_path)
        print("--- Document Content Start ---")
        for i, para in enumerate(doc.paragraphs[:10]):
            print(f"{i}: {para.text}")
        print("--- Document Content End ---")
    except Exception as e:
        print(f"Error reading DOCX: {e}")

if __name__ == "__main__":
    verify_docx()
