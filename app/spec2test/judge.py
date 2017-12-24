

class Judge:
    """テストケースの評価に関するクラス"""
    ## 一番評価の高いテストケース
    max_testcase = None
    ## 一番評価の高いテストケースのスコア
    max_score = 0.0

    def __init__(self):
        """初期化"""
        ## テストケースに含まれている重要単語の数
        self.point = 0
        ## テストケースに含まれている重要単語
        self.imporwords = []
        ## 対象のテストケース
        self.testcase = None

    def _calc_word_nums(self):
        """ポイントをテストケースの単語数で割った値を計算する
        @return ポイントをテストケースの単語数で割った値
        """
        testcase_length = len(self.testcase.split(" "))
        return self.point / testcase_length

    def _compare_word(self, imporword: str):
        """テストケースに重要単語があればポイントを増加
        @param imporword: 重要単語
        """
        if imporword not in self.testcase:
            return
        self.imporwords.append(imporword)
        self.point += 1

    def compare_testcase(self, imporwords: list, testcase: str=None)-> str:
        """テストケースを評価する。
        @return テストケースに重要単語がどれくらい含まれているかのスコア
        @param imporwords: 重要単語リスト
        @param testcase: テストケース
        """
        self.point = 0
        self.testcase = testcase
        for word in imporwords:
            self._compare_word(word)
        score = self._calc_word_nums()
        self.set_max_score(score, testcase)
        return score

    @classmethod
    def set_max_score(cls, score, testcase):
        """最大評価のテストケースを保存する。
        @param score: テストケースの評価
        @param testcase: テストケース
        """
        if cls.max_score > score:
            return
        cls.max_testcase = testcase
        cls.max_score = score
        return

    @classmethod
    def reset(cls):
        """クラスの最大評価テストケースをリセットする"""
        cls.max_testcase = None
        cls.max_score = 0.0


if __name__ == '__main__':
    string = "aa koko iku"
    imporword = ["aa", "koku", "konishi", "ikuiku", "koko"]
    judge = Judge()
    score = judge.compare_testcase(imporword, string)
    print(score)
    print(judge.imporwords)
