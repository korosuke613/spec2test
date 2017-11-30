from spec2test import Imporwords, uniqword


def main():
    imporwords = Imporwords(imporwords_dir_path_="./resource/imporwords/")
    imporwords.generate_imporwords(threshold_tfidf=0.0, threshold_model=0.0)
    uniqword.gen("./resource/wakachi/", "./resource/imporwords/")


if __name__ == '__main__':
    main()
