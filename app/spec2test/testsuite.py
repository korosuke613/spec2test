import chainer
import numpy as np

from .iomanager import IOManager
from .model import Model
from .tfidf import Tfidf
from .imporwords import Imporwords


class TestSuite(IOManager):
    def __init__(self,
                 output_path="./resource/testcase/",
                 model_=None,
                 tfidf_=None,
                 imporwords_=None):
        if model_ is None:
            model_ = Model()
        if tfidf_ is None:
            tfidf_ = Tfidf()
        if imporwords_ is None:
            imporwords_ = Imporwords()
        super().__init__(None, output_path, None, ".testsuite.csv")
        self.__model = model_
        self.__tfidf = tfidf_
        self.__imporwords = imporwords_
        self.vocab = {}
        self.vocab_n = 0
        self.vocab_i = {}
        chainer.config.train = False  # 学習中ではないことを明示

    def load_vocabulary(self, filename):
        words = open(filename, encoding="utf-8").read().replace('\n', ' ').strip().split()
        dataset = np.ndarray((len(words),), dtype=np.int32)
        for i, word in enumerate(words):
            if word not in self.vocab:
                self.vocab[word] = len(self.vocab)  # 単語をIDに変換
            dataset[i] = self.vocab[word]  # datasetに単語IDを追加
        return dataset

    def generate(self):
        pass
