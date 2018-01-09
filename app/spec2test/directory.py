import os
from typing import Iterator, Tuple

from file import File


class Directory:
    """ディレクトリを表すクラス"""
    def __init__(self,
                 path_,
                 default_extension_=None,
                 is_import_=False):
        self.path = path_
        self.default_extension = default_extension_
        self.file_dict = {}
        if is_import_:
            self.import_files()

    def append_file(self, file_name: str, extension: str=None):
        """ファイルクラスを追加する"""
        if extension is None:
            extension = self.default_extension
        if not File.is_same_extension(file_name, extension):
            return
        file = File(file_name, extension)
        self.file_dict[file_name] = file

    def import_files(self, extension=None):
        """ディレクトリ内の指定した拡張子のファイルをすべて追加する"""
        if self.path is None:
            return
        for file in os.listdir(self.path):
            self.append_file(file, extension)

    def get_file_path(self, file_name: str)-> str:
        """あるファイルのファイルパスを返す"""
        return self.path + self.file_dict[file_name].full_name

    def judge(self, file: File, is_add_test_):
        if file.extension != self.default_extension:
            return False
        if is_add_test_:
            return True
        if file.name[:len("test_")] != "test_":
            return True
        return False

    def get_file_path_list(self, is_add_test_: bool=True) -> list:
        """ディレクトリ内の全てのファイルのファイルパスを返す"""
        return [self.path + file.full_name for file in self.file_dict.values() if self.judge(file, is_add_test_)]

    def get_file_list(self, is_add_test_=True):
        return [file for file in self.file_dict.values() if self.judge(file, is_add_test_)]

    def file_dict_generator(self)->Iterator[Tuple[File, str]]:
        for file in self.file_dict.values():
            yield file, self.get_file_path(file.full_name)


def main():
    directory = Directory("./", ".py")
    directory.import_files(".py")


if __name__ == '__main__':
    main()
