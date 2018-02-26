import pandas as pd
from typing import Iterator, Tuple

from directory import Directory


class Evaluation:
    def __init__(self,
                 eval_a_: Directory,
                 eval_b_: Directory,
                 is_import=True):
        self.eval_a = eval_a_
        self.eval_b = eval_b_
        if is_import:
            self.eval_a.import_files()
            self.eval_b.import_files()

    def same_file_generator(self)->Iterator[Tuple[str, str, str]]:
        files_a = self.eval_a.file_dict_generator()
        for file_a, path_a in files_a:
            file_b = self.eval_b.file_dict[file_a.full_name]
            path_b = self.eval_b.get_file_path(file_b.full_name)
            yield file_a.name, path_a, path_b

    def compare(self, correct, inspection):
        raise NotImplementedError


class EvaluationTestsuite(Evaluation):
    def __init__(self,
                 eval_a_: Directory,
                 eval_b_: Directory,
                 correct: Directory,
                 is_import=True,
                 testsuite_extension_=".testsuite.csv",
                 correct_extension_=".wakachi"):
        eval_a_.default_extension = eval_b_.default_extension = testsuite_extension_
        correct.default_extension = correct_extension_
        super().__init__(eval_a_, eval_b_, is_import)
        self.correct = correct
        if is_import:
            self.correct.import_files()

    def unique_word_lists_generator(self)-> Iterator[Tuple[str, set, set, set]]:
        def get_unique_word_list(path_, column_num=1, is_set=False):
            unique_word = UniqueWord(path_)
            unique_word.extract_word(column_num, is_set)
            return unique_word.word_list

        generator = self.same_file_generator()
        for name, eval_a, eval_b in generator:
            correct = self.get_collect_file_path(name)
            correct = get_unique_word_list(correct, column_num=0, is_set=True)
            eval_a = get_unique_word_list(eval_a, is_set=True)
            eval_b = get_unique_word_list(eval_b, is_set=True)
            yield name, correct, eval_a, eval_b

    def get_collect_file_path(self, name):
        correct = self.correct.file_dict[name + self.correct.default_extension]
        return self.correct.path + correct.full_name

    @staticmethod
    def format_score(score):
        return f'適合率 {round(score["precision"], 2)} ' \
               f'再現率 {round(score["recall"], 2)}, ' \
               f'F値 {round(score["f_mean"], 2)}'

    def print_compares(self):
        generator = self.unique_word_lists_generator()
        for name, correct, eval_a, eval_b in generator:
            result_a = self.compare(correct, eval_a)
            result_b = self.compare(correct, eval_b)
            print()
            print(f"ファイル名: {name}")
            print("simple_ptb: " + self.format_score(result_a))
            print('spec2test: ' + self.format_score(result_b))

    def compare(self, correct_words, inspection_words):
        judge = Judge(correct_words)
        for word in inspection_words:
            judge.add_word(word)
        return judge.get_score()


class Judge:
    def __init__(self,
                 true_words_):
        self.true_words = true_words_
        self.true_words_dict = {}
        self.fails_words = {}
        self.match_words = {}
        for word in true_words_:
            self.calc_words(self.true_words_dict, word)

    @staticmethod
    def calc_words(words: dict, word):
        try:
            words[word] += 1
        except KeyError:
            words[word] = 0

    def add_word(self, word):
        if word in self.true_words:
            self.calc_words(self.match_words, word)
        else:
            self.calc_words(self.fails_words, word)

    @staticmethod
    def sum_words_times(words: dict):
        result = 0
        for times in words.values():
            result += int(times)
        result += len(words)
        return result

    def get_score(self):
        match = self.sum_words_times(self.match_words)
        true = self.sum_words_times(self.true_words_dict)
        fails = self.sum_words_times(self.fails_words)
        recall = match / true
        precision = match / (match + fails)
        result = {"recall": recall,
                  "precision": precision,
                  "f_mean": 2 * recall * precision / (recall + precision)}
        return result


class UniqueWord:
    def __init__(self,
                 path):
        self.word_list = self.file = None
        self.open_file(path)

    def open_file(self, path_):
        self.file = pd.read_csv(path_, encoding="utf-8-sig")

    def extract_word(self, column_num=0, is_set=False):
        word_list = []
        for row in self.file.iloc[:, column_num]:
            word_list.extend(row.split())
        if is_set:
            self.word_list = set(word_list)
        else:
            self.word_list = word_list


def main():
    eval_a = Directory("./", ".txt")
    eval_b = Directory("./", ".txt")
    evaluation = Evaluation(eval_a, eval_b)
    print(evaluation)
    evaluation.compare()


if __name__ == '__main__':
    main()
