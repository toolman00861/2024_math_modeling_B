# 这个文件是工厂类，负责模拟工厂生产产品，并计算相对应的利润（score）
# 设定工厂的流水线：
# 流水线有1，2两种零件，将两种零件加工成成品
# 现在设置检测环节，可以选择是否检测1，2，成品，以及失败成品是否拆解
# 对所有情况进行评分处理。

class Factory:
    def __init__(self):
        self.part_1 = 0  # 第一种零件总数
        self.part_1_defect = 0  # 第一种零件不合格率
        self.part_1_price = 0  # 第一种零件价格
        self.part_1_check = 0  # 第一种零件检测费用

        self.part_2 = 0  # 第二种零件总数
        self.part_2_defect = 0  # 第二种零件不合格率
        self.part_2_price = 0  # 第二种零件价格
        self.part_2_check = 0  # 第二种零件检测费用

        self.product = 0  # 成品总数
        self.product_defect = 0  # 成品实际不合格率
        self.product_assemble_defect_rate = 0  # 成品组装不合格率
        self.product_price = 0  # 成品组装成本
        self.product_check = 0  # 成品检测费用
        self.product_sell = 0  # 成品销售价
        self.product_return = 0  # 调换损失
        self.product_dismantle = 0  # 拆解成本

        self.settings = []  # 设置(1,2,成品，是否检测，失败是否拆解)
        self.score = 0  # 当前设置下的成本

    # 设置各零件的不合格率
    def set_defect_rate(self, part_1_defect, part_2_defect, product_defect) -> None:
        self.part_1_defect = part_1_defect
        self.part_2_defect = part_2_defect
        self.product_assemble_defect_rate = product_defect

    # 设置各零件成本
    def set_price(self, part_1_price, part_2_price, product_price, product_sell) -> None:
        self.part_1_price = part_1_price
        self.part_2_price = part_2_price
        self.product_price = product_price
        self.product_sell = product_sell

    # 设置检测费用
    def set_check(self, part_1_check, part_2_check, product_check) -> None:
        self.part_1_check = part_1_check
        self.part_2_check = part_2_check
        self.product_check = product_check

    # 设置返工成本
    def set_return(self, product_return, product_dismantle) -> None:
        self.product_return = product_return
        self.product_dismantle = product_dismantle

    #  设置检测关卡以及是否拆解
    def set_settings(self, settings: list) -> None:
        self.settings = settings
        self.settings = list(settings)

    def get_score(self) -> float:
        # 初始化
        self.score = 0  # 分数
        self.part_1 = 100  # 第一种零件总数
        self.part_2 = 100  # 第二种零件总数
        self.product = 0

        cost_1 = 0  # 检测零件1成本
        cost_2 = 0  # 检测零件2成本
        cost_product = 0  # 组装成本
        defect_cost = 0  # 不合格品所产生的成本
        total_product = 0  # 成品总数

        # 购买零件成本
        self.score -= self.part_1 * self.part_1_price
        self.score -= self.part_2 * self.part_2_price

        # 根据设置来模拟工厂运行
        while self.part_1 >= 1 and self.part_2 >= 1:  # 终止条件，只要有一个零部件用完了就结束
            # print("part_1:", self.part_1, "part_2:", self.part_2)
            # 是否检测零件一二次品
            if self.settings[0] == 1:
                cost_1 += self.part_1 * self.part_1_check * self.settings[0]  # 检测零件1成本
                self.part_1 -= self.part_1 * self.part_1_defect  # 去除不合格品
                self.part_1_defect = 0  # 此时次品率为0
                self.settings[0] = 0  # 检测后不再检测
            if self.settings[1] == 1:
                cost_2 += self.part_2 * self.part_2_check * self.settings[1]  # 检测零件2成本
                self.part_2 -= self.part_2 * self.part_2_defect  # 去除不合格品
                self.part_2_defect = 0  # 此时次品率为0
                self.settings[1] = 0  # 检测后不再检测

            # 组装：
            self.product = min(self.part_1, self.part_2)
            self.part_1 -= self.product
            self.part_2 -= self.product
            cost_product = self.product * self.product_price  # 组装成本

            # 两个零件同时为正品的概率：
            correct_rate = (1 - self.part_1_defect) * (1 - self.part_2_defect)

            # 综合次品率
            defect_rate = 1 - correct_rate * (1 - self.product_assemble_defect_rate)
            # print("综合次品率： ", defect_rate)

            # 不合格品的个数：
            defect_product = self.product * defect_rate

            # 是否检测成品
            if self.settings[2] == 1:
                #  对所有产品进行检测
                defect_cost += self.product_check * self.product  # 检测全部产品所产生的费用
                self.product -= defect_product  # 检测后正常的产品
            else:
                # 不合格品的调换成本：
                defect_cost += defect_product * self.product_return  # 调换成本
                self.product -= defect_product  # 调换后还需补上正常的产品

            # 不合格品拆解成本
            if self.settings[3] == 1:
                defect_cost += defect_product * self.product_dismantle  # 拆解成本
                self.part_1 += defect_product  # 拆解后需要重新生产
                self.part_2 += defect_product
            # 不论如何，不合格品数目最后会变为0

            total_product += self.product  # 统计总产品数
            self.product = 0

        # 综合利润：
        self.score += total_product * self.product_sell - cost_1 - cost_2 - cost_product - defect_cost

        return self.score
