import itertools
import random
from matplotlib import pyplot as plt
import pandas as pd
from 第二题 import factory_class, case_file
import seaborn as sns

# 设置sns字体
sns.set(font=['Microsoft YaHei'])
sns.set_context("paper")
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.size'] = 16  # 设置全局字体大小


# 生成所有组合的函数
def generate_combinations(n):
    return list(itertools.product([0, 1], repeat=n))


test_times = 200  # 测试次数
cases = case_file.cases  # 读取所有案例
E = 0.05  # 允许的误差
log = []

if __name__ == '__main__':
    i = 1  # 遍历案例的编号
    best_score_logs = []  # 最优的分数记录
    best_settings_logs = {
        '案例1': {},
        '案例2': {},
        '案例3': {},
        '案例4': {},
        '案例5': {},
        '案例6': {}
    }  # 最优的设置记录
    for case in cases:
        for t in range(test_times):
            test_case = case.copy()  # 复制一个实例
            # 基于原有次品率随机生成各零件的次品率
            test_case['part_1_defect'] = round(random.uniform(case['part_1_defect'] - E, case['part_1_defect'] + E), 4)
            test_case['part_2_defect'] = round(random.uniform(case['part_2_defect'] - E, case['part_2_defect'] + E), 4)
            test_case['product_defect'] = round(random.uniform(case['product_defect'] - E, case['product_defect'] + E), 4)
            factory = factory_class.Factory()
            # 初始化设置
            factory.set_defect_rate(
                test_case["part_1_defect"],
                test_case["part_2_defect"],
                test_case["product_defect"]
            )
            factory.set_price(
                test_case["part_1_price"],
                test_case["part_2_price"],
                test_case["product_price"],
                test_case["product_sell"]
            )
            factory.set_check(
                test_case["part_1_check"],
                test_case["part_2_check"],
                test_case["product_check"]
            )
            factory.set_return(
                test_case["product_return"],
                test_case["product_dismantle"]
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
            # print(f"第{i}个案例，第{t + 1}次测试，最优设置：{best_setting}，最优分数：{round(max_score, 2)}")
            log.append({
                '案例编号': i,
                '测试轮次': t + 1,
                '最优设置': tuple(best_setting),
                '最优分数': round(max_score / 100, 2)
            })
            try:
                best_settings_logs[f'案例{i}'][tuple(best_setting)] += 1
            except KeyError:
                best_settings_logs[f'案例{i}'][tuple(best_setting)] = 1

        i += 1
    log = pd.DataFrame(log)
    log.to_csv('第二题重新检验.csv', index=False)
    # 减少采样数据点
    log_sampled = log.groupby('案例编号').apply(lambda x: x.iloc[::10, :]).reset_index(drop=True)
    sns.lineplot(data=log_sampled, x='测试轮次', y='最优分数', hue='案例编号')
    plt.title('第二题不同案例下不同测试轮次的最优分数', fontsize=15)
    plt.savefig('第二题不同案例下不同测试轮次的最优分数.png')
    plt.show()

    # 画出不同案例下最优分数中位数
    grouped_log = log.groupby('案例编号')['最优分数'].mean()
    print(grouped_log)
    sns.barplot(x=grouped_log.index, y=grouped_log.values)
    plt.title('第二题不同案例下最优分数平均数', fontsize=15)
    plt.savefig('第二题不同案例下最优分数平均数.png')
    plt.show()

    # 画出不同案例下最优设置的众数
    li = []
    y = 1
    for test_case in best_settings_logs.values():
        setting, count = max(test_case.items(), key=lambda item: item[1])
        li.append({
            '案例编号': y,
            '最优设置': setting,
            '出现次数': count
        })
        y += 1
    li = pd.DataFrame(li)
    print(li)
    bar_plot = sns.barplot(data=li, x='案例编号', y='出现次数', hue='案例编号')
    # 添加最佳分数数据和设置标签
    for index, row in li.iterrows():
        bar_plot.text(index, row["出现次数"], f"{row['最优设置']}",color='black', ha="center", va="bottom")
    plt.title('第二题不同案例下最优设置的众数', fontsize=15)
    plt.xlabel('案例编号', fontsize=15)
    plt.ylabel('出现次数最高的最优设置', fontsize=15)
    plt.savefig('第二题不同案例下最优设置的众数.png')
    plt.show()
