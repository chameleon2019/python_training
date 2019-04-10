# -*- coding:utf-8 -*-
import logging
from lxml import etree
from MyCommon.MyDirLists import MyDirLists
from MyCommon.MyExcel import MyExcel

logging.basicConfig(level=logging.INFO, format=' %(asctime)s - %(levelname)s - %(message)s')
debug = True
# filepath = r'D:\PTN_SVN\多媒体\d00294865_tools\python\Alarm_Compare\SUBSYS_ID_CPUDEFEND_alminfo.xml'
#
# filexml = etree.parse(filepath)
# root= filexml.getroot()
# print(root.tag)
def get_carrier_objname(carrier_objname):
    result =''
    for i in carrier_objname:
        result = result + i + '\n'
    return result

def getText(elem):
    rc = []
    for node in elem.itertext():
        rc.append(node.strip())
    return ''.join(rc)

def get_list_getText(eles,des):
    if type(eles) == type([]):
        result = getText(eles[0])
    else:
        result = getText(eles)
    if result.strip() == "":
        return ""
    else:
        return result

def get_parameter(alarm_para_names,des):

    result = ''
    for item in alarm_para_names:
        if getText(item).strip() != "":
            result = result + getText(item)+'\n'
    if result == "":
        return ''
    return result

def get_list(eles,des=''):
    result = []
    for item in eles:
        result.append(getText(item).strip())
    return result

def makeup_parameter(para,para_desc):
    result = ''
    for i in range(len(para)):
        result = result + para[i] + ": "+para_desc[i]+'\n'
    return result

def makeup_one_cause(cause):
    des = ['对系统的影响','可能原因','处理建议','网管处理建议']
    result =''
    for i in range(4):
        if cause[i] !='':
            result = result + des[i]+"：" +cause[i] + '\n'
    return result



def makeup_cause(cause,may_cause,advise,network):
    result = ''
    for i in range(len(cause)):
        now = []
        now_cause = cause[i]
        now_may_cause = may_cause[i]
        now_advise = advise[i]
        try:
            now_network = network[i]
        except:
            now_network = '无'
        now.append(now_cause)
        now.append(now_may_cause)
        now.append(now_advise)
        now.append(now_network)
        now_result = makeup_one_cause(now)

        result = result + now_result + '\n'
    return result



xmlpath = r'E:\Github2019\python_training\4work\get_omsys_cli\alarmtopic'
files = MyDirLists(xmlpath).selected_files
class_desc = ['通信告警','业务质量告警','处理错误告警','设备告警','环境告警']
level_desc = ['紧急','重要','次要','提示']

