"""重要単語リスト生成器"""
import csv
from gensim.models import word2vec
from .tfidf import Tfidf
from .model import Model
from .wakachi_meishi import WakachiMeishi
from .iomanager import IOManager


class Imporwords(IOManager):
    """重要単語リストクラス"""

    def __init__(self,
                 output_path="./resource/imporwords/",
                 wakachi_=None,
                 tfidf_=None,
                 model_=None):
        if wakachi_ is None:
            wakachi_ = WakachiMeishi()
        if tfidf_ is None:
            tfidf_ = Tfidf()
        if model_ is None:
            model_ = Model()
        super().__init__(None, output_path, None, ".imporword.csv")
        self.__wakachi = wakachi_
        self.__model = model_
        self.__tfidf = tfidf_

    def __create_new_csv_imporword(self, extension, file_path, array2d):
        """CSVに重要単語を記録する"""
        sorted_array2d = sorted(array2d, key=lambda x: float(x[1]), reverse=True)
        file_name = \
            file_path[len(self.__tfidf.output.path):-len(self.__tfidf.output.default_extension)] + extension
        file_path = self.output.path + file_name
        with open(file_path, "w", encoding="utf_8_sig") as file:
            writer = csv.writer(file, lineterminator='\n')
            for word in sorted_array2d:
                writer.writerow(word)

    def calc_similarity(self, threshold_tfidf=0.1, threshold_model=0.11):
        """単語の類似度を計算"""
        def find_csv_name(csv_files_, find_name_):
            """同じ仕様書をCSVから見つける"""
            for (i, csv_file_path_) in enumerate(csv_files_):
                if find_name_ in csv_file_path_:
                    return csv_files_[i]

        models = self.__model.output.get_file_path_list(is_add_test_=False)
        tfidfs = self.__tfidf.output.get_file_path_list(is_add_test_=False)
        tfidfs = [self.__tfidf.output.path + file.full_name for file in tfidfs]
        for model_file in models:
            model_path = self.__model.output.path + model_file.full_name
            find_name = model_path[len(self.__model.output.path):-len(".model")]
            csv_file_path = find_csv_name(tfidfs, find_name)
            with open(csv_file_path, "r", encoding="utf_8_sig") as file:
                csv_file = csv.reader(file)
                tfidf_list = [row for row in csv_file if float(row[1]) > threshold_tfidf]
            model = word2vec.Word2Vec.load(model_path)
            important_words = {}
            for tfidf_word in tfidf_list:
                try:
                    similar_words_with_score = model.most_similar(positive=[tfidf_word[0]])
                    similar_words = {word[0]: float(word[1])*float(tfidf_word[1])
                                     for word in similar_words_with_score
                                     if float(word[1]) > threshold_model}
                except KeyError:
                    continue
                important_words[tfidf_word[0]] = tfidf_word[1]
                for word, num in similar_words.items():
                    if word in important_words:
                        important_words[word] = float(important_words[word]) + float(num)
                    else:
                        important_words[word] = float(num)
            self.__create_new_csv_imporword(".imporword.csv",
                                            csv_file_path,
                                            important_words.items())

    def generate(self, threshold_tfidf=0.1, threshold_model=0.11):
        """重要単語を生成"""
        self.calc_similarity(threshold_tfidf, threshold_model)


def main():
    """使用例
    imporwords = Imporwords(imporwords_dir_path_="./resource/imporwords/")
    imporwords.generate()
    """
    pass


if __name__ == "__main__":
    main()
