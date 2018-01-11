from spec2test import TestSuite


def main():
    testsuite = TestSuite(units_=100,
                          learn_result_="model_iter_u100_e100_p104_11583")
    testsuite.length = 30
    testsuite.load_vocabularies()
    testsuite.load_vector()
    generater = testsuite.load_imporwords()
    num = 20
    threshold = 0.25
    for filename, impolist in generater:
        print("create {0}".format(filename))
        impolist = [impo[0] for impo in impolist]
        testsuite_list, score_list = testsuite.create_testsuite(impolist,
                                                                threshold_=threshold,
                                                                num_=num)
        testsuite.create_csv(filename, testsuite_list, score_list)
        print("done {0}".format(filename))
        print()


if __name__ == '__main__':
    main()
