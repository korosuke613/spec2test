"""分かち分け文書生成器"""
import os
import MeCab


class Wakachi:
    """分かち分けに関するクラス"""
    def __init__(self, filename=None):
        self.hinshi_kind = set()
        self.text = None
        self.filename = filename
        self.results = []
        self.resource_path = "file/"
        self.file_extension = ".txt"
        self.path = "resource/wakachi/"
        self.dict_word = {'名詞': [], '形容詞': [], '動詞': [], '記号': [], '助詞': [], '助動詞': [], '接続詞': [],
                          '副詞': [], '接頭詞': []}
        self.simple_extension = ".meishi.wakachi"
        self.extension = ".wakachi"

    def __create_file_list(self, is_add_test: bool = False) -> list:
        """ファイルリストを生成する"""

        def judgment_remove_test_file(path_):
            """テストケースのファイルを除外するかどうかを判断する関数"""
            if is_add_test is True:
                return True
            else:
                return path_[:4] != "test"

        return [path
                for path in os.listdir(self.resource_path)
                if path[-len(self.file_extension):] == self.file_extension
                and judgment_remove_test_file(path)]

    def generate_all(self, is_simple_=False, is_force=False):
        file_list = self.__create_file_list(is_add_test=True)
        for file in file_list:
            self.filename = file
            if os.path.isfile(self.resource_path + self.filename) and is_force is False:
                continue
            self.generate(is_set_kind=True, is_simple=is_simple_)

    def generate(self, filename=None, is_set_kind=False, is_simple=False):
        if filename is None:
            filename = self.filename
        self.__open_text(filename)
        self.__line_split(is_set_kind, is_simple)
        self.__write(is_simple)
        if is_simple is True:
            print("create " + filename + self.simple_extension)
        else:
            print("create " + filename + self.extension)

    def __open_text(self, filename):
        self.filename = filename
        with open(self.resource_path + self.filename, 'r', encoding="utf-8") as file:
            binary_data = file.read()
            self.text = binary_data

    def __line_split(self, is_set_kind=False, is_simple=False):
        self.results = []
        t = MeCab.Tagger('-Ochasen')
        lines = self.text.split("\n")
        for line in lines:
            s = line
            s = s.replace('\\u', '')
            s = s.replace('。', '')
            s = s.replace('、', '')
            s = s.replace('.', ' ')
            s = s.replace('0xe0', '')
            t.parse("")
            tokens = t.parseToNode(s)
            r = []
            while tokens:
                w = tokens.surface
                ps = tokens.feature
                hinshi = ps.split(',')[0]
                self.hinshi_kind.add(hinshi)
                if is_simple is True:
                    hinshi_list = ['名詞']
                else:
                    hinshi_list = ['名詞', '形容詞', '動詞', '記号', '助詞', '助動詞', '接続詞', '副詞', '接頭詞']
                if hinshi in hinshi_list:
                    if len(w) < 5:
                        if ps.split(',')[1] == '数':
                            tokens = tokens.next
                            continue
                    r.append(w)
                    if is_set_kind is True and hinshi == '名詞':
                        self.dict_word[hinshi].append(w)
                        pass
                tokens = tokens.next

            rl = (" ".join(r)).strip()
            self.results.append(rl)

    def __write(self, is_simple=False):
        if is_simple is True:
            wakachi_file = self.path + self.filename + self.simple_extension
        else:
            wakachi_file = self.path + self.filename + self.extension
        with open(wakachi_file, "w", encoding='utf-8-sig') as fp:
            fp.write("\n".join(self.results))


def main():
    wakachi = Wakachi()
    wakachi.generate_all(is_simple_=True)


if __name__ == "__main__":
    main()
