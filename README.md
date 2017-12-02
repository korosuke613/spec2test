# spec2test

[![Travis](https://img.shields.io/travis/korosuke613/spec2test/master.svg?style=flat-square)](https://travis-ci.org/korosuke613/spec2test) [![Coveralls github](https://img.shields.io/coveralls/korosuke613/spec2test/master.svg?style=flat-square)](https://coveralls.io/github/korosuke613/spec2test)
 [![Codacy grade](https://img.shields.io/codacy/grade/a834a52e92cb45a294c31d32c5fd3267.svg?style=flat-square)](https://www.codacy.com/app/korosuke613613/spec2test/dashboard) [![Code Climate](https://img.shields.io/codeclimate/maintainability/korosuke613/spec2test.svg?style=flat-square)](https://codeclimate.com/github/korosuke613/spec2test)

仕様書からテストケースを生成する研究

[Doxygenドキュメント(未完成)](https://korosuke613.github.io/spec2test/)

## 概要
* 複数の仕様書の入力から、重要単語・テストケースを生成する。
* Python3系で動作するCLIツール。
* ニューラルネットワーク(RNN/LSTM)を利用する。
* Specification To Test caseの意味


## 構造

### 全体

![全体図](images/全体図.png)

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


## 定義
![クラス図](images/定義クラス図.PNG)

* *仕様書* - あるソフトウェアのある機能の仕様の集まり
* *テストスイート* - あるソフトウェアのある機能の複数のテストケース
* *学習用データ* - 機械に学習させるためのサンプルとなるデータ
* *生成対象仕様書群* - テストケースを出力したい仕様書の集まり
* *生成テストスイート群* - 生成したテストスイートの集まり

## 内部設計
![クラス図](images/Spec2testクラス図.png)
