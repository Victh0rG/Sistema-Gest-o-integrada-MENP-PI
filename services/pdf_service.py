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

    def pdf_has_text(self) -> str:
        """Extrai e retorna o texto de todas as páginas."""
        full_text = []
        for i, page in enumerate(self.reader.pages):
            text = page.extract_text()
            if text:
                full_text.append(text)
        result = "\n".join(full_text)
        print(result)
        return result  # ← antes só lia página 0

    def pdf_has_image(self) -> list[str]:
        """Salva todas as imagens de todas as páginas e retorna os caminhos."""
        saved_paths = []

        for page_num, page in enumerate(self.reader.pages):
            for i, image_file_object in enumerate(page.images):
                file_name = f"out-image-page{page_num}-{i}-{image_file_object.name}"
                image_file_object.image.save(file_name)
                saved_paths.append(file_name)
                print(f"Imagem salva: {file_name}")

        return saved_paths  # ← antes não retornava nada

    def read_pdf(self) -> str | list[str]:
        """
        Lê o PDF e retorna:
        - string com o texto completo, se o PDF tiver texto
        - lista de caminhos das imagens salvas, se for escaneado
        """
        if self.has_txt():
            print("PDF com texto detectado")
            return self.pdf_has_text()
        else:
            print("PDF escaneado — extraindo imagens")
            return self.pdf_has_image()