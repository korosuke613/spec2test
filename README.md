
# spec2test
Auther : Futa HIRAKOBA

[![Docker Automated build](https://img.shields.io/docker/automated/korosuke613/spec2test.svg?style=flat-square)](https://hub.docker.com/r/korosuke613/spec2test/) [![Travis](https://img.shields.io/travis/korosuke613/spec2test/master.svg?style=flat-square)](https://travis-ci.org/korosuke613/spec2test) [![Coveralls github](https://img.shields.io/coveralls/korosuke613/spec2test/master.svg?style=flat-square)](https://coveralls.io/github/korosuke613/spec2test)
 [![Codacy grade](https://img.shields.io/codacy/grade/a834a52e92cb45a294c31d32c5fd3267.svg?style=flat-square)](https://www.codacy.com/app/korosuke613613/spec2test/dashboard) [![Code Climate](https://img.shields.io/codeclimate/maintainability/korosuke613/spec2test.svg?style=flat-square)](https://codeclimate.com/github/korosuke613/spec2test)

仕様書からテストケースを生成する研究

[Doxygenドキュメント(未完成)](./docs/annotated.html)

## 概要

* Spec2Testは日本語で記述された仕様書から、機械学習を用いて、日本語のテストケースを自動的に生成する、
* ただし、まだまともな文章は生成できません（**ここ重要**）。
* システムテストにおける、機能テストが対象です。
* **Spec**ification **To** **Test** の略
* Python3.6系で動作します。
* Spec2TestはOpenSourceSoftwareです。最新のソースコードは[GitHub](https://github.com/korosuke613/spec2test)にあります。

## 環境構築
Spec2TestはPython3.6系で動作します。また、いくつかのライブラリに依存しています。
必要なライブラリは`requirements.txt`に書いています。

また、Spec2TestではMeCabを使用しているため、MeCabをインストールしている必要があります。

ソースコードのドキュメントは[コチラ](./docs/index.html)

### 簡単な方法
Dockerを用いることで簡単に開発環境の構築をすることができます。
`build/`ディレクトリ内で`docker build .`をすることで、Spec2Testが動作するDockerイメージを用意できます。

もしくは、`docker pull korosuke613/spec2test`をすることで、[Docker Hub](https://hub.docker.com/r/korosuke613/spec2test/)にある、最新のDockerイメージを入手する方法もあります。

## 使用方法

### 準備
Spec2Testを使用する前にいくつかの準備が必要です。以下の作業を行なってください。
1. Spec2Testを使う前に、`/app/resource/txt`内に、生成対象仕様書をテキスト形式にしたものを複数個いれてください。
2. `1.`で入れた、テキスト形式の生成対象仕様書群を分かち書きしてください。`/app/gen_wakachi.py`を実行することで、`/app/resource/wakachi`内に分かち書きした仕様書が生成されます。 
3. `2.`で生成した分かち書きした仕様書群の、 **70%** のテキストを`/app/resource/train.txt`として保存し、残りの **20%** のテキストを`/app/resource/valid.txt`として保存し、余ったの **10%** のテキストを`/app/resource/test.txt`として保存してください。
4. `/app/resource`に移動し、以下のコマンドを実行してください。

```bash
$ ../spec2test/trainptb.py -u 100 -e 100
```

このコマンドを実行することで、`3.`で作成したファイルを基に、LSTM文章学習を行ないます。
`-u`がユニット数、`-e`がエポック数を表します。
学習終了後に、`/app/resource/result`というディレクトリが生成されます。そのディレクトリ内の使いたい学習ファイル(例 `model_iter_e100_u100_3112`)を、自分で選択し、`/app/resource`に移動してください。

### テストケース生成をする。
テストケース生成を行ないます。以下のコマンドを実行してください。


## ディレクトリ構成

```
spec2test
├── app  # Spec2Test本体
│   ├── gen_all.py  # 一通りの処理をするスクリプト
│   ├── gen_imporwords.py  # 重要単語リストを生成するスクリプト
│   ├── gen_testsuite_evaluation.py  # テストスイートの評価用スクリプト
│   ├── gen_testsuite.py  # テストスイートを生成するスクリプト
│   ├── gen_tfidf.py  # TF-IDF付き単語リストを生成するスクリプト
│   ├── gen_vector.py  # 単語ベクトルを生成するスクリプト
│   ├── gen_wakachi.py  # 分かち書きを行うスクリプト
│   ├── spec2test  # Spec2Testライブラリ
│   │   ├── directory.py  # ディレクトリに関するクラス
│   │   ├── evaluation.py  # 評価に関するクラス
│   │   ├── file.py  # ファイルに関するクラス
│   │   ├── imporwords.py  # 重要単語リストに関するクラス
│   │   ├── iomanager.py  # ファイル生成関係の抽象クラス
│   │   ├── testsuite.py  # テストスイートに関するクラス
│   │   ├── tfidf.py  # TF-IDF付き単語リストに関するクラス
│   │   ├── trainptb.py  # LSTMに関するスクリプト
│   │   ├── vector.py  # 単語ベクトルに関するクラス
│   │   └── wakachi.py  # 分かち書きに関するクラス
│   ├── resource/  # 入出力ファイルを保管するディレクトリ
│   │   ├── imporwords/  # 重要単語リストの保存ディレクトリ
│   │   ├── testsuite/  # テストスイートの保存ディレクトリ
│   │   ├── txt/  # 生成対象仕様書群の保存ディレクトリ
│   │   ├── tfidf/  # TF-IDF付き単語リストの保存ディレクトリ
│   │   ├── vector/  # 単語ベクトルの保存ディレクトリ
│   │   └── wakachi/  # 分かち書き仕様書の保存ディレクトリ
│   └── test/  # Spec2Testライブラリのテストコード
├── build/  # Docker build用のディレクトリ
│   └── Dockerfile  # Dockerfile
├── docs/ # Doxygenによって生成したドキュメント
├── Doxyfile  # Doxygenの設定
├── images/  # Spec2Testに関する画像
├── LICENSE  # ライセンス
├── py_filter  # DoxygenのPython向け設定
├── pytest.ini  # pytestの設定
├── README.md  # このファイル
└── requirements.txt  # 必要なPythonライブラリ
```

## 構造

### 全体

![全体図](./images/struct_diagram.png)


