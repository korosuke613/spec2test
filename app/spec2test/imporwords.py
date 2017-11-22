import os
from gensim.models import word2vec
import csv
from .tfidf import Tfidf
from .model import Model
from .wakachi import Wakachi


class Imporwords:
    """重要単語抽出クラス"""

    def __init__(self,
                 imporwords_dir_path_="./"):
        self.imporwords_dir_path = imporwords_dir_path_
        self._wakachi = Wakachi()
        self._model = Model()
        self._tfidf = Tfidf()

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

    def __create_new_csv_imporword(self, extension, file_path, array2d):
        """CSVに重要単語を記録する"""
        sorted_array2d = sorted(array2d, key=lambda x: float(x[1]), reverse=True)
        file_name = \
            file_path[len(self._tfidf.path):-len(self._tfidf.extension)] + extension
        file_path = self.imporwords_dir_path + file_name
        with open(file_path, "w", encoding="utf_8_sig") as f:
            writer = csv.writer(f, lineterminator='\n')
            for word in sorted_array2d:
                writer.writerow(word)

    def calc_similarity(self):
        def find_csv_name(csv_files_, find_name_):
            for (i, csv_file_path_) in enumerate(csv_files_):
                if find_name_ in csv_file_path_:
                    return csv_files_[i]

        models = self.__create_filepath_list(self._model.path, self._model.extension)
        csv_files = self.__create_filepath_list(self._tfidf.path, self._tfidf.extension)
        for model_path in models:
            find_name = model_path[len(self.imporwords_dir_path):-len(".model")]
            csv_file_path = find_csv_name(csv_files, find_name)
            with open(csv_file_path, "r", encoding="utf_8_sig") as f:
                csv_file = csv.reader(f)
                tfidf_list = [row for row in csv_file if float(row[1]) > 0.1]
            model = word2vec.Word2Vec.load(model_path)
            important_words = {}
            for tfidf_word in tfidf_list:
                try:
                    similar_words_with_score = model.most_similar(positive=[tfidf_word[0]])
                    similar_words = {word[0]: float(word[1])*float(tfidf_word[1])
                                     for word in similar_words_with_score
                                     if float(word[1]) > 0.11}
                except KeyError:
                    continue
                important_words[tfidf_word[0]] = tfidf_word[1]
                for word, num in similar_words.items():
                    if word in important_words:
                        important_words[word] = float(important_words[word]) + float(num)
                    else:
                        important_words[word] = float(num)
            self.__create_new_csv_imporword(".imporword.csv", csv_file_path, important_words.items())

    def generate_imporwords(self):
        self._wakachi.generate_all(is_simple_=True, is_force=False)
        self._model.create_models_word_vector()
        self._tfidf.generate_tfidf()
        self.calc_similarity()


def main():
    imporwords = Imporwords(imporwords_dir_path_="./resource/imporwords/")
    imporwords.generate_imporwords()


if __name__ == "__main__":
    main()
