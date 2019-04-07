from MyOmsysCli import MyOmsysCli
from MyTopicCli import MyTopicCli
import os

topic_cli_path = r''
omsys_xml_files = []
for omsys_xml_file in omsys_xml_files:
    file_name = os.path.basename(omsys_xml_file)
    omsys_xml_content = MyOmsysCli(omsys_xml_file)
    omsys_xml_content.get_xml_info()
    topic_cli_zh = MyTopicCli()
    topic_cli_zh.generate_cli_topic_from_omsys_cli(omsys_xml_content, "zh-cn")
    topic_cli_zh_path = os.path.join(os.path.join(topic_cli_path, "zh"), file_name)
    topic_cli_zh.save_to_xml(topic_cli_zh_path)
    topic_cli_en = MyTopicCli()
    topic_cli_en_path = os.path.join(os.path.join(topic_cli_path, "en"), file_name)
    topic_cli_en.generate_cli_topic_from_omsys_cli(topic_cli_en_path)

