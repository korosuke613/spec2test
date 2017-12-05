from abc import ABC, abstractmethod
from .directory import Directory


class IOManager(ABC):
    """抽象基底クラス"""
    def __init__(self,
                 input_dir_path_,
                 output_dir_path_,
                 input_extension_,
                 output_extension_):
        self.input = Directory(input_dir_path_, input_extension_)
        self.output = Directory(output_dir_path_, output_extension_)
        self.import_io_files()

    @abstractmethod
    def generate(self):
        pass

    def import_io_files(self):
        """ディレクトリにファイルを登録する"""
        self.input.import_files()
        self.output.import_files()
