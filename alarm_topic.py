from lxml import etree
from MyCommon.MyDirLists import MyDirLists
import logging
from TopicAlarm import TopicAlarm
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)

zh_topics = r'E:\Github2019\python_training\4work\get_alarm_topic'

topic_lists = MyDirLists(zh_topics, file_filter='.*\.xml')
new_topic_lists = []
for item in topic_lists.selected_files:
    if not item.endswith('_ref.xml'):
        new_topic_lists.append(item)

for topic_path in new_topic_lists:
    topic_alarm = TopicAlarm(topic_path, "zh")
    if topic_alarm.is_alarm_topic:
        logging.info(topic_path)
        logging.info(topic_alarm.alarmdesc_content)
        logging.info(topic_alarm.impactonsystem_content)
        logging.info(topic_alarm.possiblecauses_content)



