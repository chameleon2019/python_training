from MyOmsysAlarm import MyOmsysAlarm

import os,logging
# topic_cli_path = r''
omsys_xml_files = [r'E:\Github2019\python_training\4work\get_omsys_cli\alarmtopic\a.xml']
for omsys_xml_file in omsys_xml_files:
    file_name = os.path.basename(omsys_xml_file)
    omsys_xml_content = MyOmsysAlarm(omsys_xml_file)
    get_xml_info_result, info = omsys_xml_content.get_xml_info()
    if not get_xml_info_result:
        print(info)
    else:
        print(omsys_xml_content)
    # logging.info(omsys_xml_content)