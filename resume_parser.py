import os
import fitz  # PyMuPDF

def parse_pdf_resume(path):
    doc = fitz.open(path)
    text = "\n".join([page.get_text() for page in doc])
    doc.close()
    return text

def parse_resume_folder(folder):
    resumes = []
    files = [f for f in os.listdir(folder) if f.endswith(".pdf")]
    total = len(files)
    print(f"[DEBUG] Found {total} PDF resumes in folder '{folder}'.")

    for i, file in enumerate(files, 1):
        path = os.path.join(folder, file)
        content = parse_pdf_resume(path)
        resumes.append({
            "name": os.path.splitext(file)[0],
            "content": content
        })
        print(f"[DEBUG] Parsed {i}/{total}: {file}")

    return resumes