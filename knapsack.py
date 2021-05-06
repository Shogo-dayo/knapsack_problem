# coding:utf-8
import numpy as np
import random
import matplotlib.pyplot as plt
import copy
from operator import itemgetter

def getLearningCurve(elite, scale):
    """
    概要:　リストの場所に相当する適合度を出力
    @param elite: もっともよい世代ごとの個体
    @param scale: もっとも良い個体の適合度
    @return もっともよい世代ごとの個体に対する適合度リスト
    """
    res = []
    for i in elite :
        res.append(i.value/scale)
    return res

def getNearestValue(table, num):
    """
    概要: リストからある値に最も近い値を返却する関数
    @param table: データ配列
    @param num: 対象値
    @return 対象値に最も近い値
    """

    # リスト要素と対象値の差分を計算し最小値のインデックスを取得
    idx = np.abs(np.asarray(table) - num).argmin()
    return table[idx]

def extract_elite(bionts, num_elite=0) :
    """エリート保存戦略関数
    上位num_eliteまでをエリートとして返す．
    """
    # エリート保存数がおかしければ個体数に依存
    if (num_elite<1) :
        num_elite = len(bionts)

    value_all = []
    elite = []
    for i in bionts :
        value_all.append(i.value)

    for i in range(num_elite) :
        elite.append(bionts[value_all.index(max(value_all))])
        value_all[value_all.index(max(value_all))] = -1
    return elite.copy()

def extract_botom(bionts, num_botoms=0) :
    """悪い形質を抽出
    """
    if (num_botoms<1) :
        num_botoms = len(bionts)

    value_all = []
    botom = []
    for i in bionts :
        value_all.append(i.value)

    for i in range(num_botoms) :
        botom.append(bionts[value_all.index(min(value_all))])
        value_all[value_all.index(min(value_all))] = -1
    return botom.copy()

def make_randdata(N=0, *, MIN_data=1, MAX_data=100) :
    """適当にランダムデータを生成する．
    MIN_data --- 乱数の最小値
    MAX_data --- 乱数の最大値
    N --- 遺伝子数
    """
    # 遺伝子数がおかしければデフォルトで10
    if (N<1) :
        N = 10
    # クラスのためのベクトル生成
    WeightandValue = []
    while (len(WeightandValue) < N) :
        WeightandValue.append([random.randint(MIN_data,MAX_data), random.randint(MIN_data,MAX_data)])
    return WeightandValue

def somepoints_crossover(twin_bionts, *, start_point=0, end_point=0) :
    """somepoints_crossover():一点交叉する関数
    第一引数:twin_bionts
    第二引数:start_point（要素数）
    第三引数:end_point  (要素数)
    """
    res = 0

    gene_xx = twin_bionts[0].gene
    gene_yy = twin_bionts[1].gene
    len_gene_xx = len(gene_xx)

    # 交叉点がおかしければ遺伝子の中間
    if (start_point>end_point) :
        tmp = start_point
        start_point = end_point
        end_point = tmp
    if (start_point<1 or end_point<2) :
        start_point = 0
        end_point = len_gene_xx/2-1
    # 遺伝子数が異なる場合は交叉しない
    if (len_gene_xx == len(gene_yy)) :
        start_point = int(start_point)
        end_point = int(end_point+1)
        gene_xy = []
        gene_yx = []
        gene_xy.extend(gene_yy[0:start_point].copy())
        gene_xy.extend(gene_xx[start_point:end_point].copy())
        gene_xy.extend(gene_yy[end_point:len_gene_xx].copy())

        gene_yx.extend(gene_xx[0:start_point].copy())
        gene_yx.extend(gene_yy[start_point:end_point].copy())
        gene_yx.extend(gene_xx[end_point:len_gene_xx].copy())

        # もし子がナップサックの容量を超えていなかったら交叉
        dot_xy = np.dot(gene_xy, twin_bionts[0].WeightandValue)
        dot_yx = np.dot(gene_yx, twin_bionts[0].WeightandValue)
        for i in range(len_gene_xx) :
            if (dot_xy[0] <= MAX_weight and dot_xy[1] > twin_bionts[0].value) :
                twin_bionts[0].gene[i] = gene_xy[i]
            if (dot_yx[0] <= MAX_weight and dot_yx[1] > twin_bionts[1].value) :
                twin_bionts[1].gene[i] = gene_yx[i]
        for i in twin_bionts :
            i.updateinfo()
        if (twin_bionts[0].weight == dot_xy[0] or twin_bionts[1].weight == dot_yx[0]) :
            #print("Done crossover.")
            res = 1

    return res

