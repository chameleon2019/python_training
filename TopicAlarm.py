from lxml import etree
import bs4
from bs4 import BeautifulSoup
import logging, os
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT, filename=r'D:\Actions\Test_Enviroment\python_Work\ptn_info_tools\alarm_to_omsys\log.log')

class TopicAlarm:
    def __init__(self, topic_path, language, type):
        self.topic_path = topic_path
        if os.path.exists(self.topic_path):
            self.file_exist = True
        else:
            self.file_exist = False
        self.language = language
        if type == "xml":
            self.create_topic_alarm_xml()
        elif type == "html":
            self.create_topic_alarm_html()

    def __str__(self):
        for item in self.__dict__:
            logging.info(item)
        # return str(self.__dict__)
        # new_str = ''
        # for item in TopicAlarm.attrs:
        #     logging.info(item)

    def create_topic_alarm_html(self):
        pass

    @staticmethod
    def get_p_content(element, language, is_cause=False, get_p_content_debug= False):
        element_contents = element.contents
        if get_p_content_debug:
            if len(element_contents) > 1:
                logging.info("长度" + str(len(element_contents)))
        element_text = ''
        multiple = 0
        for sub_element in element_contents:
            if sub_element != None:
                sub_element_tag = sub_element.name
                if sub_element_tag != None:
                    if sub_element_tag == 'parmvalue':
                        if language == "zh":
                            element_text += '“' + sub_element.string + '”'
                        else:
                            element_text += '"' + sub_element.string + '"'
                    elif sub_element_tag == 'parmvalue' or sub_element_tag == 'parmname':
                        if language == "zh":
                            element_text += '“' + sub_element.string + '”'
                        else:
                            element_text += '"' + sub_element.string + '"'
                    elif sub_element_tag == 'ph':
                        element_text += sub_element.string
                    elif sub_element_tag == 'ul':
                        if multiple > 0:
                            element_text += '\n' + TopicAlarm.get_ul_content(sub_element, language)
                        else:
                            element_text += TopicAlarm.get_ul_content(sub_element, language)
                        multiple += 1
                    else:
                        logging.error("not parmvalue")
                        logging.error(sub_element)
                else:
                    element_text += sub_element
        if is_cause:
            if language == "zh":
                if element_text.startswith("原因"):
                    co_index =element_text.find("：")
                    element_text = element_text[co_index+1:]
            elif language == 'en':
                if element_text.startswith("Cause"):
                    co_index = element_text.find(":")
                    element_text = element_text[co_index+1:]
        return element_text
        # logging.info("element_text: " + element_text)

    @staticmethod
    def get_li_content(element, language, is_cause=False, get_li_content_debug=False):
        element_contents = element.contents
        element_text = ''
        multiple = 0
        for sub_element in element_contents:
            sub_element_tag = sub_element.name

            if sub_element_tag != None:
                if sub_element_tag == 'p':
                    multiple += 1
                    element_text += TopicAlarm.get_p_content(sub_element, language)
                elif sub_element_tag == 'parmvalue' or sub_element_tag == 'parmname':
                    if language == "zh":
                        element_text += '“' + sub_element.string + '”'
                    else:
                        element_text += '"' + sub_element.string + '"'
                elif sub_element_tag == 'ph':
                    element_text += sub_element.string
                elif sub_element_tag == 'ul':
                    if multiple>0:
                        element_text += '\n'+TopicAlarm.get_ul_content(sub_element, language)
                    else:
                        element_text += TopicAlarm.get_ul_content(sub_element, language)
                    multiple += 1
                else:
                    logging.warning(sub_element_tag)
                    logging.error(sub_element)
            else:
                multiple += 1
                element_text += sub_element

        if is_cause:
            if language == "zh":
                if element_text.startswith("原因"):
                    co_index =element_text.find("：")
                    element_text = element_text[co_index+1:]
            elif language == 'en':
                if element_text.startswith("Cause"):
                    co_index = element_text.find(":")
                    element_text = element_text[co_index+1:]
        return element_text

    @staticmethod
    def get_ul_content(element, language, get_ul_content_debug= False):
        element_contents = element.contents
        ul_contents = []
        if get_ul_content_debug:
            pass

        for sub_element in element_contents:
            # logging.info(sub_element)
            sub_element_tag = sub_element.name
            if sub_element_tag != None:
                if sub_element_tag != "li":
                    logging.warning(sub_element)
                else:
                    li_content = TopicAlarm.get_li_content(sub_element, language)
                    ul_contents.append(' - ' + li_content)
            else:
                try:
                    if sub_element.strip() == "":
                        pass
                except:
                    logging.warning(sub_element)
        if len(ul_contents) == 1:
            return ul_contents[0]
        elif len(ul_contents) == 0:
            return ""
        else:
            return '\n'.join(ul_contents)

    @staticmethod
    def get_step_content(element, language, get_step_content_debug = False):
        if element.name != 'step':
            return False
        element_contents = element.contents
        step_contents = []
        for item in element_contents:
            item_tag = item.name
            if item_tag == None:
                pass
            elif item_tag == 'cmd':
                cause = TopicAlarm.get_p_content(item, language)
                # logging.warning(cause)
            elif item_tag == 'substeps':
                for substep in item.contents:
                    substep_tag = substep.name
                    if substep_tag == None:
                        pass
                    elif substep_tag == 'substep':
                        substep_content = TopicAlarm.get_substep_content(substep, language)
                        if substep_content.strip() != '':
                            step_contents.append(substep_content)
                        # logging.error(substep_content)
                    else:
                        # logging.warning(substep)
                        pass
                # logging.warning(item)
                pass
            elif item_tag == 'info':
                logging.error("step中使用了info标记对，请修改")
            else:
                # logging.error(item)
                pass
        return cause, '\n'.join(step_contents)

    @staticmethod
    def get_substep_content(element,language, get_substep_content_debug = False):
        if element.name != 'substep':
            return False
        element_contents = element.contents
        substep_contents = []
        for item in element_contents:
            item_tag = item.name
            if item_tag == None:
                pass
            if item_tag == 'cmd':
                substep_content = TopicAlarm.get_p_content(item, language)
                substep_contents.append(substep_content)
            else:
                pass
        return '\n'.join(substep_contents)

    # 获取告警解释
    def get_alarmdesc_content_xml(self):
        # logging.info(topic_xml)
        alarmdesc = self.topic_xml.find("alarmdesc")
        if alarmdesc != None:
            self.have_alarmdesc_content = True
            alarmdesc_elements = alarmdesc.contents
            alarmdesc_contents = []
            for element in alarmdesc_elements:
                # logging.info(element)
                if element.name != 'p':
                    if element.strip() != "":
                        logging.error(element)
                        logging.error("存在非P标记对")
                else:
                    element_content = self.get_p_content(element, self.language).strip()
                    if element_content != "":
                        alarmdesc_contents.append(element_content)
            if len(alarmdesc_contents) < 1:
                self.alarmdesc_content = ""
            elif len(alarmdesc_contents) == 1:
                self.alarmdesc_content = alarmdesc_contents[0]
            else:
                self.alarmdesc_content = "\n".join(alarmdesc_contents)
        else:
            self.have_alarmdesc_content = False

    # 获取可能的原因
    def get_possiblecauses_content_xml(self):
        self.cause_ids = []
        self.possiblecauses_content = []
        possiblecauses = self.topic_xml.find("possiblecauses")
        try:
            one_id = possiblecauses.attrs['id']
            if one_id != None:
                if one_id.startswith('cause'):
                    cause_id = one_id[5:]
                    self.cause_ids.append(cause_id)
        except:

            if possiblecauses != None:
                self.have_alarmposs_content = True
                self.have_alarmposs_cause_id = False
                possible_causes = possiblecauses.find_all(id=True)
                if len(possible_causes) > 0:
                    for possible_cause in possible_causes:
                        id = possible_cause.attrs['id']
                        if id != None:
                            if id.startswith('cause'):
                                cause_id = id[5:]
                                self.cause_ids.append(cause_id)
                                possible_cause_tag = possible_cause.name
                                if possible_cause_tag == 'p':
                                    cause_content = self.get_p_content(possible_cause, self.language, is_cause=True)
                                    # logging.info(cause_content)
                                elif possible_cause_tag == 'ul':
                                    cause_content = self.get_ul_content(possible_cause, self.language)
                                    # logging.info(cause_content)
                                elif possible_cause_tag == 'li':
                                    cause_content = self.get_li_content(possible_cause, self.language, is_cause=True)
                                    # logging.info(cause_content)
                                else:
                                    logging.error("标签：" + possible_cause.name)
                                    cause_content = 'empty possible_cause'
                                self.possiblecauses_content.append(
                                    {
                                        'cause_id': cause_id,
                                        'cause_content': cause_content,
                                    }
                                )
            else:
                self.have_alarmposs_content = False
        if len(self.cause_ids)<1:
            self.validated_topic = False
            self.not_validated_reason = "不含cause id"

    # 获取对系统的影响
    def get_impactonsystem_content_xml(self):
        # impactonsystem_cause_ids = []
        impactonsystem = self.topic_xml.find("impactonsystem")
        if impactonsystem != None:
            self.have_impactonsystem_content = True
            self.impactonsystem_contents = []
            impactonsystem_causes = impactonsystem.find_all(id=True)
            if len(impactonsystem_causes) > 0:
                for impactonsystem_cause in impactonsystem_causes:
                    id = impactonsystem_cause.attrs['id']
                    if id != None:
                        if id.startswith('cause'):
                            cause_id = id[5:]
                            # self.cause_ids.append(cause_id)
                            # logging.info(cause_id)
                            # impactonsystem_cause_ids.append(cause_id)
                            impactonsystem_cause_tag = impactonsystem_cause.name
                            if impactonsystem_cause_tag == 'p':
                                cause_content = self.get_p_content(impactonsystem_cause, self.language, is_cause=True)
                                # logging.info(cause_content)
                            elif impactonsystem_cause_tag == 'ul':
                                cause_content = self.get_ul_content(impactonsystem_cause, self.language)
                                # logging.info(cause_content)
                            elif impactonsystem_cause_tag == 'li':
                                cause_content = self.get_li_content(impactonsystem_cause, self.language, is_cause=True)
                                # logging.info(cause_content)
                            else:
                                logging.error("标签：" + impactonsystem_cause.name)
                            self.impactonsystem_contents.append(
                                {
                                    'cause_id': cause_id,
                                    'cause_content': cause_content,
                                }
                            )
            else:
                impactonsystem_contents = impactonsystem.contents
                multiple = 0
                element_text = ''
                for element in impactonsystem_contents:
                    element_tag = element.name
                    if element_tag == None:
                        try:
                            if element.strip() == "":
                                pass
                        except:
                            logging.warning(element)
                    else:

                        if element_tag == 'p':
                            element_text += TopicAlarm.get_p_content(element, self.language)
                            multiple +=1
                        elif element_tag == 'ul':
                            element_text += TopicAlarm.get_ul_content(element, self.language)
                            multiple += 1
                        else:
                            logging.warning(element)
                for item in self.cause_ids:
                    cause_id = item
                    self.impactonsystem_contents.append({
                        'cause_id': cause_id,
                        'cause_content': element_text,
                    })
        else:
            logging.error(impactonsystem)
            self.have_impactonsystem_content = False

    # 获取操作步骤
    def get_alarmhandling_content_xml(self):
        alarmhandling_unordered = self.topic_xml.find_all('alarmhandling-unordered')
        alarmhandling_ordered = self.topic_xml.find_all('alarmhandling')
        # 如果是ordered
        if len(alarmhandling_unordered) != 1:
            if len(alarmhandling_ordered) != 1:
                self.successful_parse = False
                self.not_successful_parse_reason = 'alarmhandling和alarmhandling-unordered数量错误'
            else:
                alarmhandlings = alarmhandling_ordered
                self.alarmhandling_type = 'alarmhandling_ordered'
        else:
            if len(alarmhandling_ordered) == 1:
                self.successful_parse = False
                self.not_successful_parse_reason = 'alarmhandling和alarmhandling-unordered数量错误'
            else:
                alarmhandlings = alarmhandling_unordered
                self.alarmhandling_type = 'alarmhandling_unordered'
        if self.successful_parse:
            if len(alarmhandlings)>1:
                self.successful_parse = False
                self.not_successful_parse_reason = 'alarmhandling和alarmhandling-unordered数量错误'
            else:
                self.alarmhandling = alarmhandlings[0]

        if self.successful_parse:
            overall_handling = False
            self.have_alarmhandling_content = True
            self.alarmhandling_contents = []
            try:
                alarmhandling_id = self.alarmhandling.attrs['id']
                if alarmhandling_id != None:
                    if alarmhandling_id.startswith('cause'):
                        cause_id = alarmhandling_id[5:]
                        overall_handling = True
                        all_step_contents = []
                        for step in self.alarmhandling.contents:
                            if step != '\n':
                                cause, step_content = self.get_step_content(step, self.language)
                                all_step_contents.append(cause+'\n'+ step_content)
                        self.alarmhandling_contents.append({
                            'cause_id': cause_id,
                            'alarmhandling': '\n'.join(all_step_contents)
                        })
            except:
                alarmhandling_causes = self.alarmhandling.find_all(id=True)
                if len(alarmhandling_causes) > 0:
                    for alarmhandling_cause in alarmhandling_causes:
                        id = alarmhandling_cause.attrs['id']
                        if id != None:
                            if id.startswith('cause'):
                                cause_id = id[5:]
                                alarmhandling_cause_tag = alarmhandling_cause.name
                                if alarmhandling_cause_tag != 'step':
                                    logging.warning(alarmhandling_cause_tag)
                                else:
                                    cause, step_content = self.get_step_content(alarmhandling_cause, self.language)
                                    # logging.warning(cause+step_content)
                                self.alarmhandling_contents.append({
                                    'cause_id': cause_id,
                                    'alarmhandling': step_content
                                })
                        else:
                            pass

                else:
                    pass


    # 获取参数列表
    def get_parameter_content_xml(self):
        alarmparameters = self.topic_xml.find("alarmparameters")
        if alarmparameters != None:
            self.have_alarmparameters_content = True
            self.alarmparameters_contents = []
            all_alarmparameter = alarmparameters.find_all('alarmparameter')
            # logging.warning(len(all_alarmparameter))
            if len(all_alarmparameter) >0:
                for alarmparameter in all_alarmparameter:
                    alarmparameterdesc = alarmparameter.find('alarmparameterdesc')
                    alarmparameterdesc_content = ''
                    for item in alarmparameterdesc.contents:
                        item_content = self.get_p_content(item, self.language)
                        alarmparameterdesc_content += item_content
                    # logging.info(alarmparameterdesc_content)
                    self.alarmparameters_contents.append(alarmparameterdesc_content)
                    # alarmparameterdesc_content = self.get_p_content(alarmparameterdesc, self.language)
                    # logging.info(alarmparameterdesc_content)
            else:
                if self.language == "zh":
                    self.alarmparameters_contents.append("无。")
                else:
                    self.alarmparameters_contents.append("None.")
        else:
            logging.error(alarmparameters)
            self.have_alarmparameters_content = False

    def create_topic_alarm_xml(self):
        self.topic_xml = BeautifulSoup(open(self.topic_path,'rb'), "xml")
        self.validated_topic = True
        self.successful_parse = True
        if self.topic_xml.find("alarmrefbody") == None:
            self.validated_topic = False
            self.not_validated_reason = '非告警topic'
        if self.validated_topic:
            self.get_alarmdesc_content_xml()
            self.get_possiblecauses_content_xml()
            self.get_impactonsystem_content_xml()
            if len(self.impactonsystem_contents) <1:
                self.successful_parse = False
                self.not_successful_parse_reason = '未获取到对系统的影响'
            elif len(self.impactonsystem_contents) != len(self.cause_ids):
                self.successful_parse = False
                self.not_successful_parse_reason = '对系统的影响中CauseID数量和告警原因的CauseID数量不一致'
            else:
                self.get_alarmhandling_content_xml()
                self.get_parameter_content_xml()