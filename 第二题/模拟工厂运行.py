import itertools
from matplotlib import pyplot as plt
import pandas as pd
from factory_class import Factory
from case_file import cases
import seaborn as sns

# 设置sns字体
sns.set(font=['Microsoft YaHei'])
sns.set_context("paper")
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.size'] = 18  # 设置全局字体大小


# 生成所有组合的函数
def generate_combinations(n):
    return list(itertools.product([0, 1], repeat=n))


if __name__ == '__main__':
    i = 1  # 遍历案例的编号
    best_score_logs = []  # 最优的分数记录
    best_settings_logs = []  # 最优的设置记录

    log = open("log.csv", "w")
    log.write("//best_setting含义：第一个是否检测，第二个是否检测，产品是否检测，产品是否拆解\n")
    # 遍历6个案例
    for case in cases:
        print("案例: ", i)
        factory = Factory()  # 实例化流水线
        # 初始化设置
        factory.set_defect_rate(
            case["part_1_defect"],
            case["part_2_defect"],
            case["product_defect"]
        )
        factory.set_price(
            case["part_1_price"],
            case["part_2_price"],
            case["product_price"],
            case["product_sell"]
        )
        factory.set_check(
            case["part_1_check"],
            case["part_2_check"],
            case["product_check"]
        )
        factory.set_return(
            case["product_return"],
            case["product_dismantle"]
        )
        # 生成所有可能的组合
        settings = generate_combinations(4)
        best_setting = []  # 最优的设置
        max_score = 0  # 最优的分数
        for setting in settings:
            factory.set_settings(setting)
            score = factory.get_score()
            if score > max_score:
                max_score = score
                best_setting = setting
            # print(setting, score)
        print("max_score:", round(max_score, 2))
        print("best_setting:", best_setting)

        best_score_logs.append(round(max_score, 2))
        best_settings_logs.append(str(best_setting))

        log.write("case: " + str(i) + "\t")
        log.write("max_score: " + str(round(max_score, 2)) + "\t")
        log.write("best_setting: " + str(best_setting) + "\n")
        i += 1

    # 将分数除以100,得到平均利润
    for i in range(len(best_score_logs)):
        best_score_logs[i] /= 100
        best_score_logs[i] = round(best_score_logs[i], 2)

    # 使用sns绘制条形图
    df = {
        "案例编号": ['1', '2', '3', '4', '5', '6'],
        "最佳分数": best_score_logs,
        "最佳设置": best_settings_logs
    }

    df = pd.DataFrame(df)
    print(df)
    df.to_csv("best_setting.csv")

    # 绘制条形图
    plt.figure(figsize=(10, 6))
    bar_plot = sns.barplot(x="案例编号", y="最佳分数", data=df, palette="viridis")
    plt.xticks(fontsize=14)  # 设置 x 轴刻度标签的字体大小
    plt.yticks(fontsize=14)  # 设置 y 轴刻度标签的字体大小

    # 添加最佳分数数据和设置标签
    for index, row in df.iterrows():
        bar_plot.text(index, row["最佳分数"] + 1, f"{row['最佳分数']}\n{row['最佳设置']}",
                      color='black', ha="center", va="bottom")

    # 这里更新了y轴的显示范围
    y_start = min(best_score_logs) * 0.9
    y_end = max(best_score_logs) * 1.1
    plt.ylim(y_start, y_end)

    plt.title("案例每件利润与分数", fontsize=20)
    plt.xlabel("案例编号", fontsize=20)
    plt.ylabel("每件利润", fontsize=20)
    plt.savefig("best_setting.png")  # 保存结果图片
    plt.show()
