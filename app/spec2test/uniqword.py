import os


def create_file_list(dir_path):
    """ファイルリストを生成する"""

    def is_test_file(path_):
        """テストケースのファイルを除外するかどうかを判断する関数"""
        return path_[:4] == "test"

    return [dir_path + path
            for path in os.listdir(dir_path)
            if path[-len(".meishi.wakachi"):] == ".meishi.wakachi"
            and is_test_file(path)]


def gen(dir_path):
    test_file_list = create_file_list(dir_path)
    for file in test_file_list:
        gen_simple(file)


def gen_simple(path):
    with open(path, "r", encoding="utf_8_sig") as f:
        word_list = []
        for row in f:
            word_list.extend(row.split())
        sorted_array2d = set(word_list)
        with open(path + ".uniq.csv", "w", encoding="utf_8_sig") as f:
            for word in sorted_array2d:
                f.write(word + "\n")


if __name__ == "__main__":
    gen("../resource/wakachi/")
