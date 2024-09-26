import aspose.words as aw
from typing import Any
import os
from pathlib import Path
from collections import defaultdict

class ValidationData:
    def __init__(self) -> None:
        self.errors = defaultdict(list)

    def validate_data(self):
        #self.validation_quality()
        ...
        
    def validation_quality(self, quality: int):
        if quality not in range(1, 100):
            raise ValueError('A qualidade precisa estar entre 1 e 100')


class PDFCompression(ValidationData):
    def __init__(self, pdf_dir:str = '') -> None:
        self.pdf_dir = pdf_dir
        
    
        
    def set_pdf_page_size(self, page_setup: Any, width: int, height: int) -> None:
        page_setup.page_width = width
        page_setup.page_height = height


    def build(self,
            file: str, 
            quality: int, 
            max_widht: int = 1500, 
            max_heigth: int = 1500,
            save_with: str = ''
            ) -> None:                                                                                          
        self.compact(
            file=file, 
            max_width=max_widht, 
            max_height=max_heigth, 
            quality=quality, 
            save_with=save_with)

    def build_all(self, 
            files_dir: str | list[str], 
            quality_per_image: int, 
            max_widht: int = 1500, 
            max_heigth: int = 1500) -> None:
        
        files = os.listdir(self.pdf_dir)
        if isinstance(files_dir, list):
            files = [os.listdir(f) for f in files_dir]
        
        for file in files:
            original_pdf = os.path.join(self.pdf_dir, file)
            self.compact(
                file=original_pdf,
                max_height=max_heigth,
                max_width=max_widht,
                quality=quality_per_image
            )
            

    def compact(self,  
                file: str, 
                save_with: str = '', 
                max_width: int = 1500, 
                max_height: int = 1500, 
                quality: int = 50):
        
        """ build the compact pdf, with quality param """
        self.validate_data()
        self.validation_quality(quality=quality)
        
        pdf_read_options = aw.pdf2word.fixedformats.PdfFixedOptions()
        pdf_read_options.image_format = aw.pdf2word.fixedformats.FixedImageFormat.JPEG
        pdf_read_options.jpeg_quality = quality
        
        renderer = aw.pdf2word.fixedformats.PdfFixedRenderer()

        with open(file, 'rb') as pdf_stream:
                aspose_image = renderer.save_pdf_as_images(pdf_stream, pdf_read_options);

        builder = aw.DocumentBuilder()
        for i in range(0, len(aspose_image)):
            page_setup = builder.page_setup
            self.set_pdf_page_size(page_setup, max_width, max_height) #set the image size in current page

            page_image = builder.insert_image(aspose_image[i])

            self.set_pdf_page_size(page_setup, page_image.width, page_image.height) 
            page_setup.top_margin = 0
            page_setup.left_margin = 0
            page_setup.bottom_margin = 0
            page_setup.right_margin = 0

            if i != len(aspose_image) - 1:
                builder.insert_break(aw.BreakType.SECTION_BREAK_NEW_PAGE)

        save_options = aw.saving.PdfSaveOptions()
        save_options.cache_background_graphics = True
        if save_with:
            name = save_with.replace('.pdf', '') #make sure that have a .pdf
            builder.document.save(f'{name}.pdf', save_options)
        else:
            builder.document.save(pdf_stream.name, save_options)


my_path = Path(__file__).parent.joinpath('pdfs')

pdf_builder = PDFCompression(pdf_dir=my_path)
pdf_builder.build(
    file=my_path / 'teste0.pdf',
    quality=30,
    max_heigth=1500,
    max_widht=1500,
    save_with='testando.pdf'
    )



        