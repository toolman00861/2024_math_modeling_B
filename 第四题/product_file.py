parts = [
    {'num': 100, 'price': 2, 'check_price': 1, 'defect_rate': 0.1},
    {'num': 100, 'price': 8, 'check_price': 1, 'defect_rate': 0.1},
    {'num': 100, 'price': 12, 'check_price': 2, 'defect_rate': 0.1},
    {'num': 100, 'price': 2, 'check_price': 1, 'defect_rate': 0.1},
    {'num': 100, 'price': 8, 'check_price': 1, 'defect_rate': 0.1},
    {'num': 100, 'price': 12, 'check_price': 2, 'defect_rate': 0.1},
    {'num': 100, 'price': 8, 'check_price': 1, 'defect_rate': 0.1},
    {'num': 100, 'price': 12, 'check_price': 2, 'defect_rate': 0.1},
]

semi_products = [
    {'num': 0, 'price': 8, 'check_price': 4, 'defect_rate': 0.1, 'product_dismantle': 6},
    {'num': 0, 'price': 8, 'check_price': 4, 'defect_rate': 0.1, 'product_dismantle': 6},
    {'num': 0, 'price': 8, 'check_price': 4, 'defect_rate': 0.1, 'product_dismantle': 6}
]

product = {
    'num': 0,  # 生产数量
    'price': 8,  # 组装成本
    'check_price': 6,  # 检查成本
    'product_dismantle': 10,  # 拆解成本
    'defect_rate': 0.1,  # 次品率
    'product_return': 40,  # 调换成本
    'sell_price': 200,  # 销售价
}
