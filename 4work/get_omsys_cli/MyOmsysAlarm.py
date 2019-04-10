
from lxml import etree
import logging
class MyOmsysAlarm():
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
        # 获取alarm_mnemonic
        alarm_mnemonic_xpath_rule = '//alarm_mnemonic'
        alarm_mnemonics = self.xml_tree.xpath(alarm_mnemonic_xpath_rule)
        if len(alarm_mnemonics) > 1:
            for item_index in range(1,len(alarm_mnemonics)):
                if alarm_mnemonics[item_index].text != alarm_mnemonics[item_index-1].text:
                    error_message = "存在多个不同助记符，请检查：" + self.ori_filepath
                    return False, error_message
            self.alarm_mnemonic = alarm_mnemonics[0].text
        elif len(alarm_mnemonics) == 1:
            self.alarm_mnemonic = alarm_mnemonics[0].text
        else:
            error_message = "不存在助记符，请检查"
            return False, error_message

        # 获取alarm_name_en
        alarm_name_xpath_rule = '//alarm_name_en'
        alarm_names = self.xml_tree.xpath(alarm_name_xpath_rule)
        if len(alarm_names) > 1:
            for item_index in range(1,len(alarm_names)):
                if alarm_names[item_index].text != alarm_names[item_index-1].text:
                    error_message = "存在多个不同告警名称，请检查：" + self.ori_filepath
                    return False, error_message
            self.alarm_name = alarm_names[0].text
        elif len(alarm_names) == 1:
            self.alarm_name = alarm_names[0].text
        else:
            error_message = "不存在告警名称，请检查"
            return False, error_message

        # 获取trap_descr_en
        trap_descr_en_xpath_rule = '//trap_descr_en'
        trap_descr_ens = self.xml_tree.xpath(trap_descr_en_xpath_rule)
        if len(trap_descr_ens) > 1:
            for item_index in range(1,len(trap_descr_ens)):
                if trap_descr_ens[item_index].text != trap_descr_ens[item_index-1].text:
                    error_message = "存在多个不同告警解释-英文，请检查：" + self.ori_filepath
                    return False, error_message
            self.trap_descr_en = trap_descr_ens[0].text
        elif len(trap_descr_ens) == 1:
            self.trap_descr_en = trap_descr_ens[0].text
        else:
            error_message = "不存在告警解释-英文，请检查"
            return False, error_message

        # 获取trap_descr_zh
        trap_descr_zh_xpath_rule = '//trap_descr_cn'
        trap_descr_zhs = self.xml_tree.xpath(trap_descr_zh_xpath_rule)
        if len(trap_descr_zhs) > 1:
            for item_index in range(1, len(trap_descr_zhs)):
                if trap_descr_zhs[item_index].text != trap_descr_zhs[item_index - 1].text:
                    error_message = "存在多个不同告警解释-中文，请检查：" + self.ori_filepath
                    return False, error_message
            self.trap_descr_zh = trap_descr_zhs[0].text
        elif len(trap_descr_zhs) == 1:
            self.trap_descr_zh = trap_descr_zhs[0].text
        else:
            error_message = "不存在告警解释-中文，请检查"
            return False, error_message

        # 获取alarm_id
        alarm_id_xpath_rule = '//alarm_id'
        alarm_ids = self.xml_tree.xpath(alarm_id_xpath_rule)
        if len(alarm_ids) > 1:
            for item_index in range(1, len(alarm_ids)):
                if alarm_ids[item_index].text != alarm_ids[item_index - 1].text:
                    error_message = "存在多个不同告警ID，请检查：" + self.ori_filepath
                    return False, error_message
            alarm_id = alarm_ids[0].text[2:].lstrip('0')
        elif len(alarm_ids) == 1:
            alarm_id = alarm_ids[0].text[2:].lstrip('0')
        else:
            error_message = "不存在告警ID，请检查"
            return False, error_message
        self.alarm_id = int(alarm_id, 16)

        # 获取event_type
        event_type_xpath_rule = '//event_type'
        event_types = self.xml_tree.xpath(event_type_xpath_rule)
        if len(event_types) > 1:
            for item_index in range(1, len(event_types)):
                if event_types[item_index].text != event_types[item_index - 1].text:
                    error_message = "存在多个不同告警类型，请检查：" + self.ori_filepath
                    return False, error_message
            event_type = event_types[0].text
        elif len(event_types) == 1:
            event_type = event_types[0].text
        else:
            error_message = "不存在告警类型，请检查"
            return False, error_message
        self.event_type = int(event_type)

        # 获取alarm_level
        alarm_level_xpath_rule = '//alarm_level'
        alarm_levels = self.xml_tree.xpath(alarm_level_xpath_rule)
        if len(alarm_levels) > 1:
            for item_index in range(1, len(alarm_levels)):
                if alarm_levels[item_index].text != alarm_levels[item_index - 1].text:
                    error_message = "存在多个不同告警级别，请检查：" + self.ori_filepath
                    return False, error_message
            alarm_level = alarm_levels[0].text
        elif len(alarm_levels) == 1:
            alarm_level = alarm_levels[0].text
        else:
            error_message = "不存在告警级别，请检查"
            return False, error_message
        self.alarm_level = int(alarm_level)

        # 获取alarm_para_info
        para_info_xpath_rule = '//alarm_para_info/para_info'
        para_infos = self.xml_tree.xpath(para_info_xpath_rule)
        parameters = []
        if len(para_infos) > 0:
            for item_index in range(0, len(para_infos)):
                parameter_index = para_infos[item_index].xpath("pa_index")[0].text
                parameter_name = para_infos[item_index].xpath("pa_name")[0].text
                parameter_info_data = para_infos[item_index].xpath("pa_info_data")[0].text
                parameter_info_data_en = para_infos[item_index].xpath("pa_info_data_en")[0].text
                parameter = [parameter_index, parameter_name, parameter_info_data, parameter_info_data_en]
                parameters.append(parameter)
        else:
            error_message = "不存在参数，请检查"
            return False, error_message
        self.parameters = parameters
        # print(self.parameters)
        # 获取itut_para_sequence，获取parameters
        itut_para_sequence_xpath_rule = '//itut_para_sequence'
        itut_para_sequences = self.xml_tree.xpath(itut_para_sequence_xpath_rule)
        # print(itut_para_sequences)
        if len(itut_para_sequences) > 1:
            for item_index in range(1, len(itut_para_sequences)):
                if itut_para_sequences[item_index].text != itut_para_sequences[item_index - 1].text:
                    error_message = "存在多个不同网管上报参数，请检查：" + self.ori_filepath
                    return False, error_message
            itut_para_sequence = itut_para_sequences[0].text
        elif len(itut_para_sequences) == 1:
            itut_para_sequence = itut_para_sequences[0].text
        else:
            error_message = "不存在网管上报参数，请检查"
            return False, error_message
        self.itut_para_sequence_list = itut_para_sequence.split("$")[1:]
        needed_parameters_zh = []
        needed_parameters_en = []
        item_index = 0
        for item in self.itut_para_sequence_list:
            item = item[1:-1]
            item_index += 1
            find_parameter_result, parameter_info_zh, parameter_info_en = self.get_parameter_info_from_parameters(item)
            if not find_parameter_result:
                error_message = "查找参数" + item + "失败：" + self.ori_filepath
                return False, error_message
            else:
                needed_parameters_zh.append(parameter_info_zh)
                needed_parameters_en.append(parameter_info_en)
        self.needed_parameters_zh = needed_parameters_zh
        self.needed_parameters_en = needed_parameters_en

        return True, self.xml_tree

    # @staticmethod
    def get_parameter_info_from_parameters(self, parameter_name):
        # print(parameter_name, self.parameters)
        for parameter in self.parameters:
            if parameter[1] == parameter_name:
                parameter_info_zh = parameter[2]
                parameter_info_en = parameter[3]
                return True, parameter_info_zh, parameter_info_en
        return False, None, None


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
