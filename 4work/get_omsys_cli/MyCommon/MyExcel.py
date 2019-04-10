import win32com
from win32com.client import constants as c
import logging
import os

logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')


class MyExcel:
    def __init__(self, filepath=""):
        self.filepath = filepath
        self.workbook = None
        self.fileExist = False
        self.fileOrDir = "unknown"
        self.ExcelApp = win32com.client.gencache.EnsureDispatch("Excel.Application")
        self.now_sheet = None
        if filepath != "":
            # 判断文件路径是否存在
            if os.path.exists(self.filepath):
                if os.path.isfile(filepath):
                    self.fileExist = True
                    self.fileOrDir = "file"
                    (self.path, self.name) = os.path.split(self.filepath)
                elif os.path.isdir(self.filepath):
                    self.fileExist = True
                    self.fileOrDir = "dir"

            try:
                self.workbook = self.ExcelApp.Workbooks.Open(filepath)
                self.successfulOpen = True
            except Exception as e:
                error_message = r'打开文件失败：' + filepath + ": " + str(e)
                logging.debug(error_message)
                self.successfulOpen = False
                self.openFailedReason = error_message

    # 获取单元格数值
    def read_cell_value(self, sheetname, row_number, column_number):
        try:
            sheet = self.workbook.Worksheets(sheetname)
            cell_value = sheet.Cells(row_number, column_number).Value
        except Exception as e:
            error_message = r"读取表格内容失败：" + str(e)
            logging.debug(error_message)
            return False, error_message
        return True, cell_value

    # 获取列数
    def read_columns_count(self, sheetname, row_number):
        try:
            sheet = self.workbook.Worksheets(sheetname)
            if isinstance(row_number, int):
                columns_count = sheet.UsedRange.Columns.Count
                for column in range(columns_count, 1, -1):
                    if sheet.Cells(row_number, column).Value is not None:
                        columns_count = column
                        break
            else:
                error_message = r'输入的row_number必须是数字类型，请检查。'
                logging.debug(error_message)
                return False, error_message
            return True, columns_count
        except Exception as e:
            error_message = r'读取列数失败：' + str(e)
            logging.debug(error_message)
            return False, error_message

    # 获取行数
    def read_rows_count(self, sheetname, column_number):
        try:
            sheet = self.workbook.Worksheets(sheetname)
            if isinstance(column_number, str):
                rows_count = sheet.Range(column_number + "65535").End(c.xlUp).Row
            elif isinstance(column_number, int):
                rows_count = sheet.Cells(65535, column_number).End(c.xlUp).Row
            else:
                error_message = r'输入的column_number必须是字符或数字类型，请检查。'
                logging.debug(error_message)
                return False, error_message
            return True, rows_count
        except Exception as e:
            error_message = r'读取行数失败：' + str(e)
            logging.debug(error_message)
            return False, error_message

    # 读取特定列名对应的列数
    def read_certain_column(self, sheetname, columnname, row_number=1):
        try:
            sheet = self.workbook.Worksheets(sheetname)
        except Exception as e:
            error_message = r'读取表格失败：' + str(e)
            logging.debug(error_message)
            return False, error_message
        try:
            for column in range(1, 65535):
                if sheet.Cells(row_number, column).Value == columnname:
                    column_number = column
                    return True, column_number
        except Exception as e:
            error_message = r'获取数据失败：' + str(e)
            logging.debug(error_message)
            return False, error_message
        return False, "未找到此数据"

    # 读取特定行名对应的行数
    def read_certain_row(self, sheetname, rowname, column_number=1):
        try:
            sheet = self.workbook.Worksheets(sheetname)
        except Exception as e:
            error_message = r'读取表格失败：' + str(e)
            logging.debug(error_message)
            return False, error_message
        try:
            for row in range(1, 65535):
                if sheet.Cells(row, column_number).Value == rowname:
                    row_number = row
                    return True, row_number
        except Exception as e:
            error_message = r'获取数据失败：' + str(e)
            logging.debug(error_message)
            return False, error_message
        return False, "未找到此数据"

    # 创建excel文件，指定路径和文件名
    def create_excel(self, path, filename, sheetname="Sheet1"):
        if self.filepath == "":
            self.ExcelApp.Visible = False
            self.path = path
            self.name = filename
            try:
                self.workbook = self.ExcelApp.Workbooks.Add()
                # self.xlApp.Worksheets.Add().Name = sheet_name
                self.ExcelApp.Worksheets("Sheet1").Name = sheetname
                self.now_sheet = self.ExcelApp.Worksheets(sheetname)
                self.filepath = os.path.join(path, filename)
                # print(self.filepath)
                if os.path.exists(self.filepath):
                    error_message = self.filepath + "已存在，创建失败"
                    return False, error_message
                self.workbook.SaveAs(self.filepath)
                return True, self.workbook
            except Exception as e:
                return False, str(e)
        else:
            error_message = r"filepath初始化不为空，不能创建文件"
            return False, error_message

    # 创建表
    def create_sheet(self, sheetname):
        try:
            self.workbook.Worksheets.Add()
            self.workbook.Worksheets.Add().Name = sheetname
            self.save()
            return True, self.workbook.Worksheets(sheetname)
        except Exception as e:
            error_message = r'创建表格失败:' + sheetname + str(e)
            return False, error_message

    # 获取所有表名
    def get_sheetnames(self):
        if self.workbook is not None:
            sheetnames = []
            for sheet in self.workbook.Worksheets:
                sheetnames.append(sheet.Name)
            return True, sheetnames
        else:
            error_message = "workbook不存在，无法获取表名"
            return False, error_message

    # 获取所有未隐藏的表名
    def get_visible_sheetnames(self):
        if self.workbook is not None:
            sheetnames = []
            for sheet in self.workbook.Worksheets:
                if sheet.Visible:
                    sheetnames.append(sheet.Name)
            return True, sheetnames
        else:
            error_message = "workbook不存在，无法获取表名"
            return False, error_message

    # 根据表名获取worksheet
    def get_sheet_by_sheetname(self, sheetname):
        get_sheetname_result, sheetnames = self.get_sheetnames()
        if get_sheetname_result:
            if sheetname in sheetnames:
                return True, self.workbook.Worksheets(sheetname)
            else:
                error_message = "不存在表：" + sheetname
                return False, error_message
        else:
            return False, sheetnames

    # 写数据到单元格
    def write_data_into_cell(self, sheetname, row_number, column_number, cell_value, cell_format="@"):
        get_sheet_result, worksheet = self.get_sheet_by_sheetname(sheetname)
        if get_sheet_result:
            try:
                worksheet.Cells(row_number, column_number).NumberFormatLocal = cell_format
                worksheet.Cells(row_number, column_number).Value = cell_value
                return True, cell_value
            except Exception as e:
                error_message = r'写单元格数据失败，请检查：行：' + row_number + ", 列：" + column_number + ":" + str(e)
                return False, error_message
        else:
            return False, worksheet

    # 读取单元格数据
    def get_cell_value(self, sheetname, row_number, column_number):
        get_sheet_result, worksheet = self.get_sheet_by_sheetname(sheetname)
        if get_sheet_result:
            try:
                cell_value = worksheet.Cells(row_number, column_number).Value
                return True, cell_value
            except Exception as e:
                error_message = r'获取单元格数据失败，请检查：行：' + row_number + ", 列：" + column_number + ":" + str(e)
                return False, error_message
        else:
            return False, worksheet

    # 删除行，暂时不处理
    def delete_row_for_board_spec(self, sheetname, column, max_row):
        get_sheet_result, worksheet = self.get_sheet_by_sheetname(sheetname)
        if get_sheet_result:
            for i in range(2, max_row):
                column_content = worksheet.Cells(1, column).Value
                content = worksheet.Cells(i, column).Value
                if column_content == "备注":
                    return False
                else:
                    if content is None:
                        logging.error("空白单元格" + str(i) + "," + str(column))
                        return False
                    else:
                        if content.strip() != "\\" and content.strip() != "×":
                            return False
            worksheet.Columns(column).Delete()
            self.save()
            return True
        else:
            return False, worksheet

    # 设置大纲方向，默认为“单板特性规格矩阵”设置
    def set_outline_direction(self, sheetname=r"单板特性规格矩阵"):
        get_sheet_result, worksheet = self.get_sheet_by_sheetname(sheetname)
        if get_sheet_result:
            try:
                if worksheet.Outline.SummaryColumn == c.xlLeft:
                    return True, "已经是正确的组合方向"
                # worksheet.Outline.SummaryRow = c.xlAbove
                worksheet.Outline.SummaryColumn = c.xlLeft
                if worksheet.Outline.SummaryColumn == c.xlLeft:
                    return True, "成功设置为正确的组合方向"
            except Exception as e:
                return False, str(e)
        else:
            return False, worksheet

    # 获取大纲级别
    def get_outline_level(self, sheetname, column_number):
        get_sheet_result, worksheet = self.get_sheet_by_sheetname(sheetname)
        if get_sheet_result:
            try:
                outline_level = int(worksheet.Columns(column_number).OutlineLevel)
                return True, outline_level
            except Exception as e:
                return False, str(e)
        else:
            return False, worksheet

    def del_app(self):
        del self.ExcelApp

    def save(self):
        self.workbook.Save()

    def close(self):
        self.workbook.Close(SaveChanges=0)
