import os
from spec2test.iomanager import IOManager
from spec2test.directory import Directory


class UniqWord(IOManager):
    def __init__(self,
                 input_=None,
                 output_=None):
        if input_ is None:
            input_ = Directory(path_="../resource/wakachi/", default_extension_=".meishi.wakachi")
        if output_ is None:
            output_ = Directory(path_="../resource/imporwords/", default_extension_=".uniq.csv")
        super().__init__(input_.path, output_.path, input_.default_extension, output_.default_extension)

    def create_file_list(self, dir_path):
        """ファイルリストを生成する"""

        def is_test_file(path_):
            """テストケースのファイルを除外するかどうかを判断する関数"""
            return path_[:4] == "test"

        return [path
                for path in os.listdir(dir_path)
                if path[-len(self.input.default_extension):] == self.input.default_extension
                and is_test_file(path)]

    def generate(self):
        test_file_list = self.create_file_list(self.input.path)
        for file in test_file_list:
            self.gen_simple(file)

    def gen_simple(self, file):
        with open(self.input.path + file, "r", encoding="utf_8_sig") as input_f:
            word_list = []
            for row in input_f:
                word_list.extend(row.split())
            sorted_array2d = set(word_list)
            with open(self.output.path + file + self.output.default_extension, "w", encoding="utf_8_sig") as output_f:
                for word in sorted_array2d:
                    output_f.write(word + "\n")


def main():
    uniq = UniqWord()
    uniq.generate()


if __name__ == "__main__":
    main()
