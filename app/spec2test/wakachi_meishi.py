from .wakachi import Wakachi


class WakachiMeishi(Wakachi):
    def __init__(self,
                 input_path="./resource/file/",
                 output_path="./resource/wakachi/"
                 ):
        super().__init__(input_path, output_path, ".txt", ".meishi.wakachi")
        self.hinshi_list = ['名詞']
