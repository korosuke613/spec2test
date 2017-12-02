"""分かち分け文書生成器"""
import os
import MeCab
from .abcbase import AbcBase


class Wakachi(AbcBase):
    """分かち分けに関するクラス"""
    def __init__(self,
                 input_path="./resource/file/",
                 output_path="./reource/wakachi/"):
        super().__init__(input_path, output_path, ".txt", ".wakachi")
        self.hinshi_list = ['名詞', '形容詞', '動詞', '記号', '助詞', '助動詞', '接続詞', '副詞', '接頭詞']
        self.hinshi_kind = set()
        self.text = None
        self.results = []
        self.dict_word = {'名詞': [], '形容詞': [], '動詞': [], '記号': [], '助詞': [], '助動詞': [], '接続詞': [],
                          '副詞': [], '接頭詞': []}

    def generate_all(self, is_force=False):
        for file in self.input.file_dict.values():
            write_path = self.output.path + file.name + self.output.default_extension
            if os.path.isfile(write_path) and is_force is False:
                continue
            self.generate(file, is_set_kind=True)

    def generate(self, file, is_set_kind=False):
        self.__open_text(file)
        self.__line_split(is_set_kind)
        self.__write(file)
        print("create " + file.name + self.output.default_extension)

    def __open_text(self, file):
        with open(self.input.path + file.full_name, 'r', encoding="utf-8") as file:
            binary_data = file.read()
            self.text = binary_data

    def __token_split(self, tokens, is_set_kind=False):
        r = []
        while tokens:
            w = tokens.surface
            ps = tokens.feature
            hinshi = ps.split(',')[0]
            self.hinshi_kind.add(hinshi)
            if hinshi in self.hinshi_list:
                if len(w) < 5:
                    if ps.split(',')[1] == '数':
                        tokens = tokens.next
                        continue
                r.append(w)
                if is_set_kind is True and hinshi == '名詞':
                    self.dict_word[hinshi].append(w)
            tokens = tokens.next
        return r

    def __line_split(self, is_set_kind=False):
        def set_stop_word(_line):
            """ストップワードの除去"""
            stop_words = ['\\u', '。', '、', '.', '0xe0', '「', '」']
            for _word in stop_words:
                _line = _line.replace(_word, '')
            return _line

        self.results = []
        t = MeCab.Tagger('-Ochasen')
        lines = self.text.split("\n")
        for line in lines:
            s = set_stop_word(line)
            t.parse("")
            tokens = t.parseToNode(s)
            r = self.__token_split(tokens, is_set_kind)
            rl = (" ".join(r)).strip()
            self.results.append(rl)

    def __write(self, file):
        wakachi_file = self.output.path + file.name + self.output.default_extension
        with open(wakachi_file, "w", encoding='utf-8-sig') as fp:
            fp.write("\n".join(self.results))


def main():
    wakachi = Wakachi()
    wakachi.generate_all()


if __name__ == "__main__":
    main()
