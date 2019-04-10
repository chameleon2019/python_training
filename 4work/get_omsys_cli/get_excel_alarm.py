from MyCommon import MyExcel
from MyOmsysAlarmExcel import MyOmsysAlarmExcel
import sys
myexcelpath = r'D:\PTN_Work\告警自动化\omsys和资料告警对比模板_最终版_平台.xlsx'
workexcel = MyExcel.MyExcel(myexcelpath)
sheetname = "Sheet1"
get_rows_count_result, rows_count = workexcel.read_rows_count(sheetname, "L")
if not get_rows_count_result:
    print(rows_count)
    sys.exit()
get_worksheet_result, worksheet = workexcel.get_sheet_by_sheetname(sheetname)
if not get_worksheet_result:
    print(worksheet)
    sys.exit()
for i in range(3, rows_count+1):
    alarm_name = worksheet.Cells(i, "E").Value
    alarm_name_suffix = worksheet.Cells(i, "G").Value
    alarm_desc = worksheet.Cells(i, "L").Value
    alarm_id = int(worksheet.Cells(i, "Q").Value)
    alarm_type = worksheet.Cells(i, "X").Value
    alarm_severity = worksheet.Cells(i, "AB").Value
    print(alarm_name_suffix)
    # print(alarm_desc)
    # print(alarm_id)
    # print(alarm_type)
    # print(alarm_severity)

workexcel.close()
