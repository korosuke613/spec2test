"""重要単語リスト生成器"""
import csv
import os
import MeCab
from gensim.models import word2vec
from directory import Directory
from iomanager import IOManager
from file import File


class Imporwords(IOManager):
    """重要単語リストクラス"""

    def __init__(self,
                 output_path="./resource/imporwords/",
                 tfidf_=None,
                 model_=None):
        """初期化"""
        if tfidf_ is None:
            tfidf_ = Directory(path_="./resource/tfidf/",
                               default_extension_=".tfidf",
                               is_import_=True)
        if model_ is None:
            model_ = Directory(path_="./resource/vector/",
                               default_extension_=".vector",
                               is_import_=True)
        super().__init__(None, output_path, None, ".imporword.csv")
        self.models = {"path": model_.path, "file_list": model_.get_file_list(is_add_test_=False)}
        self.tfidfs = tfidf_.get_file_path_list(is_add_test_=False)
        self.important_words = None

    @staticmethod
    def add_subtype_to_array2d(array2d: dict):
        mecab = MeCab.Tagger()
        mecab.parse('')
        for array in array2d:
            node = mecab.parseToNode(array).next
            node = node.feature.split(",")[1]
            array2d[array] = [node, array2d[array]]
        return array2d

    def create_new_csv(self, file_name, array2d):
        """CSVに重要単語を記録する
        @param file_name: 拡張子を除いたファイル名
        @param array2d: 保存する2次元配列
        """
        sorted_array2d = sorted(array2d, key=lambda x: float(x[1][1]), reverse=True)
        file_name = file_name + self.output.default_extension
        file_path = self.output.path + file_name
        with open(file_path, "w", encoding="utf_8_sig") as file:
            writer = csv.writer(file, lineterminator='\n')
            for word in sorted_array2d:
                word = [word[0], word[1][0], word[1][1]]
                writer.writerow(word)

    def generate_imporwords(self, model_file_: File, threshold_tfidf=0.1, threshold_model=0.11):
        """重要単語リストを生成
        @param model_file_: 生成対象のモデルファイル
        @param threshold_tfidf: tfidfの閾値
        @param threshold_model: modelの閾値
        """
        def find_csv_name(csv_files_, find_name_):
            """同じ仕様書をCSVから見つける
            @param csv_files_: 入力ファイルリスト
            @param find_name_: 拡張子を除いたファイル名
            @return 見つけたCSVファイルのパス
            """
            for (i, csv_file_path_) in enumerate(csv_files_):
                if find_name_ in csv_file_path_:
                    return csv_files_[i]

        def record_score():
            """重要単語のスコアを付ける"""
            for word, num in similar_words.items():
                if word in important_words:
                    important_words[word] = float(important_words[word]) + float(num)
                else:
                    important_words[word] = float(num)

        model = word2vec.Word2Vec.load(self.models["path"] + model_file_.full_name)
        tfidf_path = find_csv_name(self.tfidfs, model_file_.name)
        with open(tfidf_path, "r", encoding="utf_8_sig") as file:
            csv_file = csv.reader(file)
            tfidf_list = [row for row in csv_file if float(row[1]) > threshold_tfidf]
        important_words = {}
        for tfidf_word in tfidf_list:
            try:
                similar_words_with_score = model.most_similar(positive=[tfidf_word[0]])
                similar_words = {word[0]: float(word[1]) * float(tfidf_word[1])
                                 for word in similar_words_with_score
                                 if float(word[1]) > threshold_model}
            except KeyError:
                continue
            important_words[tfidf_word[0]] = tfidf_word[1]
            record_score()
        return important_words

    def generate(self, threshold_tfidf=0.1, threshold_model=0.11):
        """重要単語リストの集合を生成
        @param threshold_tfidf: tfidfの閾値
        @param threshold_model: modelの閾値
        """
        for model_file in self.models["file_list"]:
            important_words = self.generate_imporwords(model_file, threshold_tfidf, threshold_model)
            important_words = self.add_subtype_to_array2d(important_words)
            self.create_new_csv(model_file.name,
                                important_words.items())


class UniqWord(IOManager):
    def __init__(self,
                 input_=None,
                 output_=None):
        if input_ is None:
            input_ = Directory(path_="../resource/wakachi/", default_extension_=".meishi.wakachi")
        if output_ is None:
            output_ = Directory(path_="../resource/imporwords/", default_extension_=".uniq.csv")
        super().__init__(input_.path, output_.path, input_.default_extension, output_.default_extension)

    def create_file_list(self, dir_path):
        """ファイルリストを生成する"""

        def is_test_file(path_):
            """テストケースのファイルを除外するかどうかを判断する関数"""
            return path_[:4] == "test"

        return [path
                for path in os.listdir(dir_path)
                if path[-len(self.input.default_extension):] == self.input.default_extension
                and is_test_file(path)]

    def generate(self):
        test_file_list = self.create_file_list(self.input.path)
        for file in test_file_list:
            self.gen_simple(file)

    def gen_simple(self, file):
        with open(self.input.path + file, "r", encoding="utf_8_sig") as input_f:
            word_list = []
            for row in input_f:
                word_list.extend(row.split())
            sorted_array2d = set(word_list)
            with open(self.output.path + file + self.output.default_extension, "w", encoding="utf_8_sig") as output_f:
                for word in sorted_array2d:
                    output_f.write(word + "\n")


def main():
    uniq = UniqWord()
    uniq.generate()


if __name__ == "__main__":
    main()
