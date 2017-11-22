import csv


def uniq_word(path):
    with open(path, "r", encoding="utf_8_sig") as f:
        word_list = []
        for row in f:
            word_list.extend(row.split())
        sorted_array2d = set(word_list)
        with open(path + "uniq.csv", "w", encoding="utf_8_sig") as f:
            for word in sorted_array2d:
                f.write(word + "\n")


if __name__ == "__main__":
    uniq_word("../resource/wakachi/test_forcus.txt.meishi.wakachi")
