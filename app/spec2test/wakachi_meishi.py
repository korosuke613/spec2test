from .wakachi import Wakachi


class WakachiMeishi(Wakachi):
    def __init__(self,
                 input_path="./resource/file/",
                 output_path="./reource/wakachi/",
                 input_extension=".txt",
                 output_extension=".meishi.wakachi"
                 ):
        super().__init__(input_path, output_path, input_extension, output_extension)
        self.hinshi_list = ['名詞']
