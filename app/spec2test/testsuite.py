import chainer
import chainer.links as L
import chainer.functions as F
import csv
from tqdm import tqdm

import six
from chainer import serializers, cuda
import numpy as np

from file import File
from iomanager import IOManager
from directory import Directory
from trainptb import RNNForLM


class TestSuite(IOManager):
    """テストスイートの生成に関するクラス"""
    def __init__(self,
                 input_path="./resource/",
                 output_path="./resource/testsuite/",
                 learn_result_=None,
                 units_=None):
        """初期化"""
        super().__init__(input_path, output_path, ".txt", ".testsuite.csv")
        self.vocab = {}
        self.vocab_n = 0
        self.vocab_i = {}
        self.units = units_
        self.learn_model = None
        self.learn_result = learn_result_
        self.length = 30
        self.imporwords = Directory(self.input.path + "imporwords/", ".imporword.csv")
        self.imporwords.import_files()
        np.random.seed(np.random.randint(1, 1000))
        chainer.config.train = False  # 学習中ではないことを明示

    def load_vocabulary(self, file: File):
        """ボキャブラリーを読み込む
        @param file: 分かち書き済の文章
        @return データセット
        """
        file_path = self.input.path + file.full_name
        words = open(file_path, encoding="utf-8-sig").read().replace('\n', ' ').strip().split()
        dataset = np.ndarray((len(words),), dtype=np.int32)
        for i, word in enumerate(words):
            if word not in self.vocab:
                self.vocab[word] = len(self.vocab)  # 単語をIDに変換
            dataset[i] = self.vocab[word]  # datasetに単語IDを追加
        return dataset

    def load_vocabularies(self):
        """複数のボキャブラリーを読み込む"""
        vocabulary_files = [self.input.file_dict["train.txt"],
                            self.input.file_dict["valid.txt"],
                            self.input.file_dict["test.txt"]
                            ]
        for file in vocabulary_files:
            self.load_vocabulary(file)
        for c, i in self.vocab.items():
            self.vocab_i[i] = c

    def load_imporwords(self):
        """重要単語を読み込む
        @return 拡張子を除く重要単語ファイル名と重要単語リストを返すジェネレータ
        """
        files = self.imporwords.get_file_list()
        for file in files:
            imporword = self.imporwords.path + file.full_name
            with open(imporword, "r", encoding="utf_8_sig") as f:
                csv_file = csv.reader(f)
                imporword_list = [row for row in csv_file]
            yield file.name, imporword_list

    def create_csv(self, filename, testsuite: list, scores: float):
        """テストスイートをCSV形式で保存する
        @param filename: 保存ファイル名
        @param testsuite: テストケースのリスト
        @param scores: スコアのリスト
        """
        filename += self.output.default_extension
        filepath = self.output.path + filename
        with open(filepath, "w", encoding="utf-8-sig") as file:
            writer = csv.writer(file, lineterminator='\n')
            for testcase, score in zip(testsuite, scores):
                row = [score, testcase]
                writer.writerow(row)

    def create_testsuite(self, imporword_list: list, threshold_: float=99.0, num_: int=10, is_prime=True):
        """テストスイートを生成する
        @param imporword_list: 重要単語のリスト
        @param threshold_: スコアの閾値
        @param num_: 一つのテストケースを生成する際に繰り返す回数
        @return テストスイートとそのスコア
        """
        def decide_testcase():
            testcase_ = None
            score_ = 0.0
            Judge.reset()
            for _ in range(num_):
                if not is_prime:
                    testcase_ = self.gen_testcase()
                else:
                    testcase_ = self.gen_testcase(imporword)
                judge = Judge()
                score_ = judge.compare_testcase(imporword_list, testcase_)
                if score_ >= threshold_:
                    break
                np.random.seed(np.random.randint(1, 1000))
                testcase_ = judge.max_testcase
                score_ = judge.max_score
            return testcase_, score_

        testsuite = []
        scores = []
        for imporword in tqdm(imporword_list):
            try:
                testcase, score = decide_testcase()
            except ValueError:
                testcase = imporword + " is not vocabulary."
                score = 0
            testsuite.append(testcase)
            scores.append(score)
        return testsuite, scores

    def load_vector(self):
        """単語ベクトルを読み込む"""
        self.learn_model = L.Classifier(RNNForLM(len(self.vocab), self.units))
        serializers.load_npz(self.input.path+self.learn_result, self.learn_model)
        self.learn_model.predictor.reset_state()

    def gen_testcase(self, prime_text: str=None)-> str:
        """テストケースを生成する
        @param prime_text: 文頭の単語
        @return テストケース
        """
        def set_prime_text():
            nonlocal prime_text
            if isinstance(prime_text, six.binary_type):
                prime_text = prime_text.decode('utf-8-sig')
            if prime_text in self.vocab:
                prev_word = chainer.Variable(np.array([self.vocab[prime_text]], np.int32))
                return prev_word
            else:
                raise ValueError

        def set_randome_prime():
            import random
            key = random.randint(0, len(self.vocab)-1)
            vocab_ = list(self.vocab.values())
            prev_word_random = chainer.Variable(np.array([vocab_[key]], np.int32))
            return prev_word_random

        if prime_text is None:
            prime_text = ""
            prev_word = set_randome_prime()
        else:
            prev_word = set_prime_text()
        F.softmax(self.learn_model.predictor(prev_word))
        testcase = prime_text + " "
        for _ in six.moves.range(self.length):
            prob = F.softmax(self.learn_model.predictor(prev_word))
            if 1 > 0:
                probability = cuda.to_cpu(prob.data)[0].astype(np.float64)
                probability /= np.sum(probability)
                index = np.random.choice(range(len(probability)), p=probability)
            else:
                index = np.argmax(cuda.to_cpu(prob.data))

            if self.vocab_i[index] == '<eos>':
                testcase += '.'
            else:
                testcase += self.vocab_i[index] + " "
            prev_word = chainer.Variable(np.array([index], dtype=np.int32))
        return testcase

    def generate(self, prime_text=None):
        self.load_vocabularies()
        self.load_vector()
        try:
            testcase = self.gen_testcase(prime_text)
            print(testcase)
        except ValueError:
            print(prime_text + " is not vocabulary.")