# print(files)
alarm_mnemonic_map = {}
for file in files:
    filexml = etree.parse(file)
    try:
        alarm_mnemonic = get_list_getText(filexml.xpath("//alarm_mnemonic"), '告警本名')
        alarm_name_en = get_list_getText(filexml.xpath("//alarm_name_en"),'告警名称')
        alarm_mnemonic_map[alarm_mnemonic] = alarm_name_en
        alarm_name_cn = get_list_getText(filexml.xpath("//alarm_name_cn"),'告警解释中文')
        module = get_list_getText(filexml.xpath("//module"),'模块ID')
        trap_descr_cn = get_list_getText(filexml.xpath("//trap_descr_cn"),'Trap描述')
        feature = get_list_getText(filexml.xpath("//feature"),'特性分类')
        alarm_id =get_list_getText( filexml.xpath("//alarm_id"),'告警ID')
        alarm_class = get_list_getText(filexml.xpath("//event_type"),'告警分类')
        alarm_level = get_list_getText(filexml.xpath("//alarm_level"),'告警级别')
        alarm_para_names = get_list(filexml.xpath("//alarm_para_info/para_info/pa_name"),'参数名')
        alarm_para_infodatas = get_list(filexml.xpath("//alarm_para_info/para_info/pa_info_data"),'参数解释')
        prob_cause_reason = get_list(filexml.xpath("//prob_causes_cn/prob_cause_cn/pc_cause"),'告警原因')
        prob_cause_advise = get_list(filexml.xpath("//prob_causes_cn/prob_cause_cn/pc_advise"),'处理建议')
        prob_cause_network = get_list(filexml.xpath("//prob_causes_cn/prob_cause_cn/pc_network"),'网管处理建议')
        prob_cause_cause = get_list(filexml.xpath("//prob_causes_cn/prob_cause_cn/pc_may_cause"),'对系统的影响')
        itut_para_sequence = get_list_getText(filexml.xpath("//itut_para_sequence"),'上报网管参数')
        carrier_objname =  get_list(filexml.xpath("//fim/carrier_objects/carrier_obj/carrier_objname"),'告警抑制')
        # event_type = get_list_getText(filexml.xpath("//event_type"),'类型')

    except:
        print("Error: "+file)
    else:


        if trap_descr_cn.strip() == "":
            alarm_des = alarm_name_cn
        else:
            alarm_des = trap_descr_cn.strip()

        paras = makeup_parameter(alarm_para_names, alarm_para_infodatas)
        cause = makeup_cause(prob_cause_cause, prob_cause_reason, prob_cause_advise, prob_cause_network)
        carrier_objname = get_carrier_objname(carrier_objname)
        # 告警类型映射

        # 告警级别映射
        alarm_level = level_desc[int(alarm_level)-1]
        alarm_class = class_desc[int(alarm_class)-1]

        # if len(alarm_para_names) != len(alarm_para_infodatas):
        # if len(alarm_para_names) == len(alarm_para_infodatas):
        if debug:
            logging.info('-------------------------------------------------------------')
            logging.info(file)
            logging.info(alarm_mnemonic)
            logging.info(alarm_name_en)
            logging.info(module)
            logging.info(feature)
            logging.info(alarm_des)
            logging.info(alarm_id)
            logging.info(alarm_class)
            logging.info(alarm_level)
            logging.info(paras)
            logging.info(cause)
            logging.info("抑制:"+'\n'+carrier_objname)
            itut_para_sequence_parameters = ",".join(itut_para_sequence.split("$")[1:])
            itut_para_sequence_parameter_list = itut_para_sequence.split("$")[1:]
            logging.info(itut_para_sequence_parameters)
            # logging.info("event:"+event_type)
        # print()
        # print(file)
        # print(alarm_des)

        # print(paras)
        # print(cause)

        # alarm_para = alarm_para_names +'\n' + alarm_para_infodatas
        # prob_cause = prob_cause_reason+'\n' + prob_cause_advise+'\n' + prob_cause_network+'\n' + prob_cause_cause
        else:
            # excel.book.Worksheets(sheetname).Cells(excel_index,1).Value = alarm_name_en
            # excel.book.Worksheets(sheetname).Cells(excel_index,2).Value = module
            # excel.book.Worksheets(sheetname).Cells(excel_index,3).Value = feature
            # excel.book.Worksheets(sheetname).Cells(excel_index,4).Value = alarm_des
            # excel.book.Worksheets(sheetname).Cells(excel_index,8).Value = alarm_id
            # excel.book.Worksheets(sheetname).Cells(excel_index,12).Value = alarm_class
            # excel.book.Worksheets(sheetname).Cells(excel_index,16).Value = alarm_level
            # excel.book.Worksheets(sheetname).Cells(excel_index,20).Value = paras
            # excel.book.Worksheets(sheetname).Cells(excel_index,24).Value = cause
            # excel.book.Worksheets(sheetname).Cells(excel_index,28).Value = carrier_objname
            # excel.book.Worksheets(sheetname).Cells(excel_index,30).Value = itut_para_sequence
            #
            # excel_index +=1
            pass
logging.info(alarm_mnemonic_map)
#

# if not debug:
#     excel.save()
#     excel.close()