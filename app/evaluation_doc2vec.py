import MeCab
from gensim.models.doc2vec import TaggedDocument
from gensim.models import Doc2Vec
import pandas as pd
from collections import OrderedDict


def main(correct1,
         spec2test1,
         simple_ptb1,
         correct2,
         spec2test2,
         simple_ptb2,
         correct3,
         spec2test3,
         simple_ptb3
         ):

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

    documents = [open(correct1, 'r').read(),
                 open(spec2test1, 'r').read(),
                 open(simple_ptb1, 'r').read(),
                 open(correct2, 'r').read(),
                 open(spec2test2, 'r').read(),
                 open(simple_ptb2, 'r').read(),
                 open(correct2, 'r').read(),
                 open(spec2test2, 'r').read(),
                 open(simple_ptb2, 'r').read(),
                 ]

    train_corpus = []
    for i, document in enumerate(documents):
        train_corpus.append(TaggedDocument(words=words(document), tags=['doc' + str(i + 1)]))

    # min_count=1:最低1回出現した単語を学習に使用
    # dm=0: 学習モデル=DBOW
    model = Doc2Vec(documents=train_corpus, min_count=1, dm=0)

    tags = OrderedDict()  # 辞書の繰り返し時による順番を保つ
    tag_list = (('doc1', "真のテストケース1"), ('doc2', "spec2test1"), ('doc3', "simple1  "),
                ('doc4', "真のテストケース2"), ('doc5', "spec2test2"), ('doc6', "simple2  "),
                ('doc7', "真のテストケース3"), ('doc8', "spec2test3"), ('doc9', "simple3  "))
    dic = OrderedDict(tag_list)
    tags.update(dic)

    for k, v in tags.items():
        print("[" + v + "]")
        for items in model.docvecs.most_similar(k):
            print("\t" + tags[items[0]] + " : " + str(items[1]))


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
             "./resource/testsuite/" + url + "/simple_ptb/spec_forcus.testsuite.csv",
             "./resource/testsuite/correct_testsuite/spec_kaiten.wakachi",
             "./resource/testsuite/" + url + "/spec_kaiten.testsuite.csv",
             "./resource/testsuite/" + url + "/simple_ptb/spec_kaiten.testsuite.csv",
             "./resource/testsuite/correct_testsuite/spec_kaiten.wakachi",
             "./resource/testsuite/" + url + "/spec_kaiten.testsuite.csv",
             "./resource/testsuite/" + url + "/simple_ptb/spec_kaiten.testsuite.csv"
             )