class Judge:
    """テストケースの評価に関するクラス"""
    ## 一番評価の高いテストケース
    max_testcase = None
    ## 一番評価の高いテストケースのスコア
    max_score = 0.0

    def __init__(self):
        """初期化"""
        ## テストケースに含まれている重要単語の数
        self.point = 0
        ## テストケースに含まれている重要単語
        self.imporwords = []
        ## 対象のテストケース
        self.testcase = None

    def _calc_word_nums(self):
        """ポイントをテストケースの単語数で割った値を計算する
        @return ポイントをテストケースの単語数で割った値
        """
        testcase_length = len(self.testcase.split(" "))
        return self.point / testcase_length

    def _compare_word(self, imporword: str):
        """テストケースに重要単語があればポイントを増加
        @param imporword: 重要単語
        """
        if imporword not in self.testcase:
            return
        self.imporwords.append(imporword)
        self.point += 1

    def compare_testcase(self, imporwords: list, testcase: str=None)-> str:
        """テストケースを評価する。
        @return テストケースに重要単語がどれくらい含まれているかのスコア
        @param imporwords: 重要単語リスト
        @param testcase: テストケース
        """
        self.point = 0
        self.testcase = testcase
        for word in imporwords:
            self._compare_word(word)
        score = self._calc_word_nums()
        self.set_max_score(score, testcase)
        return score

    @classmethod
    def set_max_score(cls, score: float, testcase: str):
        """最大評価のテストケースを保存する。
        @param score: テストケースの評価
        @param testcase: テストケース
        """
        if cls.max_score > score:
            return
        cls.max_testcase = testcase
        cls.max_score = score
        return

    @classmethod
    def reset(cls):
        """クラスの最大評価テストケースをリセットする"""
        cls.max_testcase = None
        cls.max_score = 0.0


def main():
    string = "aa koko iku"
    imporword = ["aa", "koku", "konishi", "ikuiku", "koko"]
    judge = Judge()
    score = judge.compare_testcase(imporword, string)
    print(score)
    print(judge.imporwords)


if __name__ == '__main__':
    main()
