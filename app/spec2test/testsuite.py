import chainer
import numpy as np

from .iomanager import IOManager
from .model import Model
from .tfidf import Tfidf
from .wakachi import Wakachi
from .imporwords import Imporwords


class TestSuite(IOManager):
    def __init__(self,
                 input_path="./resource/file/",
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
        super().__init__(input_path, output_path, ".txt", ".testsuite.csv")
        self.__model = model_
        self.__tfidf = tfidf_
        self.__imporwords = imporwords_
        self.vocab = {}
        self.vocab_n = 0
        self.vocab_i = {}
        chainer.config.train = False  # 学習中ではないことを明示

    def load_vocabulary(self, file):
        wakachi = Wakachi(self.input.path, self.output.path)
        wakachi.generate(file)
        file_path = self.input.path + file.name + wakachi.output.default_extension
        words = open(file_path, encoding="utf-8").read().replace('\n', ' ').strip().split()
        dataset = np.ndarray((len(words),), dtype=np.int32)
        for i, word in enumerate(words):
            if word not in self.vocab:
                self.vocab[word] = len(self.vocab)  # 単語をIDに変換
            dataset[i] = self.vocab[word]  # datasetに単語IDを追加
        return dataset

    def load_vocabularies(self):
        vocabulary_files = [self.input.file_dict["train.txt"],
                            self.input.file_dict["valid.txt"],
                            self.input.file_dict["test.txt"]
                            ]
        for file in vocabulary_files:
            self.load_vocabulary(file)

    def generate(self):
        pass
