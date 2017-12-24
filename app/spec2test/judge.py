

class Judge:
    max_testcase = None
    max_score = 0.0

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
        score = self._calc_word_nums()
        self.set_max_score(score, testcase)
        return score

    @classmethod
    def set_max_score(cls, score, testcase):
        if cls.max_score > score:
            return
        cls.max_score = score
        cls.max_testcase = testcase
        return

    @classmethod
    def reset_max_score(cls):
        cls.max_testcase = None
        cls.max_score = 0.0


if __name__ == '__main__':
    string = "aa koko iku"
    imporword = ["aa", "koku", "konishi", "ikuiku", "koko"]
    judge = Judge()
    score = judge.compare_testcase(imporword, string)
    print(score)
    print(judge.get_imporwords)
