import os


def create_file_list(dir_path):
    """ファイルリストを生成する"""

    def is_test_file(path_):
        """テストケースのファイルを除外するかどうかを判断する関数"""
        return path_[:4] == "test"

    return [path
            for path in os.listdir(dir_path)
            if path[-len(".meishi.wakachi"):] == ".meishi.wakachi"
            and is_test_file(path)]


def gen(input_path, output_path):
    test_file_list = create_file_list(input_path)
    for file in test_file_list:
        gen_simple(file, input_path, output_path)


def gen_simple(file, input_path, output_path):
    with open(input_path + file, "r", encoding="utf_8_sig") as f:
        word_list = []
        for row in f:
            word_list.extend(row.split())
        sorted_array2d = set(word_list)
        file_name = input_path + file
        with open(output_path + file + ".uniq.csv", "w", encoding="utf_8_sig") as f:
            for word in sorted_array2d:
                f.write(word + "\n")


if __name__ == "__main__":
    gen("../resource/wakachi/", "../resource/imporwords/")
