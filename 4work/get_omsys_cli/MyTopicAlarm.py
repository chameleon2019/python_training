import re
from lxml import etree
from OmsysCommon import OmsysCommon
class MyTopicAlarm:

    def __init__(self):
        self.xml_tree = None

    def generate_alarm_topic_from_omsys_cli(self, omsys_cli, language="zh-cn"):
        # 生成alarm topic基本结构
        generate_alarm_topic_result, info = self.generate_alarm_topic()
        if not generate_alarm_topic_result:
            return False, info
        # 根据语言生成id, 标题
        generate_alarm_topic_general_result, info = self.generate_alarm_topic_general(omsys_cli.id, language, omsys_cli.title_zh, omsys_cli.title_en)
        if not generate_alarm_topic_general_result:
            return False, info
        # 生成告警解释
        generate_alarm_topic_alarmdesc_result, info = self.generate_alarm_topic_alarmdesc(omsys_cli.alarmdesc)
        if not generate_alarm_topic_alarmdesc_result:
            return False, info
        # 生成告警ID，分类，级别
        generate_alarm_topic_alarmattr_result, info = self.generate_alarm_topic_alarmattr(omsys_cli.alarm_id, omsys_cli.alarm_severity, omsys_cli.alarm_type, language)
        if not generate_alarm_topic_alarmattr_result:
            return False, info
        # 生成参数

        # self.generate_alarm_topic_views(omsys_cli.views)
        # self.generate_alarm_topic_levels(omsys_cli.default_levels)
        # self.generate_alarm_topic_task(omsys_cli.tasks)
        # self.generate_alarm_topic_cli_desc(omsys_cli.cli_desc, omsys_cli.pre_condition, omsys_cli.config_mode,
        #                                  omsys_cli.config_effect, omsys_cli.mission, omsys_cli.attention)
        # self.generate_alarm_topic_example(omsys_cli.example_cns)

    # 生成xml基本结构--OK
    def generate_alarm_topic(self):
        try:
            self.root = etree.Element("alarmref")
            self.title = etree.SubElement(self.root, "title")
            self.alarmrefbody = etree.SubElement(self.root, "alarmrefbody")
            self.alarmdesc = etree.SubElement(self.alarmrefbody, "alarmdesc")
            self.alarmattrs = etree.SubElement(self.alarmrefbody, "alarmattrs")
            alarmattrhead = etree.SubElement(self.alarmattrs, "alarmattrhead")
            alarmattridhead = etree.SubElement(alarmattrhead, "alarmattridhead")
            alarmattrseverityhead = etree.SubElement(alarmattrhead, "alarmattrseverityhead")
            alarmattrtypehead = etree.SubElement(alarmattrhead, "alarmattrtypehead")
            self.alarmattr = etree.SubElement(self.alarmattrs, "alarmattr")
            self.alarmattrid = etree.SubElement(self.alarmattr, "alarmattrid")
            self.alarmattrseverity = etree.SubElement(self.alarmattr, "alarmattrseverity")
            self.alarmattrtype = etree.SubElement(self.alarmattr, "alarmattrtype")
            self.alarmparameters = etree.SubElement(self.alarmrefbody, "alarmparameters")
            self.impactonsystem = etree.SubElement(self.alarmrefbody, "impactonsystem")
            self.possiblecauses = etree.SubElement(self.alarmrefbody, "possiblecauses")
            self.alarmhandlingunordered = etree.SubElement(self.alarmrefbody, "alarmhandling-unordered")
            self.xml_tree = etree.ElementTree(self.root)
        except Exception as e:
            error_message = "创建topic基本结构失败：" + str(e)
            return False, error_message
        return True, self.xml_tree

    # 生成除id, title--OK
    def generate_alarm_topic_general(self, id, language, title_zh, title_en):
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
        # # 设置space属性
        # self.root.set("{http://www.w3.org/XML/1998/namespace}space", "default")
        # 设置title
        if language == "zh-cn":
            title = title_zh
        elif language == "en-us":
            title = title_en
        else:
            error_message = language + "不正确"
            return False, error_message
        if isinstance(title, str):
            title = title.strip()
            self.title.text = title
            self.name = title
        else:
            error_message = "title不是字符串类型，请检查" + str(title)
            return False, error_message
        return True, self.xml_tree

    # 生成Alarm功能描述--OK
    def generate_alarm_topic_alarmdesc(self, alarmdesc_str):
        if isinstance(alarmdesc_str, str):
            element = etree.SubElement(self.alarmdesc, "p")
            element.text = alarmdesc_str.strip()
            return True, self.alarmdesc
        else:
            error_message = "alarmdesc_str不是字符串类型，请检查" + str(alarmdesc_str)
            return False, error_message

    # 生成alarm属性--OK
    def generate_alarm_topic_alarmattr(self, alarm_id_str, alarm_severity_str, alarm_type_str, language):
        severity_map = {
            "紧急": "Critical",
            "重要": "Major",
            "次要": "Minor",
            "提示": "Warning"
        }

        alarm_type_map = {
            "通信告警": "Communications alarm",
            "业务质量告警": "Quality Of Service alarm",
            "处理错误告警": "Processing error alarm",
            "设备告警": "Equipment alarm",
            "环境告警": "Environmental alarm"
        }
        if isinstance(alarm_id_str, str):
            element = etree.SubElement(self.alarmattrid, "p")
            element.text = alarm_id_str.strip()
        else:
            error_message = "alarm_id_str不是字符串类型，请检查" + str(alarm_id_str)
            return False, error_message

        if isinstance(alarm_severity_str, str):
            element = etree.SubElement(self.alarmattrseverity, "p")
            element.text = alarm_severity_str.strip()
            if language == "en-us":
                element.text = severity_map[element.text]
        else:
            error_message = "alarm_severity_str不是字符串类型，请检查" + str(alarm_severity_str)
            return False, error_message

        if isinstance(alarm_type_str, str):
            element = etree.SubElement(self.alarmattrtype, "p")
            element.text = alarm_type_str.strip()
            if language == "en-us":
                element.text = alarm_type_map[element.text]
        else:
            error_message = "alarm_type_str不是字符串类型，请检查" + str(alarm_type_str)
            return False, error_message

        return True, self.alarmattr




    # 打印TopicAlarm信息
    def __str__(self):
        object_desc = '---------------------------new_to_str------------------------------'
        for name, value in vars(self).items():
            object_desc += '\n' + '%s=%s' % (name, value)
        object_desc += '\n' + '---------------------------new_to_str_end-----------------------------'
        return object_desc