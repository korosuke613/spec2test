from gensim.models import word2vec
import os
from .wakachi import Wakachi


class Model:
    def __init__(self,
                 path_="./resource/model/",
                 extension_=".model"):
        self.path = path_
        self.extension = extension_
        self._wakachi = Wakachi()

    @staticmethod
    def __create_filepath_list(read_dir_path_: str, extension_: str, is_add_test=False) -> list:
        """ファイルリストを生成する"""

        def judgment_remove_test_file(path_):
            """テストケースのファイルを除外するかどうかを判断する関数"""
            if is_add_test is True:
                return True
            else:
                return path_[:4] != "test"

        return [read_dir_path_ + path
                for path in os.listdir(read_dir_path_)
                if path[-len(extension_):] == extension_
                and judgment_remove_test_file(path)]

    def create_models_word_vector(self):
        """単語ベクトルのモデルを生成する"""
        wakachi_files = self.__create_filepath_list(self._wakachi.path, self._wakachi.simple_extension)
        for file in wakachi_files:
            data = word2vec.LineSentence(file)
            model = word2vec.Word2Vec(data, size=200, window=10, hs=1, min_count=2, sg=1)
            model.save(
                self.path + file[len(self._wakachi.path):-len(self._wakachi.simple_extension)] + self.extension)


def main():
    model = Model()
    model.create_models_word_vector()


if __name__ == '__main__':
    main()
