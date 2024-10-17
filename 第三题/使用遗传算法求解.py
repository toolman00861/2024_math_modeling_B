import pandas as pd
from matplotlib import pyplot as plt
from generation import *
import seaborn as sns
import time

"""
    解释一下population的数据结构：
    [
        {'individual': 个体, 'score': 分数},
        {'individual': 个体, 'score': 分数},
        ....
    ]
"""

# todo 设置序列详细：
# todo 0 - 7 ： 1-8号零件是否检测
# todo 8 - 10： 1-3号半成品是否检测
# todo 11：成品是否检测
# todo 12 - 14： 1-3号是否拆解
# todo 15：成品是否拆解

# todo 全局设置
INDIVIDUAL_SIZE = 16  # 个体长度
POPULATION_SIZE = 100  # 种群大小
MAX_GENERATION = 20  # 最大迭代次数
MUTATION_RATE = 0.05  # 变异概率
POPULATION_RATE = 0.5  # 繁衍比率
CROSS_RATE = 0.5  # 交叉概率

# 设置sns字体
sns.set(font=['Microsoft YaHei'])
sns.set_context("paper")
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.size'] = 18  # 设置全局字体大小


def plot_show(times, score_logs):
    # 使用seaborn来绘制优化过程
    sns.lineplot(x=range(times), y=score_logs)
    plt.xlabel("迭代次数")
    plt.ylabel("最优分数")
    plt.title("遗传算法优化过程", fontsize=18)
    plt.savefig("遗传算法优化过程.png")
    plt.show()


if __name__ == "__main__":
    population = []  # 种群
    best_score = 0  # 最高分数
    best_settings = []  # 最优设置
    best_score_logs = []  # 最高分数记录
    best_settings_logs = []  # 最优设置记录
    shou_lian_times = 0  # 收敛所用次数
    start_time = time.time()  # 开始时间
    log = []  # 运行日志

    # 初始化种群
    individuals = generate_population(INDIVIDUAL_SIZE, POPULATION_SIZE)
    print("初始化种群")

    # 更改数据结构
    for i in individuals:
        population.append({"individual": i, "score": 0})

    # 模拟种群运行
    for i in range(MAX_GENERATION):
        population = breed(population)  # 繁衍
        population = select(population)  # 选择
        if population[0]["score"] > best_score:
            best_score = population[0]["score"]  # 最高分数
            shou_lian_times = i + 1
        best_settings = population[0]["individual"]  # 记录最优设置
        best_score_logs.append(best_score)  # 记录最高分数
        best_settings_logs.append(best_settings)  # 记录最优设置
        # print(f"第{i+1}代, 最优分数为{best_score}, 最优设置: {best_settings}， 人口大小： {len(population)}")
        log.append({
            "generation": i + 1,
            "best_score": best_score,
            "best_settings": best_settings,
            "population_size": len(population),
        })

    end_time = time.time()  # 结束时间

    log = pd.DataFrame(log)
    log.to_csv("遗传算法运行日志.csv", index=False)

    print("遗传算法运行时间：", round(end_time - start_time, 4), 's')
    print("收敛次数：", shou_lian_times)
    print("最优设置:", best_settings)
    print("最优每件利润:", round(best_score / 100, 2))

    # 将分数除以100,得到平均利润
    for i in range(len(best_score_logs)):
        best_score_logs[i] /= 100
        best_score_logs[i] = round(best_score_logs[i], 2)

    # 使用seaborn来绘制优化过程
    plot_show(MAX_GENERATION, best_score_logs)
