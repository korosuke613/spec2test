
# spec2test

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


## 使用方法
Spec2TestはPython3.6系で動作します。また、いくつかのライブラリに依存しています。
必要なライブラリは`requirements.txt`に書いています。

また、Spec2TestではMeCabを使用しているため、MeCabをインストールしている必要があります。


### 簡単な環境構築方法

Dockerを用いることで簡単に開発環境の構築をすることができます。
`build/`ディレクトリ内で`docker build .`をすることで、Spec2Testが動作するDockerイメージを用意できます。

もしくは、`docker pull korosuke613/spec2test`をすることで、[Docker Hub](https://hub.docker.com/r/korosuke613/spec2test/)にある、最新のDockerイメージを入手する方法もあります。


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

![全体図](https://github.com/korosuke613/spec2test/blob/master/images/%E5%85%A8%E4%BD%93%E5%9B%B3.png?raw=true)


