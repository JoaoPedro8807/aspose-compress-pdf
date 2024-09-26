import aspose.words as aw
from typing import Any
import os
from pathlib import Path
from collections import defaultdict

class Compress:
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        ...

    def set_pdf_page_size(self, page_setup: Any, width: int, height: int) -> None:
        page_setup.page_width = width
        page_setup.page_height = height

    def compact(self,  
                file: str, 
                max_width: int = 1500, 
                max_height: int = 1500, 
                quality: int = 50,
                *args,
                **kwargs
                ) -> Any:
        
        """ build the compact pdf, with quality param """
        
        pdf_read_options = aw.pdf2word.fixedformats.PdfFixedOptions()
        pdf_read_options.image_format = aw.pdf2word.fixedformats.FixedImageFormat.JPEG
        pdf_read_options.jpeg_quality = quality
        
        renderer = aw.pdf2word.fixedformats.PdfFixedRenderer()

        with open(file, 'rb') as pdf_stream:
                aspose_image = renderer.save_pdf_as_images(pdf_stream, pdf_read_options)

        for i in range(0, len(aspose_image)):
            page_setup = self.builder.page_setup
            self.set_pdf_page_size(page_setup, max_width, max_height) #set the image size in current page

            page_image = self.builder.insert_image(aspose_image[i])

            self.set_pdf_page_size(page_setup, page_image.width, page_image.height) 
            page_setup.top_margin = 0
            page_setup.left_margin = 0
            page_setup.bottom_margin = 0
            page_setup.right_margin = 0

            if i != len(aspose_image) - 1: # break increment in the last page 
                self.builder.insert_break(aw.BreakType.SECTION_BREAK_NEW_PAGE)

            #self.save(file=pdf_stream, name=kwargs.get('name'))
        return self.builder.document
    
    def save(self, 
             file: Any,
             name: str = '', 
             path: Path | str = '',
             *args,
             **kwargs
            ) -> None:
        
        save_options = aw.saving.PdfSaveOptions()
        save_options.cache_background_graphics = True

        if path and isinstance(path, str):
            path = Path(path)

        name = name or file.name
        if not name.endswith('.pdf'): 
            name += '.pdf'  # make sure the file will save .pdf
        save = path / name
        self.builder.document.save(str(save), save_options)

        