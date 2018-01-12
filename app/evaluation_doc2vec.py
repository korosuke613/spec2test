import MeCab
from gensim.models.doc2vec import TaggedDocument
from gensim.models import Doc2Vec
import pandas as pd
from collections import OrderedDict


def main(correct,
         spec2test,
         simple_ptb):

    def csv2text(path_):
        file = pd.read_csv(path_, encoding="utf-8-sig")
        return file.iloc[:, 1]

    def words(text):
        """
            文章から単語を抽出
        """
        out_words = []
        tagger = MeCab.Tagger('-Ochasen')
        tagger.parse('')
        node = tagger.parseToNode(text)

        while node:
            word_type = node.feature.split(",")[0]
            if word_type in ["名詞"]:
                out_words.append(node.surface)
            node = node.next
        return out_words

    documents = [open(correct, 'r').read(),
                 open(spec2test, 'r').read(),
                 open(simple_ptb, 'r').read()]

    train_corpus = []
    for i, document in enumerate(documents):
        train_corpus.append(TaggedDocument(words=words(document), tags=['doc' + str(i + 1)]))

    # min_count=1:最低1回出現した単語を学習に使用
    # dm=0: 学習モデル=DBOW
    model = Doc2Vec(documents=train_corpus, min_count=1, dm=0)

    tags = OrderedDict()  # 辞書の繰り返し時による順番を保つ
    tag_list = (('doc1', "真のテストケース"), ('doc2', "spec2test"), ('doc3', "simple   "))
    dic = OrderedDict(tag_list)
    tags.update(dic)

    for k, v in tags.items():
        print("[" + v + "]")
        for items in model.docvecs.most_similar(k):
            print("\t" + tags[items[0]] + " : " + str(items[1]))
        break


if __name__ == '__main__':
    url_list = ["リファレンス有り[重み少]/u100e100p495_184",
                "リファレンス無しテストケース無し/u100e100p1083_184",
                "リファレンス無し/u100e100p1_487_2739",
                "リファレンス無し/u100e100p3_622_521"]

    for url in url_list:
        print()
        print(url)

        print("spec_forcus")
        main("./resource/testsuite/correct_testsuite/spec_forcus.wakachi",
             "./resource/testsuite/" + url + "/spec_forcus.testsuite.csv",
             "./resource/testsuite/" + url + "/simple_ptb/spec_forcus.testsuite.csv")

        print("spec_kaiten")
        main("./resource/testsuite/correct_testsuite/spec_kaiten.wakachi",
             "./resource/testsuite/" + url + "/spec_kaiten.testsuite.csv",
             "./resource/testsuite/" + url + "/simple_ptb/spec_kaiten.testsuite.csv")

        print("spec_move")
        main("./resource/testsuite/correct_testsuite/spec_kaiten.wakachi",
             "./resource/testsuite/" + url + "/spec_kaiten.testsuite.csv",
             "./resource/testsuite/" + url + "/simple_ptb/spec_kaiten.testsuite.csv")
