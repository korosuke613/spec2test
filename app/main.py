from spec2test import TestSuite


def main():
    testsuite = TestSuite(units_=10,
                          learn_result_="model_iter_72306")
    testsuite.load_vocabularies()
    testsuite.load_model()
    generater = testsuite.load_imporwords()
    for filename, impolist in generater:
        impolist = [impo[0] for impo in impolist]
        testsuite_list = testsuite.create_testsuite(impolist)
        testsuite.create_csv(filename, testsuite_list)


if __name__ == '__main__':
    main()
