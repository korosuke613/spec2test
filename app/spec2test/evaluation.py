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

    def compare(self):
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

    def unique_word_lists_generator(self)-> Iterator[Tuple[set, set, set]]:
        def get_unique_word_list(path_, column_num=1):
            unique_word = UniqueWord(path_)
            unique_word.extract_word(column_num)
            return unique_word.word_list

        generator = self.same_file_generator()
        for name, eval_a, eval_b in generator:
            correct = self.get_collect_file_path(name)
            correct = get_unique_word_list(correct, column_num=0)
            eval_a = get_unique_word_list(eval_a)
            eval_b = get_unique_word_list(eval_b)
            yield correct, eval_a, eval_b

    def get_collect_file_path(self, name):
        correct = self.correct.file_dict[name + self.correct.default_extension]
        return self.correct.path + correct.full_name

    def compare(self):
        pass


class UniqueWord:
    def __init__(self,
                 path):
        self.word_list = self.file = None
        self.open_file(path)

    def open_file(self, path_):
        self.file = pd.read_csv(path_, encoding="utf-8-sig")

    def extract_word(self, column_num=0):
        word_list = []
        for row in self.file.iloc[:, column_num]:
            word_list.extend(row.split())
        self.word_list = set(word_list)


def main():
    eval_a = Directory("./", ".txt")
    eval_b = Directory("./", ".txt")
    evaluation = Evaluation(eval_a, eval_b)
    print(evaluation)
    evaluation.compare()


if __name__ == '__main__':
    main()
