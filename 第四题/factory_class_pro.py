# todo 设置详细：
# todo 0 - 7 ： 1-8号零件是否检测
# todo 8 - 10： 1-3号半成品是否检测
# todo 11：成品是否检测
# todo 12 - 14： 1-3号是否拆解
# todo 15：成品是否拆解
CHECK_PRODUCT = 11  # 成品是否检测
DISMANTLE_PRODUCT = 15  # 成品是否拆解
CHECK_SETTINGS = 8  # 偏移量来确定是否需要检测半成品，如序号0 的半成品想知道他是否要检测，则选择查看settings[8]
DISMANTLE_SETTINGS = 12  # 偏移量来确定是否需要拆解半成品
# ASSEMBLE_FAILED_RATE = 0.1  # 组装的失败率，都是0.1


# 零件
class Part:
    def __init__(self, price, num, check_price, defect_rate):
        self.price = price  # 价格
        self.num = num  # 数量
        self.check_price = check_price  # 检测成本
        self.defect_rate = defect_rate  # 不合格率

    def get_num(self):
        return self.num

    # 产生次品
    def clean_defect(self):
        self.num -= self.num * self.defect_rate

    def set_defect_rate(self, defect):
        self.defect_rate = defect

    def __str__(self):
        return f"零件, 数目：{self.num}，价格：{self.price}，检测成本：{self.check_price}，不合格率：{self.defect_rate}"


# 半成品
class Semi_product:
    def __init__(self, num, price, check_price, defect_rate, product_dismantle):
        self.num = num  # 数量
        self.price = price  # 组装成本
        self.check_price = check_price  # 检测成本
        self.num_defect = 0  # 不合格品数量
        self.product_dismantle = product_dismantle  # 拆解成本
        self.defect_rate = 0  # 实际的不合格率
        self.assemble_defect_rate = defect_rate  # 组装时的不合格率

    def clean_defect(self):
        self.num_defect += self.num * self.defect_rate
        self.num -= self.num_defect

    def set_defect_rate(self, defect):
        self.defect_rate = defect

    def __str__(self):
        return f"半成品, 数目：{self.num}，组装成本：{self.price}，检测成本：{self.check_price}，不合格率：{self.defect_rate}"


# 成品
class Product:
    def __init__(self, num, price, check_price, defect_rate, sell_price, product_return, product_dismantle):
        self.num = num  # 数量
        self.price = price  # 组装成本
        self.check_price = check_price  # 检测成本
        self.sell_price = sell_price  # 销售价
        self.product_return = product_return  # 调换损失
        self.product_dismantle = product_dismantle  # 拆解成本
        self.num_defect = 0  # 不合格品数量
        self.defect_rate = 0  # 实际的不合格率
        self.assemble_defect_rate = defect_rate  # 组装时的不合格率

    def __str__(self):
        return f"成品, 数目：{self.num}，组装成本：{self.price}，检测成本：{self.check_price}，不合格率：{self.defect_rate}"

    def set_defect_rate(self, defect):
        self.defect_rate = defect

    def clean_defect(self):
        self.num_defect += self.num * self.defect_rate
        self.num -= self.num_defect


