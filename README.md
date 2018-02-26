
# spec2test

[![Docker Automated build](https://img.shields.io/docker/automated/korosuke613/spec2test.svg?style=flat-square)](https://hub.docker.com/r/korosuke613/spec2test/) [![Travis](https://img.shields.io/travis/korosuke613/spec2test/master.svg?style=flat-square)](https://travis-ci.org/korosuke613/spec2test) [![Coveralls github](https://img.shields.io/coveralls/korosuke613/spec2test/master.svg?style=flat-square)](https://coveralls.io/github/korosuke613/spec2test)
 [![Codacy grade](https://img.shields.io/codacy/grade/a834a52e92cb45a294c31d32c5fd3267.svg?style=flat-square)](https://www.codacy.com/app/korosuke613613/spec2test/dashboard) [![Code Climate](https://img.shields.io/codeclimate/maintainability/korosuke613/spec2test.svg?style=flat-square)](https://codeclimate.com/github/korosuke613/spec2test)

仕様書からテストケースを生成する研究

[Doxygenドキュメント(未完成)](./docs/annotated.html)

## 概要
* 複数の仕様書の入力から、重要単語・テストケースを生成する。
* Python3系で動作するCLIツール。
* ニューラルネットワーク(RNN/LSTM)を利用する。
* Specification To Test caseの意味


## 構造

### 全体

![全体図](https://github.com/korosuke613/spec2test/blob/master/images/%E5%85%A8%E4%BD%93%E5%9B%B3.png?raw=true)

### 文章学習部
1. 仕様書とテストケースを単語ごとに区切る
2. LSTMを用いて文章の学習をする


### 重要単語抽出部
1. 仕様書を単語ごとに区切る
2. 単語ベクトルを計算する
3. 単語の希少性を計算する
4. 重要単語を生成し、リストにまとめる


### テストケース生成部
1. 文章学習部・重要単語抽出部の結果を入力として、テストケースの生成を行う


<< 使用方法 >>

Tamiasは、ソースコードをコンパイルする必要があります。
TamiasはQt5.9で開発しているため、コンパイルはgccやclangではできません。
Qt付属のqmakeを利用してMakefileを作成し、コンパイルしてください。
もし今後Qtで開発をすることがあれば、IDEのQt Creatorを導入することをオススメします。
Qt Creatorは、ビルド、実行、デバッグ、RADを搭載しているため、開発が非常に簡単になります。

<< Qtのインストール方法 >>

Qtは、マルチプラットフォームなGUIを作るためのフレームワークです。Qt自身もマルチプラットフォームで
Windows/masOS/Linux等のOSに対応しています。
Qtのインストールは、公式サイト(https://www.qt.io/download)から取得できます。
商用版と無料版がありますが、無料版(LGPLライセンス)を落としてください。
QtをWindows環境でインストールする場合で、C++のコンパイラ(gcc、clang、Visual Studio等)を
まだインストールしていない人は別途コンパイラのインストールもお願いします。

<< ディレクトリ構成 >>

```
Tool
 ┣ readme.txt
 ┗ Tamias
     ┣ src : ソースコードを入れています(以下は、ファイルの簡単な説明をしています)
     ┃ ┣ icons : Tamiasのアイコン画像を入れたディレクトリ
     ┃ ┣ Tamias.pro                 : ビルドで使用するファイル
     ┃ ┣ config.hpp/cpp             : Tamias全体で使用する設定情報を格納する構造体
     ┃ ┣ error_reporting.hpp/cpp    : タイプミスチェックダイアログに関するクラス
     ┃ ┣ grammar.hpp/cpp            : 生成規則検証部で使用する解析表現文法を格納するクラス
     ┃ ┣ grammar_check.hpp/cpp      : 文法チェック(タイプミス/左再帰チェック)を実行するクラス
     ┃ ┣ input_string.hpp/cpp       : ユーザが指定した入力文字列を格納するクラス
     ┃ ┣ input_string_editor.hpp/cpp: 拡大した入力文字列エディタに関するクラス
     ┃ ┣ input_string_info.hpp/cpp  : 入力文字列の情報ダイアログに解するクラス
     ┃ ┣ interpreter.hpp/cpp        : インタプリタに関するクラス
     ┃ ┣ left_recursion.hpp/cpp     : 左再帰チェックを実行するクラス
     ┃ ┣ line_number_area.hpp/cpp   : 行番号を表示する部分に関するクラス
     ┃ ┣ result_table.hpp/cpp       : メモ化テーブルに関するクラス
     ┃ ┣ rule_editor.hpp/cpp        : 生成規則エディタ部に関するクラス
     ┃ ┣ rule_recognizer.hpp/cpp    : 生成規則内の非終端記号および解析表現の演算子を認識してデータ構造へ格納するクラス
     ┃ ┣ rule_separator.hpp/cpp     : 解析表現を演算子によって分割するクラス
     ┃ ┣ tamias.hpp/cpp             : Tamias全体の処理に関するクラス(最も主要なクラスです)
     ┃ ┣ test_case.hpp/cpp          : テストケースウィジェットに関するクラス
     ┃ ┣ test_types.hpp/cpp         : 検証方法に関するクラス
     ┃ ┣ tamias.ui                  : TamiasのGUI部品を設定するファイル
     ┃ ┣ left_recursion.ui          : 左再帰チェック画面のGUI部品を設定するファイル
     ┃ ┣ input_string_info.ui       : 入力文字列の情報ダイアログのGUI部品を設定するファイル
     ┃ ┣ input_string_editor.ui     : 拡大した入力文字列エディタのGUI部品を設定するファイル
     ┃ ┣ grammar_check.ui           : 文法チェック(タイプミス/左再帰チェック)のGUI部品を設定するファイル
     ┃ ┣ error_reporting.ui         : タイプミスチェックダイアログのGUI部品を設定するファイル
     ┃ ┗ images.qrc                 : Tamiasのアイコンを入れたファイル
     ┗ test : 卒業論文で使用した解析表現文法の例を入れています。
         ┣ direct_left_recursion.txt         : 直接左再帰を含む文法
         ┣ direct_left_recursion_solved.txt  : 直接左再帰を含まない文法
         ┣ indirect_left_recursion.txt       : 間接左再帰を含む文法
         ┣ indirect_left_recursion_solved.txt: 間接左再帰を含まない文法
         ┣ verification.txt                  : 生成規則の動作検証で使用した文法
         ┣ prefix_capture.txt                : Prefix Captureが発生する文法
         ┗ prefix_capture_solved.txt         : Prefix Captureが発生しない文法
```