from abc import ABC, abstractmethod


class AbcBase(ABC):
    def __init__(self):
        self.__wdp = None
        self.__idp = None
        self.__odp = None
        self.__ie = None
        self.__oe = None

    @property
    def work_dir_path(self):
        return self.__wdp

    @work_dir_path.setter
    def work_dir_path(self, path):
        self.__wdp = path

    @property
    def input_dir_path(self):
        """ファイルを読み込むディレクトリ"""
        return self.work_dir_path + self.__idp

    @input_dir_path.setter
    def input_dir_path(self, path):
        self.__idp = path

    @property
    def output_dir_path(self):
        """ファイルを書き出すディレクトリ"""
        return self.work_dir_path + self.__odp

    @output_dir_path.setter
    def output_dir_path(self, path):
        """ファイルを書き出すディレクトリ"""
        self.__odp = path

    @property
    def input_extension(self):
        """入力ファイルの拡張子"""
        return self.__ie

    @input_extension.setter
    def input_extension(self, extension):
        """入力ファイルの拡張子"""
        self.__ie = extension

    @property
    def output_extension(self):
        return self.__oe

    @output_extension.setter
    def output_extension(self, extension):
        self.__oe = extension

    def set_path(self,
                 work_dir_path_,
                 input_dir_path_,
                 output_dir_path_,
                 ):
        self.work_dir_path = work_dir_path_
        self.input_dir_path = input_dir_path_
        self.output_dir_path = output_dir_path_

    def set_extension(self,
                      input_extension_,
                      output_extension_):
        self.input_extension = input_extension_
        self.output_extension = output_extension_
