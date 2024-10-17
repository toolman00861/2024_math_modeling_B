# 使用遗传算法来优化选择模型
import random
from factory_class_pro import Factory

# 全局设置
INDIVIDUAL_SIZE = 16  # 个体长度
POPULATION_SIZE = 100  # 种群大小
MAX_GENERATION = 20  # 最大迭代次数
MUTATION_RATE = 0.05  # 变异概率
POPULATION_RATE = 0.5  # 繁衍比率
CROSS_RATE = 0.5  # 交叉概率


# 随机生成初始化种群
def generate_population(individual_size, population_size):
    population_ = []
    for n_ in range(population_size):
        li = []
        for i_ in range(individual_size):
            li.append(random.randint(0, 1))
        population_.append(li)
    return population_


# 评估存活率函数
def calculate_score(individual: list, parts_, semi_products_, product_) -> float:
    factory = Factory()
    factory.set_settings(individual)
    factory.set_part(parts_)
    factory.set_semi_product(semi_products_)
    factory.set_product(product_)
    data = factory.get_score()
    return round(data['score'], 2)


# 交叉操作, 两个父母生两个娃，保证群体数目不波动
def crossover(parent1: dict, parent2: dict) -> (dict, dict):
    child_1 = {'individual': [], 'score': 0}
    child_2 = {'individual': [], 'score': 0}
    for i__ in range(len(parent1['individual'])):
        if random.random() < 0.5:
            child_1['individual'].append(parent1['individual'][i__])
            child_2['individual'].append(parent2['individual'][i__])
        else:
            child_1['individual'].append(parent2['individual'][i__])
            child_2['individual'].append(parent1['individual'][i__])
    return child_1, child_2


# 变异操作
def mutate(individual_: dict) -> dict:
    for i_ in range(len(individual_)):
        if random.random() < MUTATION_RATE:
            individual_['individual'][i_] = 1 - individual_['individual'][i_]
    return individual_


# 种群繁衍，假设都会繁衍
def breed(population_: list) -> list:
    new_population = population_
    for i_ in range(int(len(population_) * POPULATION_RATE)):
        # 随机选择一对父母
        parent1 = random.choice(population_)
        parent2 = random.choice(population_)
        child_1, child_2 = crossover(parent1, parent2)  # 交叉
        child_1 = mutate(child_1)  # 变异
        child_2 = mutate(child_2)
        # 添加新成员
        new_population.append(child_1)
        new_population.append(child_2)
    return new_population


# 进行自然选择，淘汰一半个体
def select(population_: list, parts_: dict, semi_products_: dict, product_: dict) -> list:
    """
    解释一下population_的数据结构：
    [
        {'individual': 个体, 'score': 分数},
        {'individual': 个体, 'score': 分数},
        ....
    ]
    """
    for y in population_:
        y["score"] = calculate_score(y["individual"], parts_, semi_products_, product_)
    population_.sort(key=lambda x: x["score"], reverse=True)  # 按分数排序
    return population_[:int(len(population_) * POPULATION_RATE)]  # 选出前50%
