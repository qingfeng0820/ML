# -*- coding: utf-8 -*-
from math import sqrt


# 返回一个有关person1和person2的基于距离的相似度评价
def sim_distance(prefs, person1, person2):
    # 得到双方都评价过的物品列表
    si = {}
    for item in prefs[person1]:
        if item in prefs[person2]:
            si[item] = 1

    # 如果两者没有任何双方都评价过的物品，即没共同之处，返回0
    if len(si) == 0:
        return 0

    # 计算所有差值的平方和
    sum_of_squares = sum([pow(prefs[person1][item] - prefs[person2][item], 2) for item in si])

    # 归一
    return 1 / (1 + sqrt(sum_of_squares))


# 返回person1和person2的皮尔逊相关系数
def sim_pearson(prefs, person1, person2):
    # 得到双方都评价过的物品列表
    si = {}
    for item in prefs[person1]:
        if item in prefs[person2]:
            si[item] = 1

    # 得到物品列表的长度
    n = len(si)

    # 如果两者没有任何双方都评价过的物品，即没共同之处，返回0
    if n == 0:
        return 0

    # pearson_correlation = E((x - E(x))(y - E(y))) / SD(x)SD(y)
    # pearson_correlation = [E(xy) - E(x)E(y)] / [sqrt((E(sqr(x)) - sqr(E(x)))) * sqrt((E(sqr(y)) - sqr(E(y))))]
    # pearson_correlation = [sum(xy) / n - sum(x) * sum(y) / sqr(n)] / [sqrt((sum(sqr(x)) / n - sqr(sum(x)) / sqr(n))) * sqrt((sum(sqr(y)) / n - sqr(sum(y)) / sqr(n)))]
    # pearson_correlation = [sum(xy) - sum(x) * sum(y) / n] / [sqrt((sum(sqr(x))  - sqr(sum(x)) / n)) * sqrt((sum(sqr(y)) - sqr(sum(y)) / n))]

    # 所有偏好的和
    sum1 = sum([prefs[person1][it] for it in si])
    sum2 = sum([prefs[person2][it] for it in si])

    # 所有偏好平方的和
    sqSum1 = sum([pow(prefs[person1][it], 2) for it in si])
    sqSum2 = sum([pow(prefs[person2][it], 2) for it in si])

    # 所有偏好相互乘积的和
    pSum = sum([prefs[person1][it] * prefs[person2][it] for it in si])

    # 计算皮尔逊评价值
    num = pSum - (sum1 * sum2 / n)
    den = sqrt(sqSum1 - pow(sum1, 2) / n) * sqrt(sqSum2 - pow(sum2, 2) / n)

    return num / den


# 从反映偏好的数据中返回最为匹配者
def top_matches(prefs, person, n=5, similarity=sim_pearson):
    scores = [(similarity(prefs, person, other), other) for other in prefs if other != person]

    # 对列表排序
    scores.sort()
    # 切片，评价值最高排在最前面
    ret = scores[-n:]
    ret.reverse()
    return ret


# 利用所有他人评价值的加权平均，为某人提供建议 (user-based collaborative filtering)
def get_recommendations(prefs, person, similarity=sim_pearson):
    totals = {}
    sim_sums = {}
    for other in prefs:
        # 不要和自己做比较
        if other == person:
            continue
        sim = similarity(prefs, person, other)

        # 忽略与自己相似度为0或者小于0的人
        if sim < 0:
            continue

        # 遍历他人的评价值
        for item in prefs[other]:
            # 只对自己没有评价过(或者评价值为0)的评价值做推荐
            if item not in prefs[person] or prefs[person][item] == 0:
                # 评价值 * 相似度 (加权评价值) 之和
                totals.setdefault(item, 0)
                totals[item] += prefs[other][item] * sim
                # 相似度之和
                sim_sums.setdefault(item, 0)
                sim_sums[item] += sim

    # 构建一个归一化推荐列表
    rankings = [(total / sim_sums[item], item) for item, total in totals.items()]

    rankings.sort()
    rankings.reverse()
    return rankings


def transform_prefs(prefs):
    results = {}
    for person in prefs:
        for item in prefs[person]:
            results.setdefault(item, {})

            # 将人和物品对调
            results[item][person] = prefs[person][item]
    return results


# 构建相似物品数据集
def calculate_similar_items(prefs, n=10, similarity=sim_pearson):
    # 建立字典，以给出与这些物品最为相近的所有其他物品
    results = {}

    # 以物品为中心对偏好矩阵实施倒置处理
    item_prefs = transform_prefs(prefs)
    # 状态变量，用来打印进度
    c = 0
    for item in item_prefs:
        # 针对大数据集更新状态变量
        c += 1
        if c % 100 == 0:
            print "%d %d" % (c, (c, len(item_prefs)))
        # 寻找最为相近的物品
        scores = top_matches(item_prefs, item, n=n, similarity=similarity)
        results[item] = scores
    return results


# 利用相似物品数据集，给用户做推荐 (item-based collaborative filtering)
def get_recommended_items(prefs, similar_items, user):
    user_ratings = prefs[user]
    scores = {}
    total_sim = {}
    # 遍历当前用户评分的物品
    for (item, rating) in user_ratings.items():
        # 遍历与当前物品相近的物品
        for (sim, item2) in similar_items[item]:
            # 如果该用户已经评价过该物品，则将其忽略
            if item2 in user_ratings:
                continue
            # 评价值 * 相似度 (加权评价值) 之和
            scores.setdefault(item2, 0)
            scores[item2] += rating * sim
            # 全部相似度之和
            total_sim.setdefault(item2, 0)
            total_sim[item2] += sim

    # 构建一个归一化推荐列表
    rankings = [(score / total_sim[item], item) for item, score in scores.items()]

    rankings.sort()
    rankings.reverse()
    return rankings
