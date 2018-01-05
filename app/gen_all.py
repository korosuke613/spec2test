import gen_wakachi
import gen_model
import gen_tfidf
import gen_imporwords
import gen_testsuite


def main():
    gen_wakachi.main()
    gen_model.main()
    gen_tfidf.main()
    gen_imporwords.main()
    gen_testsuite.main()


if __name__ == '__main__':
    main()
