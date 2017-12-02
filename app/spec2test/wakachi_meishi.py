from .wakachi import Wakachi


class WakachiMeishi(Wakachi):
    """名詞のみの分かち書きに関するクラス"""
    def __init__(self,
                 input_path="./resource/file/",
                 output_path="./resource/wakachi/"
                 ):
        super().__init__(input_path, output_path)
        self.output.default_extension = ".meishi.wakachi"
        self.hinshi_list = ['名詞']
