import chainer
import chainer.links as L
import chainer.functions as F
import csv

import six
from chainer import serializers, cuda
import numpy as np

from .iomanager import IOManager
from .directory import Directory
from .trainptb import RNNForLM


class TestSuite(IOManager):
    def __init__(self,
                 input_path="./resource/",
                 output_path="./resource/testsuite/",
                 learn_result_=None,
                 units_=None):
        super().__init__(input_path, output_path, ".txt", ".testsuite.csv")
        self.vocab = {}
        self.vocab_n = 0
        self.vocab_i = {}
        self.units = units_
        self.learn_model = None
        self.learn_result = learn_result_
        self.length = 50
        self.imporwords = Directory(self.input.path + "imporwords/", ".imporword.csv")
        self.imporwords.import_files()
        np.random.seed(np.random.randint(1, 1000))
        chainer.config.train = False  # 学習中ではないことを明示

    def load_vocabulary(self, file):
        file_path = self.input.path + file.full_name
        words = open(file_path, encoding="utf-8-sig").read().replace('\n', ' ').strip().split()
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

    def load_imporwords(self):
        files = self.imporwords.get_file_path_list()
        for file in files:
            imporword = self.imporwords.path + file.full_name
            with open(imporword, "r", encoding="utf_8_sig") as f:
                csv_file = csv.reader(f)
                imporword_list = [row for row in csv_file]
            yield file.name, imporword_list

    def create_csv(self, filename, testsuite):
        filename += self.output.default_extension
        filepath = self.output.path + filename
        with open(filepath, "w", encoding="utf-8-sig") as file:
            writer = csv.writer(file, lineterminator='\n')
            for testcase in testsuite:
                testcase = [testcase,]
                writer.writerow(testcase)

    def create_testsuite(self, imporword_list):
        testsuite = []
        for imporword in imporword_list:
            try:
                testcase = self.gen_testcase(imporword)
            except ValueError:
                testcase = imporword + " is not vocabulary."
            testsuite.append(testcase)
        return testsuite

    def load_model(self):
        self.learn_model = L.Classifier(RNNForLM(len(self.vocab), self.units))
        serializers.load_npz(self.input.path+self.learn_result, self.learn_model)
        self.learn_model.predictor.reset_state()

    def gen_testcase(self, prime_text):
        def set_prime_text():
            nonlocal prime_text
            if isinstance(prime_text, six.binary_type):
                prime_text = prime_text.decode('utf-8-sig')
            if prime_text in self.vocab:
                prev_word = chainer.Variable(np.array([self.vocab[prime_text]], np.int32))
                return prev_word
            else:
                raise ValueError

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
        self.load_model()
        testcase = self.gen_testcase(prime_text)
        print(testcase)
