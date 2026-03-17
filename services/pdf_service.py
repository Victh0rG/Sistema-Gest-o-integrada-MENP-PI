# Extração de texto PDF e Transformação em imagem
from pypdf import PdfReader

class PdfFileReader:
    def __init__(self, pdf_file):
        self.pdf_file = pdf_file
        self.reader = PdfReader(pdf_file)

    def has_txt(self):

        for page in self.reader.pages:
            text = page.extract_text()
            if text and text.strip():
                return True
        return False

    def pdf_has_text(self):

        page = self.reader.pages[0]
        text = page.extract_text()
        print(text)
        return text

    def pdf_has_image(self):

        page = self.reader.pages[0]
        for i, image_file_object in enumerate(page.images):
            file_name = "out-image-" + str(i) + "-" + image_file_object.name
            image_file_object.image.save(file_name)

    def read_pdf(self, pdf_file ):
        self.__init__(pdf_file)

        if self.has_txt():
            print("Pdf com texto detectado")
            return self.pdf_has_text()
        else:
            return self.pdf_has_image()