# 流水线
class Factory:
    def __init__(self):
        self.parts = []
        self.semi_products = []
        self.product = Product(0, 0, 0, 0, 0, 0, 0)

        self.settings = []  # 设置(1-8号零件是否检测，1-3号半成品是否检测，成品是否检测，1-3号是否拆解，成品是否拆解）
        # todo 详细：
        # todo 0 - 7 ： 1-8号零件是否检测
        # todo 8 - 10： 1-3号半成品是否检测
        # todo 11：成品是否检测
        # todo 12 - 14： 1-3号是否拆解
        # todo 15：成品是否拆解
        self.score = 0  # 当前设置下的成本

    def set_all_part_num(self, num):
        for part in self.parts:
            part.num = num

    def set_all_semi_num(self, num):
        for semi in self.semi_products:
            semi.num = num

    def set_product_num(self, num):
        self.product.num = num

    # 导入零件信息
    def set_part(self, parts: list[dict]) -> None:
        for part in parts:
            self.parts.append(Part(
                part["price"],
                part["num"],
                part["check_price"],
                part["defect_rate"]
            ))

    def set_semi_product(self, semi_products: list[dict]) -> None:
        for semi in semi_products:
            self.semi_products.append(Semi_product(
                semi["num"],
                semi["price"],
                semi["check_price"],
                semi["defect_rate"],
                semi["product_dismantle"]
            ))

    def set_product(self, product: dict) -> None:
        self.product = Product(
            product["num"],
            product["price"],
            product["check_price"],
            product["defect_rate"],
            product["sell_price"],
            product["product_return"],
            product["product_dismantle"]
        )

    # 设置检测关卡以及是否拆解
    def set_settings(self, settings: list) -> None:
        self.settings = settings
        self.settings = list(settings)

    # 设置运行状态
    def part_running(self) -> bool:
        for part in self.parts:
            if part.num < 1:
                return False
        return True

    def semi_running(self) -> bool:
        for semi in self.semi_products:
            if semi.num < 1:
                return False
        return True

    def get_score(self) -> dict:

        total_product_num = 0
        # 初始化
        self.score = 0
        self.set_all_part_num(100)  # 初始化所有零件数量
        self.set_all_semi_num(0)
        self.set_product_num(0)

        # 成本
        parts_cost = 0  # 零件成本
        semi_product_cost = 0  # 半成品成本
        product_cost = 0  # 成品成本
        product_defect_rate = 0 # 成品不合格率

        for part in self.parts:
            parts_cost += part.price * part.num  # 购买成本

        # 根据设置来模拟工厂运行
        # 生产半成品
        while self.part_running():
            # 是否检测零件次品
            for i in range(0, 8):
                if self.settings[i] == 1:
                    # 检测零件
                    parts_cost += self.parts[i].check_price * self.parts[i].num
                    self.parts[i].clean_defect()  # 清除次品
                    self.parts[i].set_defect_rate(0)  # 设置零件次品率为0，没有次品了
                    self.settings[i] = 0  # 之后便不需要检测了，因为次品已经被检测清除了

            # 组装： 1-3号组成一个半成品， 4-6号组成半成品， 7-8号组成一个半成品
            # 1-3号组成一个半成品
            self.semi_products[0].num += min(  # 半成品数量由最少的一个零件决定
                self.parts[0].num,
                self.parts[1].num,
                self.parts[2].num
            )
            # 组装成本
            semi_product_cost += self.semi_products[0].price * self.semi_products[0].num

            part_correct_rate = 1  # 全部零件正确率
            for i in range(0, 3):
                self.parts[i].num -= self.semi_products[0].num  # 消耗零件
                part_correct_rate *= (1 - self.parts[i].defect_rate)  # 更新全部零件正确率

            # 更新1号半成品的实际次品率
            defect_rate1 = 1 - part_correct_rate * (1 - self.semi_products[0].assemble_defect_rate)  # 1号半成品的次品率
            self.semi_products[0].set_defect_rate(defect_rate1)

            # 4-6号组成半成品
            self.semi_products[1].num += min(
                self.parts[3].num,
                self.parts[4].num,
                self.parts[5].num
            )
            # 组装成本
            semi_product_cost += self.semi_products[1].price * self.semi_products[1].num

            part_correct_rate = 1  # 零件正确率
            for i in range(3, 6):
                self.parts[i].num -= self.semi_products[1].num
                part_correct_rate *= (1 - self.parts[i].defect_rate)

            # 更新2号半成品的实际次品率
            defect_rate2 = 1 - part_correct_rate * (1 - self.semi_products[1].assemble_defect_rate)
            self.semi_products[1].set_defect_rate(defect_rate2)

            # 7-8号组成一个半成品
            self.semi_products[2].num += min(
                self.parts[6].num,
                self.parts[7].num
            )
            # 组装成本
            semi_product_cost += self.semi_products[2].price * self.semi_products[2].num

            part_correct_rate = 1  # 零件正确率
            for i in range(6, 8):
                self.parts[i].num -= self.semi_products[2].num
                part_correct_rate *= (1 - self.parts[i].defect_rate)

            # 更新3号半成品的实际次品率
            defect_rate3 = 1 - part_correct_rate * (1 - self.semi_products[2].assemble_defect_rate)
            self.semi_products[2].set_defect_rate(defect_rate3)

            # 生产成品
            while self.semi_running():
                # 是否检测半成品次品
                for i in range(0, 3):
                    if self.settings[i + CHECK_SETTINGS] == 1:
                        # 检测成本
                        semi_product_cost += self.semi_products[i].check_price * self.semi_products[i].num
                        self.semi_products[i].clean_defect()  # 区分次品
                        self.semi_products[i].set_defect_rate(0)  # 当前的半成品次品率为0
                        # 半成品和零件不一样，之后仍然需要检测
                        # 还需判断是否要拆解：
                        if self.settings[i + DISMANTLE_SETTINGS] == 1:
                            # 拆解费用
                            semi_product_cost += (
                                    self.semi_products[i].product_dismantle
                                    * self.semi_products[i].num_defect
                            )
                            # 根据半成品号数来拆解
                            if i == 0:
                                self.parts[0].num += self.semi_products[i].num_defect
                                self.parts[1].num += self.semi_products[i].num_defect
                                self.parts[2].num += self.semi_products[i].num_defect
                            elif i == 1:
                                self.parts[3].num += self.semi_products[i].num_defect
                                self.parts[4].num += self.semi_products[i].num_defect
                                self.parts[5].num += self.semi_products[i].num_defect
                            elif i == 2:
                                self.parts[6].num += self.semi_products[i].num_defect
                                self.parts[7].num += self.semi_products[i].num_defect
                        # 不论是否拆解，残次半成品数目清零
                        self.semi_products[i].num_defect = 0
                        self.semi_products[i].set_defect_rate(0)  # 更新成品的实际残次率

                    else:
                        # 保持当前次品率继续
                        pass

                # 组装： 1-3号半成品组成成品
                self.product.num += min(
                    self.semi_products[0].num,
                    self.semi_products[1].num,
                    self.semi_products[2].num
                )
                # 计算成品正确率, 更新半成品数量
                semi_product_correct_rate = 1
                for i in range(0, 3):
                    semi_product_correct_rate *= (1 - self.semi_products[i].defect_rate)
                    self.semi_products[i].num -= self.product.num

                # 更新成品的实际残次率
                # 实际残次率源于半成品的残次率和自身残次率
                defect_rate = 1 - semi_product_correct_rate * (1 - self.product.assemble_defect_rate)
                self.product.set_defect_rate(defect_rate)
                product_defect_rate = defect_rate

                # 是否检测成品：
                product_cost += self.product.price * self.product.num  # 组装成本
                if self.settings[CHECK_PRODUCT] == 1:
                    product_cost += self.product.check_price * self.product.num  # 检测成本
                    self.product.clean_defect()  # 区分次品, 这里会修改num和num_defect 的值
                    self.product.set_defect_rate(0)  # 综合次品率 0%

                else:
                    # 流入市场，并承担调换费用， 保持综合次品率不变
                    self.product.clean_defect()  # 区分次品, 这里会修改num和num_defect 的值
                    product_cost += self.product.num_defect * self.product.product_return  # 调换费用

                total_product_num += self.product.num  # 生产产品正品数保存
                # 是否拆解残次成品
                if self.settings[DISMANTLE_PRODUCT] == 1:
                    # 拆解费用
                    product_cost += (
                            self.product.product_dismantle
                            * self.product.num_defect
                    )
                    # 拆解成半成品
                    self.semi_products[0].num += self.product.num_defect
                    self.semi_products[1].num += self.product.num_defect
                    self.semi_products[2].num += self.product.num_defect
                self.product.num_defect = 0  # 清零
                self.product.num = 0

        # 综合利润：
        self.score = total_product_num * self.product.sell_price - product_cost - semi_product_cost - parts_cost
        return {
            "score": round(self.score, 2),
            "total_product_num": round(total_product_num, 2),
            "product_cost": round(product_cost, 2),
            "semi_product_cost": round(semi_product_cost, 2),
            "parts_cost": round(parts_cost, 2),
            "product_defect_rate": product_defect_rate
        }
