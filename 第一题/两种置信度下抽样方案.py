import math

from scipy.stats import norm

# 样本容量
n95 = 139
n90 = 98

# 次品率
p = 0.1

# 求出临界值
# 95% 置信度
k95 = n95 * p + norm.ppf(0.95) * math.sqrt(n95 * p * (1 - p))
k95 = math.ceil(k95)  # 向上取整
print('95%置信度下临界值: ', k95)

k90 = n90 * p + norm.ppf(0.90) * math.sqrt(n90 * p * (1 - p))
k90 = math.ceil(k90)
print('90%置信度下临界值: ', k90)
