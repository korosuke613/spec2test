from spec2test import Directory, EvaluationTestsuite

PATH_CORRECT = "./resource/testsuite/correct_testsuite/"
PATH_MODEL1 = "リファレンス有り[重み少]/u100e100p495_184/"
PATH_MODEL2 = "リファレンス無しテストケース無し/u100e100p1083_184/"
PATH_MODEL3 = "リファレンス無し/u100e100p1_487_2739/"
PATH_MODEL4 = "リファレンス無し/u100e100p3_622_521/"
PATH_MODEL = PATH_MODEL1
PATH_RESOURCE_SIMPLE = "./resource/testsuite/" + PATH_MODEL + "simple_ptb/"
PATH_RESOURCE_S2T = "./resource/testsuite/" + PATH_MODEL


def main():
    correct = Directory(path_=PATH_CORRECT)
    simple_ptb = Directory(path_=PATH_RESOURCE_SIMPLE)
    s2t = Directory(path_=PATH_RESOURCE_S2T)
    evaluation = EvaluationTestsuite(correct=correct, eval_a_=simple_ptb, eval_b_=s2t)
    evaluation.print_compares()


if __name__ == '__main__':
    main()
