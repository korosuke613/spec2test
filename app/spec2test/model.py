"""単語ベクトル生成器"""
from gensim.models import word2vec
from .abcbase import AbcBase


class Model(AbcBase):
    """モデルに関するクラス"""
    def __init__(self,
                 input_path="./resource/wakachi/",
                 output_path="./resource/model/"):
        super().__init__(input_path, output_path, ".meishi.wakachi", ".model")

    def create_models_word_vector(self):
        """単語ベクトルのモデルを生成する"""
        wakachi_files = [file for file in self.input.file_dict.values()]
        for file in wakachi_files:
            data = word2vec.LineSentence(self.input.path + file.full_name)
            model = word2vec.Word2Vec(data, size=200, window=10, hs=1, min_count=2, sg=1)
            model.save(self.output.path + file.name + self.output.default_extension)


def main():
    model = Model()
    model.create_models_word_vector()


if __name__ == '__main__':
    main()
