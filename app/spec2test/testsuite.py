import chainer
import chainer.links as L
from chainer import serializers
import numpy as np

from .iomanager import IOManager
from .model import Model
from .tfidf import Tfidf
from .wakachi import Wakachi
from .imporwords import Imporwords
from .trainptb import RNNForLM


class TestSuite(IOManager):
    def __init__(self,
                 input_path="./resource/file/",
                 output_path="./resource/testcase/",
                 model_=None,
                 tfidf_=None,
                 imporwords_=None,
                 learn_result_=None,
                 units_=None):
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
        self.units = units_
        self.learn_model = None
        self.learn_result = learn_result_
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
        for c, i in self.vocab.items():
            self.vocab_i[i] = c

    def load_model(self):
        self.learn_model = L.Classifier(RNNForLM(len(self.vocab, self.units)))
        serializers.load_npz(self.learn_result, self.learn_model)
        self.learn_model.predictor.reset_state()

    def generate(self):
        pass
