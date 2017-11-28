"""単語ベクトル生成器"""
import os
from gensim.models import word2vec
from .wakachi import Wakachi


class Model:
    """モデルに関するクラス"""
    def __init__(self,
                 path_="./resource/model/",
                 extension_=".model"):
        self.path = path_
        self.extension = extension_
        self.__wakachi = Wakachi()

    def __create_filepath_list(self, is_add_test=False) -> list:
        """ファイルリストを生成する"""

        def judgment_remove_test_file(path_):
            """テストケースのファイルを除外するかどうかを判断する関数"""
            if is_add_test is True:
                return True
            else:
                return path_[:4] != "test"

        return [self.__wakachi.path + path
                for path in os.listdir(self.__wakachi.path)
                if path[-len(self.__wakachi.simple_extension):] == self.__wakachi.simple_extension
                and judgment_remove_test_file(path)]

    def create_models_word_vector(self):
        """単語ベクトルのモデルを生成する"""
        wakachi_files = self.__create_filepath_list()
        for file in wakachi_files:
            data = word2vec.LineSentence(file)
            model = word2vec.Word2Vec(data, size=200, window=10, hs=1, min_count=2, sg=1)
            model.save(
                self.path + file[len(self.__wakachi.path):-len(self.__wakachi.simple_extension)] + self.extension)


def main():
    model = Model()
    model.create_models_word_vector()


if __name__ == '__main__':
    main()
