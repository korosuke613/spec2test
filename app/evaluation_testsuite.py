from spec2test import Directory, EvaluationTestsuite

PATH_CORRECT = "./resource/testsuite/correct_testsuite/"
PATH_MODELS = ["ref_F_test_F/ref_F_test_F_u100_e100_196/",
               "ref_F_test_T/ref_F_test_T_u100_e100_196/",
               "ref_S_test_F/ref_S_test_F_u100_e100_196/",
               "ref_S_test_T/ref_S_test_T_u100_e100_2539/",
               "ref_T_test_F/ref_T_test_F_u100_e100_12420/",
               "ref_T_test_T/ref_T_test_T_u100_e100_14763/"]


def main():
    def print_eval(PATH_MODEL):
        PATH_RESOURCE_SIMPLE = "./resource/testsuite/" + PATH_MODEL + "simple_ptb/"
        PATH_RESOURCE_S2T = "./resource/testsuite/" + PATH_MODEL
        correct = Directory(path_=PATH_CORRECT)
        simple_ptb = Directory(path_=PATH_RESOURCE_SIMPLE)
        s2t = Directory(path_=PATH_RESOURCE_S2T)
        evaluation = EvaluationTestsuite(correct=correct, eval_a_=simple_ptb, eval_b_=s2t)
        evaluation.print_compares()

    for path in PATH_MODELS:
        print(path)
        print_eval(path)
        print()


if __name__ == '__main__':
    main()
