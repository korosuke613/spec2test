class File:
    """ファイルを表すクラス"""
    def __init__(self,
                 file_name_,
                 extension_):
        self.name = file_name_[:-len(extension_)]
        self.extension = extension_
        self.full_name = file_name_
        self.check()

    @staticmethod
    def is_same_extension(file_name: str, extension: str) -> bool:
        """ファイル名と拡張子が同じかどうかチェックする"""
        return file_name[-len(extension):] == extension

    def check(self):
        """このクラスの整合性をチェックする"""
        if not File.is_same_extension(self.full_name, self.extension):
            raise ValueError
