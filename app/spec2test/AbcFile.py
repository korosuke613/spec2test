from abc import ABC


class AbcBase(ABC):
    def __init__(self):
        self.__wdp = None
        self.__idp = None
        self.__odp = None
        self.__ie = None
        self.__oe = None

    @property
    def work_dir_path(self) -> str:
        return self.__wdp

    @work_dir_path.setter
    def work_dir_path(self, path: str):
        self.__wdp = path

    @property
    def input_dir_path(self) -> str:
        """ファイルを読み込むディレクトリ"""
        return self.work_dir_path + self.__idp

    @input_dir_path.setter
    def input_dir_path(self, path: str):
        self.__idp = path

    @property
    def output_dir_path(self) -> str:
        """ファイルを書き出すディレクトリ"""
        return self.work_dir_path + self.__odp

    @output_dir_path.setter
    def output_dir_path(self, path: str):
        """ファイルを書き出すディレクトリ"""
        self.__odp = path

    @property
    def input_extension(self) -> str:
        """入力ファイルの拡張子"""
        return self.__ie

    @input_extension.setter
    def input_extension(self, extension: str):
        """入力ファイルの拡張子"""
        self.__ie = extension

    @property
    def output_extension(self) -> str:
        return self.__oe

    @output_extension.setter
    def output_extension(self, extension: str):
        self.__oe = extension

    def set_path(self,
                 work_dir_path_: str,
                 input_dir_path_: str,
                 output_dir_path_: str,
                 ):
        self.work_dir_path = work_dir_path_
        self.input_dir_path = input_dir_path_
        self.output_dir_path = output_dir_path_

    def set_extension(self,
                      input_extension_: str,
                      output_extension_: str):
        self.input_extension = input_extension_
        self.output_extension = output_extension_
