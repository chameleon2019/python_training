# 打印TopicAlarm信息
from bs4 import BeautifulSoup
class OmsysCommon:
    needed_products = ['PTN90X', 'PTN9X0', 'PTN7900']
    def __str__(self):
        object_desc = '---------------------------new_to_str------------------------------'
        for name, value in vars(self).items():
            object_desc += '\n' + '%s=%s' % (name, value)
        object_desc += '\n' + '---------------------------new_to_str_end-----------------------------'
        return object_desc
    # 判断是否是PTN产品，返回一个数组，数组中是产品过滤后的产品名
    @staticmethod
    def is_ptn_products(products):
        new_products = [x for x in OmsysCommon.needed_products if x in products]
        return new_products
    # 从HTML中获取可换行的文本
    @staticmethod
    def generate_striped_strings(html_content):
        striped_strings = BeautifulSoup(html_content, "lxml").stripped_strings
        return striped_strings