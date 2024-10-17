import pandas as pd
from matplotlib import pyplot as plt
from generation import *
import seaborn as sns
import time

# todo 全局设置
INDIVIDUAL_SIZE = 16  # 个体长度
POPULATION_SIZE = 100  # 种群大小
MAX_GENERATION = 20  # 最大迭代次数
MUTATION_RATE = 0.05  # 变异概率
POPULATION_RATE = 0.5  # 繁衍比率
CROSS_RATE = 0.5  # 交叉概率
TEST_TIMES = 50  # 测试次数

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


def main():
    global log  # 记录日志
    population = []  # 种群
    best_score = 0  # 最高分数
    best_settings = []  # 最优设置
    best_score_logs = []  # 最高分数记录
    best_settings_logs = []  # 最优设置记录
    shou_lian_times_ = 0  # 收敛所用次数
    start = time.time()
    # 初始化种群
    individuals = generate_population(INDIVIDUAL_SIZE, POPULATION_SIZE)

    # 更改数据结构
    for i in individuals:
        population.append({"individual": i, "score": 0})

    # 模拟种群运行
    for i in range(MAX_GENERATION):
        population = breed(population)  # 繁衍
        population = select(population)  # 选择
        if population[0]["score"] > best_score:
            best_score = population[0]["score"]  # 最高分数
            shou_lian_times_ = i + 1
        best_settings = population[0]["individual"]  # 记录最优设置
        best_score_logs.append(best_score)  # 记录最高分数
        best_settings_logs.append(best_settings)  # 记录最优设置
        # print(f"第{i+1}代, 最优分数为{best_score}, 最优设置: {best_settings}， 人口大小： {len(population)}")

    end = time.time()

    log.append({
        "best_settings": str(best_settings),
        "best_score": round(best_score / 100, 2),
    })
    # print("收敛次数：", shou_lian_times_)
    # print("最优设置:", best_settings)
    # print("最优分数:", best_score)

    return shou_lian_times_, end - start


if __name__ == "__main__":
    shou_lian_times_log = []  # 收敛次数记录
    run_time_log = []  # 运行时间记录
    log = []  # 记录数据

    for _ in range(TEST_TIMES):
        shou_lian_times, run_time = main()
        shou_lian_times_log.append(shou_lian_times)
        run_time_log.append(run_time)

    shou_lian_times = sum(shou_lian_times_log)
    run_time = sum(run_time_log)

    print("平均运行时间：", run_time / TEST_TIMES, 4)
    print("平均收敛次数：", shou_lian_times / TEST_TIMES)

    # 日志保存：
    print(log)
    log = pd.DataFrame(log)
    log.to_csv("遗传算法稳定性检验数据.csv", index=False)

    df = pd.DataFrame(shou_lian_times_log)

    # 使用seaborn来绘制优化过程
    sns.lineplot(data=df)
    plt.xlabel("运行次数")
    plt.ylabel("收敛次数")
    plt.title(f"遗传算法收敛次数，平均次数{shou_lian_times / TEST_TIMES}", fontsize=18)
    plt.savefig("遗传算法迭代次数.png")
    plt.show()

    df = pd.DataFrame(run_time_log)
    # 使用seaborn来绘制优化过程
    sns.lineplot(data=df)
    plt.xlabel("运行次数")
    plt.ylabel("运行所用时间")
    plt.title(f"遗传算法运行时间，平均运行时间{round(run_time / TEST_TIMES, 3)}s", fontsize=18)
    plt.savefig("遗传算法运行时间.png")
    plt.show()
