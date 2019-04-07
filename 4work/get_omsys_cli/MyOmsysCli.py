from lxml import etree
import logging
class MyOmsysCli():
    def __init__(self, xml_file):
        self.fix_xml_result = self.fix_xml(xml_file)
        self.process_failed = False
        self.ori_filepath = xml_file
        try:
            self.xml_tree = etree.parse(xml_file)
        except Exception as e:
            error_message = "解析XML失败：" + xml_file + str(e)
            self.process_failed = True
            self.process_failed_reason = error_message
            self.xml_tree = None

    def get_xml_info(self):
        # 获取function_name
        function_name_xpath_rule = '//function_name'
        function_names = self.xml_tree.xpath(function_name_xpath_rule)
        if len(function_names) == 1:
            self.function_name = function_names[0].text
        # 获取cli_name和id
        cli_name_xpath_rule = '//cli_name'
        cli_names = self.xml_tree.xpath(cli_name_xpath_rule)
        if len(cli_names) == 1:
            self.cli_name = cli_names[0].text
            self.id = self.cli_name.replace(" ","_")
        # 获取命令功能
        cli_description_xpath_rule = '//cli_description'
        cli_descriptions = self.xml_tree.xpath(cli_description_xpath_rule)
        if len(cli_descriptions) == 1:
            self.cli_description = cli_descriptions[0].text
        # 获取命令缺省值
        default_config_xpath_rule = '//default_config'
        default_configs = self.xml_tree.xpath(default_config_xpath_rule)
        if len(default_configs) == 1:
            self.default_config = default_configs[0].text
        # 获取视图信息
        view_xpath_rule = '//view'
        views = self.xml_tree.xpath(view_xpath_rule)
        self.views = []
        if len(views) > 0:
            for item in views:
                view_name = item.xpath('view_name')[0].text
                view_name_TDC = item.xpath('view_name_TDC')[0].text
                view_sharp_names = item.xpath('view_sharp_names')[0].text
                self.views.append([view_name, view_name_TDC, view_sharp_names])
        # 获取级别
        default_level_xpath_rule = '//default_level'
        default_levels = self.xml_tree.xpath(default_level_xpath_rule)
        if len(default_levels) == 1:
            self.cli_level = default_levels[0][0].text
        elif len(default_levels) > 1:
            pass
        # 获取使用指南
        cli_desc_xpath_rule = '//clidesc'
        cli_descs = self.xml_tree.xpath(cli_desc_xpath_rule)
        if len(cli_descs) == 1:
            ori_cli_desc = cli_descs[0].text
            self.cli_desc = ori_cli_desc
        # 获取配置使用前事项
        pre_condition_xpath_rule = '//pre_condition'
        pre_conditions = self.xml_tree.xpath(pre_condition_xpath_rule)
        if len(pre_conditions) == 1:
            self.pre_condition = pre_conditions[0].text
        # 获取配置模式
        config_mode_xpath_rule = '//config_mode'
        config_modes = self.xml_tree.xpath(config_mode_xpath_rule)
        if len(config_modes) == 1:
            self.config_mode = config_modes[0].text
        # 获取配置影响
        config_effect_xpath_rule = '//config_effect'
        config_effects = self.xml_tree.xpath(config_effect_xpath_rule)
        if len(config_effects) == 1:
            self.config_effect = config_effects[0].text
        # 获取要执行的任务
        mission_xpath_rule = '//mission'
        missions = self.xml_tree.xpath(mission_xpath_rule)
        if len(missions) == 1:
            # print(type(missions[0].text))
            self.mission = missions[0].text
        # 获取注意事项
        attention_xpath_rule = '//attention'
        attentions = self.xml_tree.xpath(attention_xpath_rule)
        if len(attentions) == 1:
            ori_attention = attentions[0].text
            self.attention = ori_attention
        # 获取命令行
        cmd_line_xpath_rule = '//cl'
        cmd_lines = self.xml_tree.xpath(cmd_line_xpath_rule)
        self.cmd_lines = []
        if len(cmd_lines)>0:
            for item in cmd_lines:
                cmd_line = item.xpath('cl_content')[0].text
                cmd_line_mode = item.xpath('cl_mode')[0].text
                cmd_line_products = item.xpath('cl_sharp_names')[0].text
                self.cmd_lines.append([cmd_line, cmd_line_mode, cmd_line_products])
        # 获取参数
        parameter_xpath_rule = '//keyword'
        parameters = self.xml_tree.xpath(parameter_xpath_rule)
        self.parameters = []
        if len(parameters) > 0:
            for item in parameters:
                kw_index = item.xpath('kw_index')[0].text
                kw_name = item.xpath('kw_name')[0].text
                kw_cnhelp = item.xpath('kw_cnhelp')[0].text
                kw_enhelp = item.xpath('kw_enhelp')[0].text
                kw_sharp_names = item.xpath('kw_sharp_names')[0].text
                if kw_name.startswith("<"):
                    kw_type = 'parameter'
                    kw_ptype = item.xpath('kw_ptype')[0].text
                    kw_prange = item.xpath('kw_prange')[0].text
                    kw = [kw_index, kw_name, kw_cnhelp, kw_enhelp, kw_sharp_names, kw_type, kw_ptype, kw_prange]
                else:
                    kw_type = 'keyword'
                    kw = [kw_index, kw_name, kw_cnhelp, kw_enhelp, kw_sharp_names, kw_type]
                self.parameters.append(kw)
        # auto_calculate_default_levels
        auto_calculate_default_level_xpath_rule = '//auto_calculate_default_levels/default_level'
        auto_calculate_default_levels = self.xml_tree.xpath(auto_calculate_default_level_xpath_rule)
        self.auto_calculate_default_levels = []
        if len(auto_calculate_default_levels) > 0:
            for item in auto_calculate_default_levels:
                level = item.xpath('level')[0].text
                product_names = item.xpath('product_names')[0].text
                self.auto_calculate_default_levels.append([level, product_names])

        # 获取default_levels
        default_level_xpath_rule = '//default_levels/default_level'
        default_levels = self.xml_tree.xpath(default_level_xpath_rule)
        self.default_levels = []
        if len(default_levels) > 0:
            for item in default_levels:
                level = item.xpath('level')[0].text
                product_names = item.xpath('product_names')[0].text
                self.default_levels.append([level, product_names])

        # 获取任务
        task_xpath_rule = '//task'
        tasks = self.xml_tree.xpath(task_xpath_rule)
        self.tasks = []
        if len(tasks) > 0:
            for item in tasks:
                taks_name = item.xpath('task_name')[0].text
                option = item.xpath('option')[0].text
                self.tasks.append([taks_name, option])

        # 获取举例
        example_cn_xpath_rule = '//example_cn'
        example_cns = self.xml_tree.xpath(example_cn_xpath_rule)
        self.example_cns = []
        if len(example_cns) > 0:
            for item in example_cns:
                ex_content_cn = item.xpath('ex_content_cn')[0].text
                sharp_names = item.xpath('sharp_names')[0].text
                self.example_cns.append([ex_content_cn, sharp_names])
    def __str__(self):
        object_desc = '---------------------------new_to_str------------------------------'
        for name, value in vars(self).items():
            object_desc += '\n' + '%s=%s' % (name, value)
        object_desc += '\n' + '---------------------------new_to_str_end-----------------------------'
        return object_desc

    # 修改实体引用为文本
    @staticmethod
    def fix_xml(file):
        replace_entity = [
            ['&nbsp;', ' '],
        ]
        file_data1 = ""
        file_data2 = ""
        # print("准备打开",file)
        with open(file, "r", encoding="utf-8") as f:
            for line in f.readlines():
                file_data1 += line
                for each_entity in replace_entity:
                    line = line.replace(each_entity[0], each_entity[1])
                file_data2 += line
        if file_data1 == file_data2:
            f.close()
            return 0
        else:
            try:
                with open(file, "w", encoding="utf-8") as f:
                    f.write(file_data2)
                    f.close()
                return 1
            except Exception as e:
                error_message = '处理失败：'+ file + str(e)
                logging.error(error_message)
                return 2
