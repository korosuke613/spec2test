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

    def compare(self):
        raise NotImplementedError


class EvaluationTestsuite(Evaluation):
    def __init__(self,
                 eval_a_: Directory,
                 eval_b_: Directory,
                 is_import=True,
                 extension_=".testsuite"):
        eval_a_.default_extension = extension_
        eval_b_.default_extension = extension_
        super().__init__(eval_a_, eval_b_, is_import)

    def compare(self):
        raise NotImplementedError


def main():
    eval_a = Directory("./", ".txt")
    eval_b = Directory("./", ".txt")
    evaluation = Evaluation(eval_a, eval_b)
    print(evaluation)
    evaluation.compare()


if __name__ == '__main__':
    main()
