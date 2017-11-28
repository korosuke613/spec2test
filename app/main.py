from spec2test import Imporwords, uniqword


def main():
    imporwords = Imporwords(imporwords_dir_path_="./resource/imporwords/")
    imporwords.generate_imporwords()
    uniqword.gen("./resource/wakachi/")


if __name__ == '__main__':
    main()
