# FROM でベースとなるイメージを指定
FROM ubuntu:latest

# 作者の指定
MAINTAINER Futa HIRAKOBA

# ワークディレクトリ
WORKDIR ~/

# 更新
RUN apt update && apt -y upgrade

RUN apt install -y apt-file 
RUN apt install -y software-properties-common
RUN apt install -y wget git

# Python3のインストール
RUN add-apt-repository -y ppa:jonathonf/python-3.6
RUN apt -y update
RUN apt install -y python3.6 python3.6-dev
RUN wget https://bootstrap.pypa.io/get-pip.py
RUN python3.6 get-pip.py


# mecabのインストール
RUN apt install -y make xz-utils
RUN apt install -y mecab libmecab-dev mecab-ipadic-utf8 -y
RUN git clone --depth 1 https://github.com/neologd/mecab-ipadic-neologd.git
WORKDIR ~/mecab-ipadic-neologd
RUN yes yes | ./bin/install-mecab-ipadic-neologd -n

# リポジトリのクローン
WORKDIR ~/
RUN git clone https://github.com/korosuke613/spec2test.git ~/spec2test
WORKDIR ~/spec2test/

# Pythonライブラリのインストール
RUN apt install gcc g++
RUN pip3 install -r requirements.txt
