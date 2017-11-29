"""TFIDF計算器"""
import os
import csv
from sklearn.feature_extraction.text import TfidfVectorizer
from .AbcFile import AbcBase


class Tfidf(AbcBase):
    """TFIDFに関するクラス"""
    def __init__(self):
        super().__init__()
        self.set_path("./resource/", "wakachi/", "tfidf/")
        self.set_extension(".meishi.wakachi", ".tfidf")

    def __create_wakachi_list(self, is_add_test: bool = False) -> list:
        """ファイルリストを生成する"""

        def judgment_remove_test_file(path_):
            """テストケースのファイルを除外するかどうかを判断する関数"""
            if is_add_test is True:
                return True
            else:
                return path_[:4] != "test"

        return [self.input_dir_path + path
                for path in os.listdir(self.input_dir_path)
                if path[-len(self.input_extension):] == self.input_extension
                and judgment_remove_test_file(path)]

    def __create_csv(self, file_path, array2d):
        """CSVにTFIDF上位の単語を記録する"""
        file_name = \
            file_path[len(self.input_dir_path):-len(self.input_extension)] + self.output_extension
        file_path = self.output_dir_path + file_name
        with open(file_path, "w", encoding="utf_8_sig") as f:
            writer = csv.writer(f, lineterminator='\n')
            writer.writerows(array2d)

    def generate_tfidf(self, is_save=True):
        """TF-IDFを計算する"""
        wakachi_files = self.__create_wakachi_list()
        # ベクタライザーの作成
        tfidf_vectorizer = TfidfVectorizer(input='filename', max_df=0.5, min_df=1, max_features=3000, norm='l2')
        tfidf = tfidf_vectorizer.fit_transform(wakachi_files)
        feature_names = tfidf_vectorizer.get_feature_names()
        for num_key in range(len(wakachi_files)):  # 1ファイルずつTF-IDFを出力
            tfidf_obj = [(feature_names[i], x) for (i, x) in enumerate(tfidf.toarray()[num_key]) if x > 0.0]
            # TF-IDFの高い順にソートし、リストに格納
            csv_list = [[k, v] for k, v in sorted(tfidf_obj, key=lambda x: x[1], reverse=True)]
            if is_save is True:  # CSV保存する場合
                self.__create_csv(wakachi_files[num_key], csv_list)
            else:  # CSV保存しない場合
                print(wakachi_files[num_key])
                print(csv_list)


def main():
    """使用例"""
    tfidf = Tfidf()
    tfidf.generate_tfidf()


if __name__ == "__main__":
    main()
