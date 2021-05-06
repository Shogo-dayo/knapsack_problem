# coding:utf-8
import numpy as np
import random
import matplotlib.pyplot as plt
import copy
from operator import itemgetter

import knapsack

# シード値を設定(再現させるため)
random.seed(0)

# knapsack.WeightandValue:クラスのための実データ
knapsack.WeightandValue = knapsack.make_randdata(knapsack.N)
print("knapsack.WeightandValue")
print(knapsack.WeightandValue)
optimal_solution = knapsack.rec_dp(0, knapsack.MAX_weight, knapsack.dp, knapsack.WeightandValue)
print("Optimal solution : {0}".format(optimal_solution))

# オブジェクト生成(個体をknapsack.MAX_biontだけ生成)
bionts = []
for i in range(knapsack.MAX_biont) :
    bionts.append(knapsack.Genetic_Biont(knapsack.WeightandValue, knapsack.MAX_weight))
    bionts[i].showinfo()

# 価値が最大のものを抽出する
elite = []

# generation:世代交代回数
generation = 25
for i in range(generation) :
    knapsack.somepoints_crossover(knapsack.roulette_choice(bionts), start_point=random.randint(0, knapsack.MAX_biont-1), end_point=random.randint(0, knapsack.MAX_biont-1))
    # knapsack.somepoints_crossover([knapsack.extract_elite(bionts, 1)[0], knapsack.extract_botom(bionts, 1)[0]], start_point=random.randint(0, knapsack.MAX_biont-1), end_point=random.randint(0, knapsack.MAX_biont-1))
    for j in bionts :
        # 数%で突然変異
        j.mutation(0.05)

    # print("generation:{0}".format(i+1))
    for i in range(knapsack.MAX_biont) :
        bionts[i].updateinfo()
        # bionts[i].showinfo()

    # 学習曲線をプロットするため
    elite.append(knapsack.extract_elite(bionts, knapsack.MAX_elite)[0].copy())


print("generation:{0}".format(generation))
for i in range(knapsack.MAX_biont) :
    bionts[i].updateinfo()
    bionts[i].showinfo()

print("elite")
for i in elite :
    i.updateinfo()
    i.showinfo()

# 学習曲線を表示する
print(knapsack.getLearningCurve(elite, optimal_solution))
plt.plot(range(len(elite)), knapsack.getLearningCurve(elite, optimal_solution))
plt.show()
