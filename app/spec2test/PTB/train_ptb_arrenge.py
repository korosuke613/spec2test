"""Sample script of recurrent neural network language model.

This code is ported from following implementation written in Torch.
https://github.com/tomsercu/lstm

"""
import argparse
import math
import sys
import time

import numpy as np
import six
import six.moves.cPickle as pickle

import chainer
from chainer import cuda
import chainer.functions as F
from chainer import optimizers


parser = argparse.ArgumentParser()
parser.add_argument('model',
                    help='Trained model') #パラメータ modelを追加(必須)
parser.add_argument('--gpu', '-g', default=-1, type=int,
                    help='GPU ID (negative value indicates CPU)')
args = parser.parse_args()
mod = cuda if args.gpu >= 0 else np

n_units = 650  # number of units per layer
batchsize = 20   # minibatch size
bprop_len = 35   # length of truncated BPTT
grad_clip = 5    # gradient norm threshold to clip

# Prepare dataset (preliminary download dataset by ./download.py)
vocab = {}
inv_vocab={} #逆引き辞書


def load_data(filename):
    global vocab, n_vocab
    words = open(filename).read().replace('\n', '').strip().split()
    dataset = np.ndarray((len(words),), dtype=np.int32)
    for i, word in enumerate(words):
        if word not in vocab:
            vocab[word] = len(vocab)
            inv_vocab[len(vocab)-1]=word
        dataset[i] = vocab[word]
    return dataset

train_data = load_data('train.txt')
valid_data = load_data('valid.txt')
test_data = load_data('test.txt')
print('#vocab =', len(vocab))

whole_len = train_data.shape[0]
jump = whole_len // batchsize
print("jump =",jump)

if args.gpu >= 0:
    cuda.init(args.gpu)

# Prepare RNNLM model
model = pickle.load(open(args.model,'rb')) #モデルをロード


def forward_one_step(x_data, y_data, state, train=True):
    if args.gpu >= 0:
        x_data = cuda.to_gpu(x_data)
    x = chainer.Variable(x_data, volatile=not train)
    h0 = model.embed(x)
    h1_in = model.l1_x(F.dropout(h0, train=train)) + model.l1_h(state['h1'])
    c1, h1 = F.lstm(state['c1'], h1_in)
    h2_in = model.l2_x(F.dropout(h1, train=train)) + model.l2_h(state['h2'])
    c2, h2 = F.lstm(state['c2'], h2_in)
    y = model.l3(F.dropout(h2, train=train))
    state = {'c1': c1, 'h1': h1, 'c2': c2, 'h2': h2}
    return state, F.softmax(y) #ここを改造


def make_initial_state(batchsize=batchsize, train=True):
    return {name: chainer.Variable(mod.zeros((batchsize, n_units),
                                             dtype=np.float32),
                                   volatile=not train)
            for name in ('c1', 'h1', 'c2', 'h2')}


# Evaluation routine


def evaluate(dataset):
    sum_log_perp = mod.zeros(())
    state = make_initial_state(batchsize=1, train=False)
    data = dataset[101:] #適当な単語を選ぶ
    rand = np.random.uniform(0.0, 1.0,dataset.size)
    for i in six.moves.range(dataset.size - 1): #ループの数は適当なのでとりあえずこのまま
        x_batch = data[0:1] #最初の単語だけを渡す
        print(inv_vocab[x_batch[0]]), #逆引き辞書を使って単語を表示
        state, predict = forward_one_step(x_batch, x_batch, state, train=False)
        score = cuda.to_cpu(predict)
        top_k=1
        prediction = zip(score.data[0].get().tolist(), vocab)
        prediction.sort(cmp=lambda x, y: cmp(x[0], y[0]), reverse=True)
        m = rand[i] #乱数
        total = 0.0
        for rank, (score, name) in enumerate(prediction, start=1):
            data[0] = vocab[name] #最初の単語を推定した単語に更新する
            total += score
            if total>m : #推定された単語の確率にしたがって単語を選ぶ
                break
    return math.exp(cuda.to_cpu(sum_log_perp) / (dataset.size - 1))


# Evaluate on test dataset
test_perp = evaluate(train_data)