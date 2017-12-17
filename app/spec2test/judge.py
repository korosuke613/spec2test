

class Judge:
    def __init__(self):
        self.point = 0
        self.get_imporwords = []
        self.testcase = None

    def _calc_word_nums(self):
        testcase_length = len(self.testcase.split(" "))
        return self.point / testcase_length

    def _compare_word(self, imporword: str):
        if imporword not in self.testcase:
            return
        self.get_imporwords.append(imporword)
        self.point += 1

    def compare_testcase(self, imporwords: list, testcase: str=None):
        self.point = 0
        self.testcase = testcase
        for word in imporwords:
            self._compare_word(word)
        return self._calc_word_nums()


if __name__ == '__main__':
    string = "aa koko iku"
    imporword = ["aa", "koku", "konishi", "ikuiku", "koko"]
    judge = Judge()
    score = judge.compare_testcase(imporword, string)
    print(score)
    print(judge.get_imporwords)
