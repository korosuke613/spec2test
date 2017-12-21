from spec2test import TestSuite


def main():
    testsuite = TestSuite(units_=100,
                          learn_result_="model_iter_u100_e100_p1_487_norefa_2739")
    testsuite.load_vocabularies()
    testsuite.load_model()
    generater = testsuite.load_imporwords()
    threshold = 0.2
    num = 50
    print("threshold={0}, num={1}".format(threshold, num))
    for filename, impolist in generater:
        impolist = [impo[0] for impo in impolist]
        testsuite_list = testsuite.create_testsuite(impolist, threshold, num)
        testsuite.create_csv(filename, testsuite_list)


if __name__ == '__main__':
    main()
