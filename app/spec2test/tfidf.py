"""TFIDF計算器"""
import csv
from sklearn.feature_extraction.text import TfidfVectorizer
from .abcbase import AbcBase


class Tfidf(AbcBase):
    """TFIDFに関するクラス"""
    def __init__(self,
                 input_path="./resource/wakachi",
                 output_path="./resource/tfidf"):
        super().__init__(input_path, output_path, ".meishi.wakachi", ".tfidf")

    def __create_csv(self, file, array2d):
        """CSVにTFIDF上位の単語を記録する"""
        file_path = self.output.path + file.name + self.output.default_extension
        with open(file_path, "w", encoding="utf_8_sig") as f:
            writer = csv.writer(f, lineterminator='\n')
            writer.writerows(array2d)

    def generate_tfidf(self, is_save=True):
        """TF-IDFを計算する"""
        wakachi_files = [file for file in self.input.file_dict.values()]
        wakachi_file_list = [self.input.path + file.full_name for file in wakachi_files]
        # ベクタライザーの作成
        tfidf_vectorizer = TfidfVectorizer(input='filename', max_df=0.5, min_df=1, max_features=3000, norm='l2')
        tfidf = tfidf_vectorizer.fit_transform(wakachi_file_list)
        feature_names = tfidf_vectorizer.get_feature_names()
        for num_key, _ in enumerate(wakachi_files):  # 1ファイルずつTF-IDFを出力
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
