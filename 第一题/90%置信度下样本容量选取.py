import math
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import norm

# 设置sns字体
sns.set(font=['Microsoft YaHei'])
sns.set_context("paper")
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False


# 样本容量确定（二项分布）
def get_sample_size(a, p, d):
    # a是置信度
    # d是允许的误差
    # p是次品概率
    z = norm.ppf((1 - a) / 2)  # z是正态分布的a/2 的分位数
    return math.ceil(z * z * p * (1 - p) / (d * d))


# 允许误差和样本容量关系
for i in range(1, 11):
    dd = i * 0.01  # 允许的误差
    sample_size = get_sample_size(0.90, 0.1, dd)
    print(dd, sample_size)
    # 使用seaborn的散点图绘制
    # 显示每个点的数值
    plt.text(dd, sample_size, str(sample_size), ha='center', va='bottom')
    plt.title('90%置信度下允许的误差和样本容量关系', fontsize=16)
    plt.xlabel('允许的误差')
    plt.ylabel('抽取的样本容量')
    sns.set_style("whitegrid")
    sns.scatterplot(x=[dd] * sample_size, y=np.arange(sample_size))

plt.savefig('90%置信度下允许的误差和样本容量关系.png')
plt.show()

