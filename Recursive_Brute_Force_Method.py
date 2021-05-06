# coding:utf-8
import numpy as np
import random
import matplotlib.pyplot as plt

# 再起による全探索関数
# i番目以降の品物から重さの和がj以下なるように選んだときの、
# 取りうる価値の総和の最大値を返す関数
def rec(i, j):
    if (i == N) :
        # 品物がもう残っていないときは、価値の和の最大値は0で確定
        res = 0
    elif (j < w[i]) :
        # 残りの容量が足りず品物iを入れられないので、入れないパターンだけ処理
        # i+1 以降の品物のみを使ったときの最大値をそのままこの場合の最大値にする
        res = rec(i + 1, j)
    else :
        # 品物iを入れるか入れないか選べるので、両方試して価値の和が大きい方を選ぶ
        res = max(rec(i + 1, j), rec(i + 1, j - w[i]) + v[i])
    return res


# シード値を設定(再現させるため)
random.seed(0)

# 商品の数
N = 10
# ナップサックの入れられる重さ
W = 300

# w[i]:i番目商品の重さ
# v[i]:i番目商品の価値
# item:ナップサックに入れた価値リスト
w = []
v = []
# w,vを1~100のランダムに設定
for i in range(N) :
    w.append(random.randint(1,100))
    v.append(random.randint(1,100))

print("w")
print(w)
print("v")
print(v)
print(rec(0, W))
