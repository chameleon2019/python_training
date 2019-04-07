import re
from lxml import etree
from bs4 import BeautifulSoup
class MyTopicCli:
    needed_products = ['PTN90X', 'PTN9X0', 'PTN7900']
    def __init__(self):
        self.xml_tree = None

    def generate_cli_topic_from_omsys_cli(self, omsys_cli, language="zh-cn"):
        self.generate_cli_topic()
        self.generate_cli_topic_general(omsys_cli.id, language, omsys_cli.cli_name)
        self.generate_cli_topic_parameters(omsys_cli.parameters)
        self.generate_cli_topic_clifunc(omsys_cli.cli_description)
        self.generate_cli_topic_format(omsys_cli.cmd_lines)

        self.generate_cli_topic_views(omsys_cli.views)
        self.generate_cli_topic_levels(omsys_cli.default_levels)
        self.generate_cli_topic_task(omsys_cli.tasks)
        self.generate_cli_topic_cli_desc(omsys_cli.cli_desc, omsys_cli.pre_condition, omsys_cli.config_mode,
                                         omsys_cli.config_effect, omsys_cli.mission, omsys_cli.attention)
        self.generate_cli_topic_example(omsys_cli.example_cns)

    def __str__(self):
        object_desc = '---------------------------new_to_str------------------------------'
        for name, value in vars(self).items():
            object_desc += '\n' + '%s=%s' % (name, value)
        object_desc += '\n' + '---------------------------new_to_str_end-----------------------------'
        return object_desc

    @staticmethod
    def is_ptn_products(products):
        new_products = [x for x in MyTopicCli.needed_products if x in products]
        return new_products

    @staticmethod
    def generate_striped_strings(html_content):
        striped_strings = BeautifulSoup(html_content, "lxml").stripped_strings
        return striped_strings

    # 生成xml基本结构
    def generate_cli_topic(self):
        self.root = etree.Element("cliref")
        self.title = etree.SubElement(self.root, "title")
        self.clirefbody = etree.SubElement(self.root, "clirefbody")
        self.clifunc = etree.SubElement(self.clirefbody, "clifunc")
        self.cliformat = etree.SubElement(self.clirefbody, "cliformat")
        self.cliparam = etree.SubElement(self.clirefbody, "cliparam")
        self.cliview = etree.SubElement(self.clirefbody, "cliview")
        self.clidefaultlevel = etree.SubElement(self.clirefbody, "clidefaultlevel")
        self.clitasknameandoper = etree.SubElement(self.clirefbody, "clitasknameandoper")
        self.clidesc = etree.SubElement(self.clirefbody, "clidesc")
        self.cliexample = etree.SubElement(self.clirefbody, "cliexample")
        self.xml_tree = etree.ElementTree(self.root)

    # 生成除id, title
    def generate_cli_topic_general(self, id, language, title):
        # 设置id
        if isinstance(id, str):
            id = id.strip()
            self.root.set("id", id)
        else:
            error_message = "id不是字符串类型，请检查" + str(id)
            return False, error_message
        # 设置xml语言属性
        if isinstance(language, str):
            language = language.strip()
            if language == "zh-cn" or language == "en-us":
                self.root.set("{http://www.w3.org/XML/1998/namespace}lang", language)
                self.language = language
            else:
                error_message = "Topic语言设置有误，请检查：" + str(language)
                return False, error_message
        else:
            error_message = "语言不是字符串类型，请检查" + str(language)
            return False, error_message
        # 设置space属性
        self.root.set("{http://www.w3.org/XML/1998/namespace}space", "default")
        # 设置title
        if isinstance(title, str):
            title = title.strip()
            self.title.text = title
            self.name = title
        else:
            error_message = "title不是字符串类型，请检查" + str(title)
            return False, error_message
        return True, self.xml_tree

    # 生成cli功能描述
    def generate_cli_topic_clifunc(self, clifunc_str):
        if isinstance(clifunc_str, str):
            clifunc_strs = self.generate_striped_strings(clifunc_str)
            for item in clifunc_strs:
                element = etree.SubElement(self.clifunc, "p")
                element.text = item.strip()
            return True, self.clifunc
        else:
            error_message = "clifunc_str不是字符串类型，请检查" + str(clifunc_str)
            return False, error_message

    # 生成命令行格式
    def generate_cli_topic_format(self, omsys_cli_formats):
        for each_cli_format in omsys_cli_formats:
            cmd_line = each_cli_format[0]
            cmd_line_products = each_cli_format[2].strip().split(",")
            processed_products = self.is_ptn_products(cmd_line_products)
            # print(processed_products)
            if len(processed_products) > 0:
                cmd = self.generate_cmdline_from_omsys(cmd_line)
                self.cliformat.insert(len(self.cliformat), etree.XML(cmd))

    # 生成命令行参数
    def generate_cli_topic_parameters(self, omsys_cli_parameters):
        self.has_parameter = 0
        for item in omsys_cli_parameters:
            if item[5] == 'parameter':
                products = item[4].strip()
                processed_products = self.is_ptn_products(products)
                if len(processed_products) > 0:
                    self.has_parameter += 1
                    parameter_name = item[1].strip()[1:-1]
                    parameter_desc_zh = item[2]
                    parameter_desc_en = item[3]
                    parameter_type = item[6]
                    parameter_range = item[7]
                    if self.has_parameter == 1:
                        self.parameters = etree.SubElement(self.cliparam, "parameters")
                        self.cliparamhead = etree.SubElement(self.parameters, "cliparamhead")
                        element = etree.SubElement(self.cliparamhead, "cliparamnamehd")
                        element = etree.SubElement(self.cliparamhead, "cliparamdeschd")
                        element = etree.SubElement(self.cliparamhead, "cliparamvaluehd")
                    cliparameter = etree.SubElement(self.parameters, "cliparameter")
                    cliparamname = etree.SubElement(cliparameter, "cliparamname")
                    varname = etree.SubElement(cliparamname, "varname")
                    varname.text = parameter_name
                    cliparamdesc = etree.SubElement(cliparameter, "cliparamdesc")
                    if self.language == "zh-cn":
                        cliparamdesc.text = parameter_desc_zh
                    elif self.language == "en-us":
                        cliparamdesc.text = parameter_desc_en
                    cliparamvalue = etree.SubElement(cliparameter, "cliparamvalue")
                    cliparamvalue.text = parameter_range
                # print(products,parameter_name,parameter_desc_zh,parameter_desc_en, parameter_type,parameter_range)

    # 生成命令行视图
    def generate_cli_topic_views(self, views):
        if len(views) > 0:
            for view in views:
                view_content_zh = view[0].strip()
                view_content_en = view[1].strip()
                view_products = view[2].strip().split(',')
                processed_products = self.is_ptn_products(view_products)
                if len(processed_products) > 0:
                    element = etree.SubElement(self.cliview, 'p')
                    if self.language == "zh-cn":
                        element.text = view_content_zh
                    elif self.language == "en-us":
                        element.text = view_content_en

    # 生成命令行级别
    def generate_cli_topic_levels(self, default_levels):
        if len(default_levels) > 0:
            for level in default_levels:
                level_content = level[0].strip()
                level_products = level[1].strip().split(',')
                processed_products = self.is_ptn_products(level_products)
                if len(processed_products) > 0:
                    element = etree.SubElement(self.clidefaultlevel, 'p')
                    if self.language == "zh-cn":
                        element.text = level_content
                    elif self.language == "en-us":
                        element.text = level_content
    # 生成任务
    def generate_cli_topic_task(self, task):
        if len(task) == 1:
            clitasknameandoperations = etree.SubElement(self.clitasknameandoper, 'clitasknameandoperations')
            clitasknameandoperhead = etree.SubElement(clitasknameandoperations, 'clitasknameandoperhead')
            clitasknamehd = etree.SubElement(clitasknameandoperhead, 'clitasknamehd')
            clioperationshd = etree.SubElement(clitasknameandoperhead, 'clioperationshd')
            clitasknameandoperbody = etree.SubElement(clitasknameandoperations, 'clitasknameandoperbody')
            self.clitaskname = etree.SubElement(clitasknameandoperbody, 'clitaskname')
            self.clitaskname.text = task[0][0]
            self.clioperations = etree.SubElement(clitasknameandoperbody, 'clioperations')
            self.clioperations.text = task[0][1]

    # 生成cli描述
    def generate_cli_topic_cli_desc(self, cli_desc, pre_condition, config_mode, config_effect, mission, attention):
        if isinstance(cli_desc, str) and cli_desc.strip() != "":
            cli_descs = self.generate_striped_strings(cli_desc)
            clidesc_title = etree.SubElement(self.clidesc, "p")
            clidesc_title_b = etree.SubElement(clidesc_title, "b")
            if self.language == "zh-cn":
                clidesc_title_b.text = "使用场景"
            elif self.language == "en-us":
                clidesc_title_b.text = "Usage Scenario"
            for item in cli_descs:
                element = etree.SubElement(self.clidesc, "p")
                element.text = item.strip()
        else:
            error_message = "cli_desc不是字符串类型，请检查" + str(cli_desc)
            return False, error_message

        if isinstance(pre_condition, str) and pre_condition.strip() != "":
            print("pre_condition"+"非空"+pre_condition)

        if isinstance(config_mode, str) and config_mode.strip() != "":
            print("config_mode"+"非空"+config_mode)

        if isinstance(config_effect, str) and config_effect.strip() != "":
            print("config_effect"+"非空"+config_effect)

        if isinstance(mission, str) and mission.strip() != "":
            print("mission"+"非空"+mission)

        if isinstance(attention, str) and attention.strip() != "":
            attentions = self.generate_striped_strings(attention)
            attention_title = etree.SubElement(self.clidesc, "p")
            attention_title_b = etree.SubElement(attention_title, "b")
            if self.language == "zh-cn":
                attention_title_b.text = "注意事项"
            elif self.language == "en-us":
                attention_title_b.text = "Attention"
            for item in attentions:
                element = etree.SubElement(self.clidesc, "p")
                element.text = item.strip()
        return True, self.clidesc

    # 生成命令行屏显
    def generate_cli_topic_example(self, examples):
        if len(examples) > 0:
            for example in examples:
                example_content = example[0]
                example_products = example[1].strip().split(',')
                processed_products = self.is_ptn_products(example_products)
                # print(processed_products)
                if len(processed_products) > 0:
                    example_contents = self.generate_striped_strings(example_content)
                    for item in example_contents:
                        item = item.strip()
                        if item.startswith("#"):
                            element = etree.SubElement(self.cliexample, "p")
                            element.text = item
                        else:
                            element = etree.SubElement(self.cliexample, "screen")
                            element.text = item
    # 保存到文件
    def save_to_xml(self, xml_topic_name):
        self.xml_tree.write(xml_topic_name, pretty_print=True, encoding='utf-8')


    @staticmethod
    def generate_cmdline_from_omsys(omsys_cli):
        str_initial = omsys_cli.strip().split(" ")
        str_initial_len = len(str_initial)
        # 给定初始结果
        str_result = ""
        con_flag = str_initial_len
        # 寻找第一个分割符号或尖括号，如果找到符号或参数，记录下来，准备下一步生成cmdname部分
        for i in range(0, str_initial_len):
            if str_initial[i] == "{" or str_initial[i] == "|" or str_initial[i] == "}" or str_initial[i] == "[" or \
                            str_initial[i] == "]" or str_initial[i].startswith("<"):
                con_flag = i
                break
        for k in range(0, con_flag):
            if k == 0:
                str_result = r'(cmdname)' + str_initial[k] + " "
            elif not k == con_flag - 1:
                str_result = str_result + str_initial[k] + " "
            else:
                str_result = str_result + str_initial[k] + r'(/cmdname)'
        for j in range(con_flag, str_initial_len):
            if str_initial[j] == "{" or str_initial[j] == "|" or str_initial[j] == "}" or str_initial[j] == "[" or \
                            str_initial[j] == "]":
                str_result = str_result + " " + str_initial[j]
            elif str_initial[j].startswith("<") and str_initial[j].endswith(">"):
                getdata = re.compile(r'[<](.*?)[>]', re.S)
                real_str = re.findall(getdata, str_initial[j])[0]
                # print(real_str)
                new_str = r'(varname)' + real_str + r'(/varname)'
                str_result = str_result + " " + new_str
            else:
                new_str = r'(cmdparmname)' + str_initial[j] + r'(/cmdparmname)'
                str_result = str_result + " " + new_str
        str_result = str_result.replace('(', '<')
        str_result = str_result.replace(')', '>')
        return "<p>" + str_result + "</p>"