def roulette_choice(bionts, MIN_data=1, MAX_data=100) :
    """ルーレット選択を行う関数
    第一引数:bions
    """
    value_all = []
    # 適合度割合を求める
    for i in bionts :
        i.updateinfo()
        value_all.append(i.value)
    p_all = []
    sum_value = sum(value_all)
    for i in bionts :
        i.raito = i.value/sum_value
        p_all.append(i.raito)

    # 二対の個体をルーレット選択
    twin_bionts = []
    nearest_value = p_all[random.randint(0, len(p_all)-1)]
    for i in range(2) :
        # ルーレットを回す
        rand_raito = random.random()
        # すでに選ばれたものが出た場合は出なくなるまで回す
        while (nearest_value == getNearestValue(p_all, rand_raito)) :
            # ルーレットを回す
            rand_raito = random.random()
        # 回した値に最も近い値をリストから取る
        nearest_value = getNearestValue(p_all, rand_raito)
        nearest_index = p_all.index(nearest_value)

        # 遺伝子を選択
        twin_bionts.append(bionts[p_all.index(nearest_value)])

    return twin_bionts

# def ranking_choice() :

class Genetic_Biont :
    """遺伝的アルゴリズムのためのクラス
    WeightandValue --- [[重み, 価値], ...]
    MAX_weight --- ナップサックの重さ容量
    N --- 遺伝子数

    メソッド内関数一覧
    showinfo():オブジェクトの情報を表示
    updateinfo():スコア情報を更新
    copy():実態の深いコピー
    mutation():突然変異が発生
    """
    # コンストラクタ
    def __init__(self, WeightandValue, MAX_weight ,N=0) :
        # 遺伝子を生成
        self.gene = []
        self.weight = 0
        self.value = 0
        self.raito = 0
        self.WeightandValue = WeightandValue.copy()
        # 遺伝子数がおかしければ実データに依存
        if (N<1) :
            N = len(WeightandValue)
        for j in range(N) :
            self.gene.append(random.randint(0,1))
            if (self.gene[j]==1) :
                # 入れる商品の重さがナップサックに入るなら入れる
                if (self.weight+WeightandValue[j][0] <= MAX_weight) :
                    self.weight += WeightandValue[j][0]
                # 入らなければ遺伝子を操作
                else :
                    self.gene[j] = 0
        self.updateinfo()

    def showinfo(self) :
        print("gene:{0}, weight:{1}, value:{2}, raito:{3}".format(self.gene, self.weight, self.value, self.raito))

    def updateinfo(self) :
        tmp = np.dot(self.gene, self.WeightandValue)
        self.weight = tmp[0]
        self.value  = tmp[1]
        # ゼロ除算防止
        if (self.weight != 0) :
            self.raito = self.value / self.weight
        else :
            self.raito = 0

    def copy(self) :
        res = Genetic_Biont(self.WeightandValue, MAX_weight)
        res.gene = self.gene.copy()
        res.updateinfo()
        return res

    def mutation(self, p=random.uniform(0, 0.1)) :
        # p:突然変異の確率
        if (p>1) :
            p = 1
        elif (p<0) :
            p = 0

        self.updateinfo()
        # ランダムに遺伝子を決定
        rand_index = random.randint(0, len(self.gene)-1)
        # 突然変異発生なら
        if (random.random() < p) :
            not_gene = (self.gene[rand_index]&1)^1
            if (self.weight + not_gene*self.WeightandValue[rand_index][0] <= MAX_weight) :
                 self.gene[rand_index] = not_gene
        self.updateinfo()

def rec_dp(i, j, dp, WeightandValue):
    """メモ化再起による全探索関数
    i番目以降の品物から重さの和がj以下なるように選んだときの、
    取りうる価値の総和の最大値を返す関数
    """

    # 既にメモ化によって探索された後ならその結果を
    # 探索されていないなら探索した結果を返す
    if (dp[i][j] == -1) :
        if (i == N) :
            # 品物がもう残っていないときは、価値の和の最大値は0で確定
            dp[i][j] = 0
        elif (j < WeightandValue[i][0]) :
            # 残りの容量が足りず品物iを入れられないので、入れないパターンだけ処理
            # i+1 以降の品物のみを使ったときの最大値をそのままこの場合の最大値にする
            dp[i][j] = rec_dp(i + 1, j, dp, WeightandValue)
        else :
            # 品物iを入れるか入れないか選べるので、両方試して価値の和が大きい方を選ぶ
            dp[i][j] = max(rec_dp(i + 1, j, dp, WeightandValue), rec_dp(i + 1, j - WeightandValue[i][0], dp, WeightandValue) + WeightandValue[i][1])

    return dp[i][j]


# 商品の数
N = 20
# ナップサックの入れられる重さ
MAX_weight = 600
# 個体をMAX_biontだけ生成する
MAX_biont = 10
# エリート保存数
MAX_elite = 1
# WeightandValue[i][0]:i番目商品の重さ
# WeightandValue[i][1]:i番目商品の価値
WeightandValue = make_randdata(N)
w = []
for i in WeightandValue :
    w.append(i[0])
# Wの最大値
MAX_W = sum(w)

# メモ化テーブル。
# dp[i][j]はi番目以降の品物から重さの和がj以下なるように選んだときの価値の和の最大値を表す。
# -1なら値が未決定であることを表す
dp = np.zeros([N+1,MAX_W+1])
for i in range(N+1) :
    for j in range(MAX_W+1) :
        dp[i][j] = -1
