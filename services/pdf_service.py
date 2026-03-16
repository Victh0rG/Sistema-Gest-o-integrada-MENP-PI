# Extração de texto PDF
from pypdf import PdfReader

def pdf_has_text(pdf_file):
    reader = PdfReader(pdf_file)
    page = reader.pages[0]
    text = page.extract_text()
    print(text)
    return text
    # for page in reader.pages:
    #     text = page.extract_text()
    #     if text and text.strip():
    #         return True
    #     return False

def pdf_has_image(pdf_file):
    reader = PdfReader(pdf_file)
    page = reader.pages[0]
    for i, image_file_object in enumerate(page.images):
        file_name = "out-image-" + str(i) + "-" + image_file_object.name
        image_file_object.image.save(file_name)