import aspose.words as aw
from typing import Any
import os
from pathlib import Path
from compress import Compress
from validation_data import ValidationData


class PDFCompression(ValidationData, Compress):
    def __init__(self, pdf_dir:str = '') -> None:
        self.pdf_dir: Path = Path(pdf_dir) if pdf_dir else Path()
        self.builder = aw.DocumentBuilder()
        self.files_to_process: list[Path] = []
        
    def __str__(self) -> str:
        return  f'PDFCompression work with directory {self.pdf_dir}'

    @property
    def files(self):
        return self.files_to_process
    
    @files.setter
    def files(self, files: list[Path]):
        self.files_to_process = files


    def build(self,
            file: str, 
            quality: int, 
            name: str = '',
            dir_to_save: Path | str = '',
            max_width: int = 1500, 
            max_heigth: int = 1500,
            ) -> Any:    
        """" 
        Build a compact PDF file.

    Parameters:
        file (str, required): The path to the PDF file to compress.
        quality (int, required): The quality level for the compression (0-100).
        name (str, optional): The name of the output file (without extension).
        dir_to_save (Path, or, required): The directory where the output file will be saved.
        max_width (int, optional): The maximum width for the output PDF pages. Default is 1500.
        max_height (int, optional): The maximum height for the output PDF pages. Default is 1500.

        """
                     
        self.files_to_process = [file]                                         

        self.init_validate( 
            quality=quality, 
            max_width=max_width, 
            max_heigth=max_heigth
        )    

        stream = self.compact(
            file=file, 
            max_width=max_width, 
            max_height=max_heigth, 
            quality=quality
            )
        self.save(stream, name, dir_to_save)

    def build_all(self, 
            files_dir: Path | str, 
            quality_per_image: int, 
            dir_to_save: Path | str = '',
            name: str = '',
            max_width: int = 1500, 
            max_heigth: int = 1500) -> None:
        """ 
            Build all pdfs files (only pdf files) at the path

        Parameters:
        file_dir (Path or str, required): The path to the PDFs files to compress.
        quality_per_image (int, required): The quality level for the compression (0-100).
        name (str, optional): The name of the output file,  will be save with the int increment in the end of name ex: (teste-1.pdf)
        dir_to_save (Path, or, required): The directory where the output file will be saved.
        max_width (int, optional): The maximum width for the output PDF pages. Default is 1500.
        max_height (int, optional): The maximum height for the output PDF pages. Default is 1500.

        """

        if isinstance(files_dir, str):
            files_dir = Path(files_dir)

        #get only pdfs files
        self.files_to_process = [file for file in files_dir.iterdir() if file.is_file() and file.suffix == '.pdf']

        self.init_validate(
            quality=quality_per_image, 
            max_width=max_width, 
            max_heigth=max_heigth
        )

        for i, file in enumerate(self.files_to_process):
            if name: #if name does not exist, will be save with older name
                name = f'{name}-{i}'
            stream = self.compact(
                file=file,
                max_height=max_heigth,
                max_width=max_width,
                quality=quality_per_image
            )
            self.save(file=stream, name=name, path=dir_to_save)
            
    def init_validate(self, *args, **kwargs) -> None:
        self.validate_data(*args, **kwargs)

    def __repr__(self) -> str:
        return f'PDFCompression(pdf_dir={self.pdf_dir})'
    
    def __len__(self) -> int:
        return len(self.files_to_process)
    
    def __enter__(self):
        print(f'Iniciando a compressão do diretório {self.pdf_dir}')
        return self
    
    def __exit__(self, exec_type, exec_value, traceback):
        if exec_type:
            print(f'error: {exec_value}')
        else:
            print(f'Compressãoc concluida com sucesso, {len(self.files_to_process)} de arquivos processados')    


my_path = Path(__file__).parent.joinpath('pdfs')

# pdf_builder = PDFCompression()
# doc = pdf_builder.build(
#     file=my_path / ''teste0.pdf'',
#     quality=30,
#     max_heigth=1500,
#     max_width=1500)
#print('DOC: ', doc)

with PDFCompression() as compressor:
    print(compressor)
    compressor.build_all(
        files_dir=my_path,
        name='teste-all',
        dir_to_save= my_path.parent / 'teste',
        quality_per_image=30,
        max_heigth=1500,
        max_width=1500
    )





        