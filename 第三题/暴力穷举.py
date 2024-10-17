import itertools
import time

from factory_class_pro import Factory
from product_file import parts, semi_products, product


# todo 设置序列详细：
# todo 0 - 7 ： 1-8号零件是否检测
# todo 8 - 10： 1-3号半成品是否检测
# todo 11：成品是否检测
# todo 12 - 14： 1-3号是否拆解
# todo 15：成品是否拆解
def generate_combinations(n):
    return list(itertools.product([0, 1], repeat=n))


if __name__ == '__main__':
    start_time = time.time()  # 开始时间
    # 生成所有可能的组合
    settings = generate_combinations(16)  # 16个参数 65536 种组合
    best_setting = []  # 最优的设置
    max_score = 0  # 最优的分数
    product_defect_rate = 0  # 产品综合次品率
    data = []

    for setting in settings:
        factory = Factory()
        # 重置工厂属性
        factory.set_part(parts)
        factory.set_semi_product(semi_products)
        factory.set_product(product)
        factory.set_settings(setting)

        data = factory.get_score()
        if data["score"] > max_score:
            max_score = data["score"]
            best_setting = setting
            product_defect_rate = round(data["product_defect_rate"], 4)
        # print(setting, data["score"])

    end_time = time.time()  # 结束时间
    run_time = round(end_time - start_time, 4)
    print("暴力枚举所有情况运行时间运行时间：", run_time, 's')
    print("最优每件利润:", round(max_score / 100, 2))
    print("最优设置:", best_setting)
    print('产品综合次品率：', product_defect_rate * 100, '%')
