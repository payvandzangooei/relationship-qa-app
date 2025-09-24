import os
import gdown
import pdfplumber

def download_pdfs_from_drive(folder_url, output_dir="pdfs"):
    """
    Downloads all PDFs from a public Google Drive folder into local 'pdfs/'.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Extract folder ID from the shared URL
    if "folders/" in folder_url:
        folder_id = folder_url.split("folders/")[1].split("?")[0]
    else:
        raise ValueError("Invalid Google Drive folder link.")

    # Use gdown to list and download files
    file_list = gdown.download_folder(id=folder_id, output=output_dir, quiet=False, use_cookies=False)
    return file_list

def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

def extract_text_from_folder(folder_path):
    all_text = ""
    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            file_path = os.path.join(folder_path, filename)
            all_text += extract_text_from_pdf(file_path)
    return all_text