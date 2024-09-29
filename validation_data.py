from  pathlib import Path

class ValidationData:
    def __init__(self, *args, **kwargs) -> None:
        ...

    def validate_data(self, *args, **kwargs) -> None:
        self.data = kwargs
        self.errors = []
        self.validate_file()
        self.validate_image_length()
        self.validate_quality()
        if self.errors:
            raise ValueError(f"Erros de validação: {self.errors}")

    def validate_file(self):
        """ check all files existing """
        files = self.files_to_process
        for file in files:
            if not Path(file).is_file():
                self.errors.append(f"O arquivo {file} não existe.")

    def validate_image_length(self):
        max_width = self.data.get('max_width')
        max_height = self.data.get('max_heigth')
        if max_width <= 0 or max_height <= 0:
            self.errors.append('Largura e altura máximas devem ser positivas.')
        
    def validate_quality(self):
        quality = self.data.get('quality')
        if quality and quality not in range(1, 101):
            self.errors.append('A qualidade precisa estar entre 1 e 100.')
