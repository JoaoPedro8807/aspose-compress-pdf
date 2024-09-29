from main import PDFCompression
from pathlib import Path

my_path = Path(__file__).parent.joinpath('pdfs')
my_file = my_path / 'pdf-teste.pdf'

with PDFCompression() as compressor:
    compressor.build_all(  #build_all take all pdf files
        files_dir=my_path,
        quality_per_image=30,
        dir_to_save=my_path / 'results',
        max_width=1500, 
        max_heigth=1500
    )
    print(compressor.get_compartives) # get comparatives params