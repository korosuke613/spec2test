#!/usr/bin/env python3

"""分かち分け文書生成器"""
import os
import MeCab
from iomanager import IOManager
from file import File


class Wakachi(IOManager):
    """分かち書きに関するクラス"""
    def __init__(self,
                 input_path="./resource/file/",
                 output_path="./resource/wakachi/"):
        super().__init__(input_path, output_path, ".txt", ".wakachi")
        self.hinshi_list = ['名詞', '形容詞', '動詞', '記号', '助詞', '助動詞', '接続詞', '副詞', '接頭詞']
        self.hinshi_kind = set()
        self.text = None
        self.results = []
        self.dict_word = {'名詞': [], '形容詞': [], '動詞': [], '記号': [], '助詞': [], '助動詞': [], '接続詞': [],
                          '副詞': [], '接頭詞': []}
        self.stop_word = ['\\u', '。', '、', ',', '.', '0xe0', '「', '」', '(', ')', '=', "-", "*", '"']
        self.stop_subtype = []

    def generate(self, is_force: bool=False):
        """ディレクトリ内のテキストを全て分かち書きする"""
        for file in self.input.file_dict.values():
            write_path = self.output.path + file.name + self.output.default_extension
            if os.path.isfile(write_path) and is_force is False:
                continue
            self.generate_file(file, is_set_kind=True)

    def generate_file(self, file: File=None, is_set_kind: bool=False):
        """あるテキストを分かち書きする"""
        if file is None:
            raise IndexError
        self.__open_text(file)
        self.__line_split(is_set_kind)
        self.__write(file)

    def __open_text(self, file: File):
        """テキストを開く"""
        with open(self.input.path + file.full_name, 'r', encoding="utf-8") as file:
            binary_data = file.read()
            self.text = binary_data

    def token_split(self, tokens: object, is_set_kind=False)-> list:
        """トークンを解析する"""
        r = []
        while tokens:
            w = tokens.surface
            ps = tokens.feature
            hinshi = ps.split(',')[0]
            self.hinshi_kind.add(hinshi)
            if hinshi in self.hinshi_list:
                if ps.split(',')[1] in self.stop_subtype:
                    tokens = tokens.next
                    continue
                r.append(w)
                if is_set_kind is True:
                    self.dict_word[hinshi].append(w)
            tokens = tokens.next
        return r

    def __line_split(self, is_set_kind: bool=False):
        """テキストを行ごとに分ける"""
        def set_stop_word(_line):
            """ストップワードの除去"""
            for _word in self.stop_word:
                _line = _line.replace(_word, ' ')
            return _line

        self.results = []
        t = MeCab.Tagger('-Ochasen')
        lines = self.text.split("\n")
        for line in lines:
            s = set_stop_word(line)
            t.parse("")
            tokens = t.parseToNode(s)
            r = self.token_split(tokens, is_set_kind)
            rl = (" ".join(r)).strip()
            self.results.append(rl)

    def __write(self, file: File):
        """分かち書きした結果を書き込む"""
        wakachi_file = self.output.path + file.name + self.output.default_extension
        with open(wakachi_file, "w", encoding='utf-8-sig') as fp:
            fp.write("\n".join(self.results))


class WakachiMeishi(Wakachi):
    """名詞のみの分かち書きに関するクラス"""
    def __init__(self,
                 input_path="./resource/file/",
                 output_path="./resource/wakachi/"
                 ):
        super().__init__(input_path, output_path)
        self.output.default_extension = ".meishi.wakachi"
        self.hinshi_list = ['名詞']
        self.stop_subtype = ['代名詞', '非自立', '数']
        self.stop_sub_subtype = []
        self.stop_word.extend(['_', '[', ']'])


def main():
    wakachi = WakachiMeishi()
    wakachi.generate()


if __name__ == "__main__":
    main()
