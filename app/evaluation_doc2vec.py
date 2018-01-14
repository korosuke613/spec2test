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
    tag_list = (('doc1', "spec_forcus"), ('doc2', "spec2test_forcus"), ('doc3', "simple_forcus  "),
                ('doc4', "spec_kaiten"), ('doc5', "spec2test_kaiten"), ('doc6', "simple_kaiten  "),
                ('doc7', "spec_move"), ('doc8', "spec2test_move"), ('doc9', "simple_move  "))
    dic = OrderedDict(tag_list)
    tags.update(dic)

    for k, v in tags.items():
        if v != "spec_forcus" and v != "spec_kaiten" and v != "spec_move":
            continue
        print("[" + v + "]")
        for items in model.docvecs.most_similar(k):
            print("\t" + tags[items[0]] + " : " + str(round(items[1], 2)))


if __name__ == '__main__':
    url_list = ["ref_F_test_F/",
                "ref_F_test_T/",
                "ref_S_test_F/",
                "ref_S_test_T/",
                "ref_T_test_F/",
                "ref_T_test_T/"]

    for url in url_list:
        print()
        print(url)

        main("./resource/testsuite/correct_testsuite/spec_forcus.wakachi",
             "./resource/testsuite/" + url + "/spec_forcus.testsuite.csv",
             "./resource/testsuite/" + url + "/simple_ptb/spec_forcus.testsuite.csv",
             "./resource/testsuite/correct_testsuite/spec_kaiten.wakachi",
             "./resource/testsuite/" + url + "/spec_kaiten.testsuite.csv",
             "./resource/testsuite/" + url + "/simple_ptb/spec_kaiten.testsuite.csv",
             "./resource/testsuite/correct_testsuite/spec_move.wakachi",
             "./resource/testsuite/" + url + "/spec_move.testsuite.csv",
             "./resource/testsuite/" + url + "/simple_ptb/spec_move.testsuite.csv"
             )