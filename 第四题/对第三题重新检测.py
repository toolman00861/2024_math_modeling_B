import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from generation import *
import seaborn as sns
import time
from product_file import parts, semi_products, product

# todo 全局设置
INDIVIDUAL_SIZE = 16  # 个体长度
POPULATION_SIZE = 100  # 种群大小
MAX_GENERATION = 20  # 最大迭代次数
MUTATION_RATE = 0.05  # 变异概率
POPULATION_RATE = 0.5  # 繁衍比率
CROSS_RATE = 0.5  # 交叉概率
TEST_TIMES = 50  # 测试次数
E = 0.05  # 误差

# 设置sns字体
sns.set(font=['Microsoft YaHei'])
sns.set_context("paper")
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.size'] = 18  # 设置全局字体大小


def plot_show(times, score_logs):
    # 使用seaborn来绘制优化过程
    sns.lineplot(x=range(times), y=score_logs)
    plt.xlabel("测试次数")
    plt.ylabel("最优分数")
    plt.title("遗传算法检验运行过程", fontsize=18)
    plt.savefig("遗传算法检验运行过程.png")
    plt.show()


def main(parts_, semi_products_, product_):
    population = []  # 种群
    best_score = 0  # 最高分数
    best_settings = []  # 最优设置
    best_score_logs = []  # 最高分数记录
    best_settings_logs = []  # 最优设置记录
    # 初始化种群
    individuals = generate_population(INDIVIDUAL_SIZE, POPULATION_SIZE)

    # 更改数据结构
    for i in individuals:
        population.append({"individual": i, "score": 0})

    # 模拟种群运行
    for i in range(MAX_GENERATION):
        population = breed(population)  # 繁衍
        population = select(population, parts_, semi_products_, product_)  # 选择
        if population[0]["score"] > best_score:
            best_score = population[0]["score"]  # 最高分数
        best_settings = population[0]["individual"]  # 记录最优设置
        best_score_logs.append(best_score)  # 记录最高分数
        best_settings_logs.append(best_settings)  # 记录最优设置

    return best_settings, best_score


if __name__ == "__main__":
    best_settings_log = []  # 最优设置记录
    best_score_log = []  # 最高分数记录
    log = []  # 测试记录

    for _ in range(TEST_TIMES):
        # 基于随机数据进行测试
        parts_, semi_products_, product_ = parts.copy(), semi_products.copy(), product.copy()
        for part_ in parts_:
            part_['defect_rate'] = random.uniform(0.1 - E, 0.1 + E)
        for semi_product_ in semi_products_:
            semi_product_['defect_rate'] = random.uniform(0.1 - E, 0.1 + E)

        product_['defect_rate'] = random.uniform(0.1 - E, 0.1 + E)

        best_settings, best_score = main(parts_, semi_products_, product_)
        best_settings_log.append(tuple(best_settings))
        best_score_log.append(best_score)
        log.append({
            "测试轮次": _ + 1,
            "最优设置": tuple(best_settings),
            "最优设置对应的最优利润": round(best_score / 100, 2),
        })

    # 计算每件利润
    for i in range(len(best_score_log)):
        best_score_log[i] = round(best_score_log[i] / 100, 2)

    # 生成数据框
    df = pd.DataFrame(log)
    df.to_csv("第三问测试结果.csv", index=False)
    plot_show(TEST_TIMES, best_score_log)

    print("平均最优分数： ", round(sum(best_score_log) / len(best_score_log), 2))

    setting_counter = {}  # 记录最优设置数目
    for setting in best_settings_log:
        if setting in setting_counter:
            setting_counter[setting] += 1
        else:
            setting_counter[setting] = 1
    print("最优设置分布： ")
    for setting, count in setting_counter.items():
        print(setting, count)

