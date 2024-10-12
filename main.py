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
        self.comparative: list[tuple] = [] #list of tuple with (file, old_size, new_size)
        
    def __str__(self) -> str:
        return  f'PDFCompression working with directory {self.pdf_dir}'

    @property
    def files(self):
        return self.files_to_process
    
    @files.setter
    def files(self, files: list[Path]):
        self.files_to_process = files

    @property
    def get_compartives(self):
        """ return files sizes compartives before and after """
        result = []
        for build in self.comparative:
            total = build[1] 
            dif = build[1] - build[2]
            perct = round((dif * 100) / total , 3)
            result.append(f'O arquivo {build[0]} foi de {build[1]} kb para {build[2]} kb, redução de {perct}%')
        return result


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

        print(f'Inicializando a fila de compressão em {self.files_to_process}')
                                
        self.init_validate( 
            quality=quality, 
            max_width=max_width, 
            max_heigth=max_heigth
        )    
        self.construct(
            original_file=file,
            dir_to_save=dir_to_save,
            quality=quality,
            name=name,
            max_heigth=max_heigth,
            max_width=max_width)

    def construct(
            self, 
            original_file:  Path | str, 
            dir_to_save:  Path | str, 
            quality: int,
            name: str = '',
            max_width: int = 1500, 
            max_heigth: int = 1500):
        
        name = name or original_file.name
        if not name.endswith('.pdf'): 
            name += '.pdf'  # make sure the file will save .pdf
            
        stream = self.compact(
            file=original_file, 
            max_width=max_width, 
            max_height=max_heigth, 
            quality=quality
            )
        
        self.save(file=stream, name=name, path=dir_to_save)

        new_file_path = Path(dir_to_save) / name 
        new_size = os.path.getsize(str(new_file_path))
        original_size = os.path.getsize(original_file)
        self.comparative.append((original_file.name, original_size, new_size))


    def save(self, 
        file: aw.Document,
        name: str = '', 
        path: Path | str = '',
        *args,
        **kwargs
    ) -> None:
        save_options = aw.saving.PdfSaveOptions()
        save_options.cache_background_graphics = True

        #if path and isinstance(path, str):
        path = Path(path)                                                                   
        if not path.exists():                       
            path.mkdir(parents=True, exist_ok=True)

        if not name:
            name = file.original_file_name
        ouput_path = path / name

        self.builder.document.save(str(ouput_path), save_options)  # Salva diretamente o documento no fluxow  


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

        print(f'Inicializando a fila de compressão em {files_dir}, com os  arquivos: {self.files_to_process}')

        self.init_validate(
            quality=quality_per_image, 
            max_width=max_width, 
            max_heigth=max_heigth
        )

        for i, file in enumerate(self.files_to_process):
            name = file.name
            self.construct(
                original_file=file,
                dir_to_save=dir_to_save,
                quality=quality_per_image,
                name=name,
                max_width=max_width,
                max_heigth=max_heigth
            )
     
            
    def init_validate(self, *args, **kwargs) -> None:
        self.validate_data(*args, **kwargs)

    def __repr__(self) -> str:
        return f'PDFCompression(pdf_dir={self.pdf_dir})'
    
    def __len__(self) -> int:
        return len(self.files_to_process)
    
    def __enter__(self):
        print(f'PDFCompression inicializado com sucesso!')
        return self
    
    def __exit__(self, exec_type, exec_value, traceback):
        if exec_type:
            print(f'error: {exec_value}')
        else:
            print(f'Compressão concluida com sucesso, {len(self.files_to_process)} de arquivos processados')    






            