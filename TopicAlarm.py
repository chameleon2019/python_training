from lxml import etree
import logging, os
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT, filename=r'D:\Actions\Test_Enviroment\python_Work\ptn_info_tools\alarm_to_omsys\log.log')

class TopicAlarm:
    def __init__(self, topic_path, language):
        self.topic_path = topic_path
        if os.path.exists(self.topic_path):
            self.file_exist = True
        else:
            self.file_exist = False
        self.language = language
        self.create_topic_alarm()
    @staticmethod
    def getText(elem):
        rc = []
        for node in elem.itertext():
            rc.append(node.strip())
        return ''.join(rc)

    @staticmethod
    def get_text_p(ele):
        ele_children = ele.xpath(".//*")
        ele_children_ph = ele.xpath(".//ph")
        if len(ele_children) == len(ele_children_ph):
            logging.debug("P标记对内都是ph标记对")
            text = TopicAlarm.getText(ele)
            return True, text
        else:
            error_message = "P标记对内有其他标记对"
            return False, error_message


    @staticmethod
    def process_p(ele):
        ele_children = ele.xpath("./*")
        ele_children_p = ele.xpath("./p")
        texts = []
        errors = []
        if len(ele_children) == len(ele_children_p):
            logging.debug("都是P标记对"+str(ele))
            for p in ele_children_p:
                result, text = TopicAlarm.get_text_p(p)
                if result:
                    texts.append(text)
                else:
                    errors.append(text +":" + str(ele_children_p.index(p)))
        else:
            error_message = "此标记对内不是全是p标记对"
            errors.append(error_message)
        if len(errors)>0:
            return False, "\n".join(errors)
        else:
            if len(texts) == 1:
                return True, texts[0]
            else:
                return True, "\n".join(texts)

    def create_topic_alarm(self):
        topic_etree = etree.parse(self.topic_path)
        root = topic_etree.getroot()
        if root.tag != "alarmref":
            logging.error(self.topic_path+" 不是告警文件")
            self.is_alarm_topic = False
        else:
            self.is_alarm_topic = True
            # 获取告警title
            title = topic_etree.xpath("//alarmref/title")
            if len(title) != 1:
                logging.error(self.topic_path+"title个数错误")
            else:
                self.topic_title = title[0].text
                logging.debug(self.topic_title)

            # 获取告警文件alarmrefbody
            alarmrefbody = topic_etree.xpath("//alarmref/alarmrefbody")
            if len(alarmrefbody) != 1:
                not_validated_reason = "alarmrefbody个数错误"
                logging.error(self.topic_path+"alarmrefbody个数错误")
                self.validated = False
                self.not_validated_reason = not_validated_reason
            else:
                alarmrefbody = alarmrefbody[0]

                # 获取告警解释部分
                alarmdesc = alarmrefbody.xpath("alarmdesc")
                if len(alarmdesc) != 1:
                    logging.error(self.topic_path + "alarmdesc个数错误")
                else:
                    alarmdesc = alarmdesc[0]
                    get_alarmdesc_content_result, alarmdesc_content = self.process_p(alarmdesc)
                    if get_alarmdesc_content_result:
                        self.alarmdesc_content = alarmdesc_content
                        if alarmdesc_content.strip() == "":
                            logging.error("告警解释为空：" + self.topic_title)
                    else:
                        logging.error("告警解释解析失败：" + alarmdesc_content)

                # 获取alarmattrs部分，暂时不做
                alarmattrs = alarmrefbody.xpath("alarmattrs")
                if len(alarmattrs) != 1:
                    logging.error(self.topic_path + "alarmattrs个数错误")
                else:
                    alarmattr = alarmattrs[0]



                impactonsystems = alarmrefbody.xpath("impactonsystem")
                self.impactonsystem_content = []
                if len(impactonsystems) != 1:
                    logging.error(self.topic_path + "impactonsystem个数错误")
                else:
                    impactonsystem = impactonsystems[0]
                    impactonsystem_children = impactonsystem.xpath("./*")
                    impactonsystem_children_p = impactonsystem.xpath("./p")
                    impactonsystem_children_ul = impactonsystem.xpath("./ul")
                    if len(impactonsystem_children) == 0:
                        pass
                    else:
                        have_other_elements = False
                        for item in impactonsystem_children:
                            if item.tag not in ['p', 'ul']:
                                logging.error(self.topic_path + "impactonsystem中存在非p/ul标记对，请检查")
                                self.impactonsystem_content = ""
                                have_other_elements = True
                        if have_other_elements:
                            pass
                        else:
                            if len(impactonsystem_children_p) >0 and len(impactonsystem_children_ul)>0:
                                logging.error(self.topic_path + "impactonsystem中存在p和ul标记对混用，请检查")
                            else:
                                if len(impactonsystem_children_p) > 0:
                                    if len(impactonsystem_children_p) == 1:
                                        get_impactonsystem_content_result, impactonsystem_content =  self.get_text_p(impactonsystem_children_p[0])
                                        if get_impactonsystem_content_result:
                                            # self.impactonsystem_content = impactonsystem_content
                                            p_attrs = impactonsystem_children_p[0].items()
                                            for item in p_attrs:
                                                if item[0] == 'id':
                                                    # logging.info(item[1])
                                                    cause_id = item[1][5:]
                                                    # logging.info(cause_id)
                                                    self.impactonsystem_content = {
                                                        'cause_id': cause_id,
                                                        'impactonsystem_content': impactonsystem_content
                                                    }
                                            # (cause_id)
                                        else:
                                            logging.error(impactonsystem_content)
                                    else:
                                        logging.error(self.topic_path + "impactonsystem中存在p标记对超过两个，请检查")
                                elif len(impactonsystem_children_ul)>0:
                                    if len(impactonsystem_children_ul) == 1:
                                        impactonsystem_cause_id = False
                                        impactonsystem_ul_cause_id = False
                                        only_one_cause = False
                                        lis = impactonsystem_children_ul[0].xpath("./li")
                                        # logging.info(len(lis))
                                        ul_attrs = impactonsystem_children_ul[0].items()
                                        impactonsystem_attrs = impactonsystem.items()
                                        for item in impactonsystem_attrs:
                                            if item[0] == 'id':
                                                cause_id = item[1][5:]
                                                impactonsystem_cause_id = True
                                                only_one_cause = True
                                        if not impactonsystem_cause_id:
                                            for item in ul_attrs:
                                                if item[0] == 'id':
                                                    impactonsystem_ul_cause_id = True
                                                    cause_id = item[1][5:]
                                                    only_one_cause = True
                                                # 后面获取内容都是某个cause的
                                        impactonsystem_contents = []
                                        for li in lis:
                                            get_impactonsystem_content_result, impactonsystem_content = self.get_text_p(li)
                                            logging.info(impactonsystem_content)
                                            if not get_impactonsystem_content_result:
                                                logging.error(impactonsystem_content)
                                            else:
                                                if not only_one_cause:
                                                    li_attrs = li.items()
                                                    for item in li_attrs:
                                                        if item[0] == 'id':
                                                            cause_id = item[1][5:]
                                                            self.impactonsystem_content.append(
                                                                {
                                                                    'cause_id': cause_id,
                                                                    'impactonsystem_content': impactonsystem_content
                                                                }
                                                            )
                                                        else:
                                                            logging.error(self.topic_path + "impactonsystem的ul标记对中，有li未标记cause")
                                                else:
                                                    impactonsystem_contents.append(impactonsystem_content)

                                        if only_one_cause:
                                            self.impactonsystem_content = {
                                                'cause_id': cause_id,
                                                'impactonsystem_content': '\n'.join(impactonsystem_contents)
                                            }



                possiblecausess = alarmrefbody.xpath("possiblecauses")
                self.possiblecauses_content = []
                if len(possiblecausess) != 1:
                    logging.error(self.topic_path + "possiblecauses个数错误")
                else:
                    possiblecauses = possiblecausess[0]
                    possiblecauses_children = possiblecauses.xpath("./*")
                    possiblecauses_children_p = possiblecauses.xpath("./p")
                    possiblecauses_children_ul = possiblecauses.xpath("./ul")
                    if len(possiblecauses_children) == 0:
                        pass
                    else:
                        have_other_elements = False
                        for item in possiblecauses_children:
                            if item.tag not in ['p', 'ul']:
                                logging.error(
                                    self.topic_path + "possiblecauses中存在非p/ul标记对，请检查")
                                self.possiblecauses_content = ""
                                have_other_elements = True
                        if have_other_elements:
                            pass
                        else:
                            if len(possiblecauses_children_p) > 0 and len(
                                    possiblecauses_children_ul) > 0:
                                logging.error(
                                    self.topic_path + "possiblecauses中存在p和ul标记对混用，请检查")
                            else:
                                if len(possiblecauses_children_p) > 0:
                                    if len(possiblecauses_children_p) == 1:
                                        get_possiblecauses_content_result, possiblecauses_content = self.get_text_p(
                                            possiblecauses_children_p[0])
                                        if get_possiblecauses_content_result:
                                            # self.possiblecauses_content = possiblecauses_content
                                            p_attrs = possiblecauses_children_p[0].items()
                                            for item in p_attrs:
                                                if item[0] == 'id':
                                                    # logging.info(item[1])
                                                    cause_id = item[1][5:]
                                                    # logging.info(cause_id)
                                                    self.possiblecauses_content = {
                                                        'cause_id': cause_id,
                                                        'possiblecauses_content': possiblecauses_content
                                                    }
                                                    # (cause_id)
                                        else:
                                            logging.error(possiblecauses_content)
                                    else:
                                        logging.error(
                                            self.topic_path + "possiblecauses中存在p标记对超过两个，请检查")
                                elif len(possiblecauses_children_ul) > 0:
                                    if len(possiblecauses_children_ul) == 1:
                                        possiblecauses_cause_id = False
                                        possiblecauses_ul_cause_id = False
                                        only_one_cause = False
                                        lis = possiblecauses_children_ul[0].xpath("./li")
                                        # logging.info(len(lis))
                                        ul_attrs = possiblecauses_children_ul[0].items()
                                        possiblecauses_attrs = possiblecauses.items()
                                        for item in possiblecauses_attrs:
                                            if item[0] == 'id':
                                                cause_id = item[1][5:]
                                                possiblecauses_cause_id = True
                                                only_one_cause = True
                                        if not possiblecauses_cause_id:
                                            for item in ul_attrs:
                                                if item[0] == 'id':
                                                    possiblecauses_ul_cause_id = True
                                                    cause_id = item[1][5:]
                                                    only_one_cause = True
                                                    # 后面获取内容都是某个cause的
                                        possiblecauses_contents = []
                                        for li in lis:
                                            get_possiblecauses_content_result, possiblecauses_content = self.get_text_p(
                                                li)
                                            logging.info(possiblecauses_content)
                                            if not get_possiblecauses_content_result:
                                                logging.error(possiblecauses_content)
                                            else:
                                                if not only_one_cause:
                                                    li_attrs = li.items()
                                                    for item in li_attrs:
                                                        if item[0] == 'id':
                                                            cause_id = item[1][5:]
                                                            self.possiblecauses_content.append(
                                                                {
                                                                    'cause_id': cause_id,
                                                                    'possiblecauses_content': possiblecauses_content
                                                                }
                                                            )
                                                        else:
                                                            logging.error(
                                                                self.topic_path + "possiblecauses的ul标记对中，有li未标记cause")
                                                else:
                                                    possiblecauses_contents.append(
                                                        possiblecauses_content)

                                        if only_one_cause:
                                            self.possiblecauses_content = {
                                                'cause_id': cause_id,
                                                'possiblecauses_content': '\n'.join(
                                                    possiblecauses_contents)
                                            }

                                        # get_possiblecauses_content_result, possiblecauses_content =  self.get_text_ul(possiblecauses_children_ul)
                                        # if get_possiblecauses_content_result:
                                        #     self.possiblecauses_content = possiblecauses_content
                                        # else:
                                        #     logging.error(possiblecauses_content)
                                    else:
                                        logging.error(self.topic_path + "possiblecauses中存在ul标记对超过两个，请检查")



                possiblecauses = alarmrefbody.xpath("possiblecauses")
                if len(possiblecauses) != 1:
                    logging.error(self.topic_path+"possiblecause个数错误")
                else:
                    possiblecause = possiblecauses[0]


                alarmhandling = alarmrefbody.xpath("alarmhandling")
                alarmhandling_unordered = alarmrefbody.xpath("alarmhandling-unordered")
                if (len(alarmhandling) + len(alarmhandling_unordered)) != 1:
                    logging.error(self.topic_path+"alarmhandling个数错误")
                else:
                    if len(alarmhandling) == 1:
                        real_alarmhandling = alarmhandling[0]
                    else:
                        real_alarmhandling = alarmhandling_unordered[0]
                    real_alarmhandling_steps = real_alarmhandling.xpath(".//step")

