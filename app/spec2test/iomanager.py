from abc import ABC, abstractmethod
from directory import Directory


class IOManager(ABC):
    """ファイルを生成するクラスの抽象クラス"""
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
        """何かを生成する為の抽象メソッド"""
        pass

    def import_io_files(self):
        """ディレクトリにファイルを登録する"""
        self.input.import_files()
        self.output.import_files()


class IOManagerDirectory(IOManager):
    def __init__(self,
                 input_dir_: Directory,
                 output_dir_: Directory):
        super().__init__(input_dir_.path, output_dir_.path,
                         input_dir_.default_extension, output_dir_.default_extension)

    def generate(self):
        raise NotImplementedError
