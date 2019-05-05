from lxml import etree
from MyCommon.MyDirLists import MyDirLists
import logging
from TopicAlarm import TopicAlarm
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)

# zh_topics = r'D:\Actions\Test_Enviroment\python_Work\ptn_info_tools\alarm_to_omsys\data\html\zh\PTN7900E-32'
zh_topics = r'E:\Github2019\python_training\4work\get_alarm_topic'

topic_lists = MyDirLists(zh_topics, file_filter='.*\.xml')
new_topic_lists = []
for item in topic_lists.selected_files:
    if not item.endswith('_ref.xml'):
        new_topic_lists.append(item)
# print(new_topic_lists)
for topic_path in new_topic_lists:
    logging.info(topic_path)
    topic_alarm = TopicAlarm(topic_path, "zh", 'xml')
    if topic_alarm.validated_topic:

        # pass
        # logging.info(topic_alarm.cause_ids)
        #
        if topic_alarm.successful_parse:
            for item in topic_alarm.__dict__:
                logging.info(item)
            # logging.info(topic_alarm.possiblecauses_content)
            # logging.info(topic_alarm.impactonsystem_contents)
            # logging.info(topic_alarm.alarmhandling_contents)
            # logging.info(topic_alarm.alarmparameters_contents)
            # logging.info(topic_alarm)
            pass
        else:
            logging.error(topic_alarm.not_successful_parse_reason)
        # pass
    else:
        logging.error(topic_alarm.not_validated_reason)