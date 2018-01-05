from spec2test import Wakachi, WakachiMeishi


def gen_wakachi():
    wakachi = Wakachi()
    wakachi.generate_all(is_force=True)


def gen_wakachi_meishi():
    wakachi = WakachiMeishi()
    wakachi.generate_all(is_force=True)


def main():
    gen_wakachi()
    gen_wakachi_meishi()


if __name__ == '__main__':
    main()
