# coding:utf-8
import numpy as np
import random
import matplotlib.pyplot as plt

import knapsack

# シード値を設定(再現させるため)
random.seed(151)

# 商品の数
knapsack.N = 10
# ナップサックの入れられる重さ
knapsack.MAX_weight = 10

# WeightandValue[i][0]:i番目商品の重さ
# WeightandValue[i][1]:i番目商品の価値
knapsack.WeightandValue = knapsack.make_randdata(knapsack.N)
knapsack.w = []
for i in knapsack.WeightandValue :
    knapsack.w.append(i[0])

# Wの最大値
knapsack.MAX_W = sum(knapsack.w)

# メモ化テーブル。
# dp[i][j]はi番目以降の品物から重さの和がj以下なるように選んだときの価値の和の最大値を表す。
# -1なら値が未決定であることを表す
knapsack.dp = np.zeros([knapsack.N+1,knapsack.MAX_W+1])
for i in range(knapsack.N+1) :
    for j in range(knapsack.MAX_W+1) :
        knapsack.dp[i][j] = -1

print("WeightandValue")
print(knapsack.WeightandValue)
print(knapsack.rec_dp(0, knapsack.MAX_weight, knapsack.dp, knapsack.WeightandValue))
