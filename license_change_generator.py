from MyExcel import MyExcel
import sys, os
from configobj import ConfigObj

# sales_data = r'D:\Zhijie_Workplace\data\compare_license\sales.xlsx'
# license_data = r'D:\Zhijie_Workplace\data\compare_license\License.xlsx'
config_data = r'D:\Zhijie_Workplace\data\compare_license\config.config'


try:
    # sales_excel = MyExcel(sales_data)
    # license_excel = MyExcel(license_data)
    continue_flag = True
    configs = ConfigObj(config_data)

    license_map = configs['licensemap']
    product_map = configs['productmap']
    # print(configs)
    print(license_map)
    print(product_map)
    for license_data, sales_data in license_map.items():
        # print(item)
        if not os.path.exists(license_data):
            print(license_data + " 不存在，请检查！")
            continue_flag = False
        if not os.path.exists(sales_data):
            print(sales_data + " 不存在，请检查！")
            continue_flag = False

        if continue_flag:
            print(sales_data)
            print(license_data)
            sales_excel = MyExcel(sales_data)
            license_excel = MyExcel(license_data)
            get_license_sheetnames_result, license_excel_sheetnames = license_excel.get_sheetnames()
            if not get_license_sheetnames_result:
                print("获取sheetname失败：" + license_data)
            # else:
            #     print(license_excel_sheetnames)
            get_sales_sheetnames_result, sales_excel_sheetnames = sales_excel.get_sheetnames()
            if not get_sales_sheetnames_result:
                print("获取sheetname失败：" + sales_data)
            # else:
            #     print(sales_excel_sheetnames)

            for sales_product_sheetname in sales_excel_sheetnames:
                # print(sales_product_sheetname)
                try:
                    license_product_sheetname = product_map[sales_product_sheetname]
                except:
                    print("表格映射有误："+sales_product_sheetname)
                    continue


                print(sales_product_sheetname+' '+license_product_sheetname)
                if license_product_sheetname not in license_excel_sheetnames:
                    print("License未找到sheet: " + license_product_sheetname)
                    continue
                else:
                    get_sheet_result_s, sales_product_sheet = sales_excel.get_sheet_by_sheetname(sales_product_sheetname)
                    get_sheet_result_l, license_product_sheet = license_excel.get_sheet_by_sheetname(license_product_sheetname)
                    read_result, sales_bom_column = sales_excel.read_certain_column(sales_product_sheetname, "BOM")
                    # print(sales_bom_column)
                    read_result, license_bom_column  = license_excel.read_certain_column(license_product_sheetname, "BOM")
                    # print(license_bom_column)
                    read_rows_count_result, sales_row_count = sales_excel.read_rows_count(sales_product_sheetname,sales_bom_column)
                    read_rows_count_result, license_row_count = license_excel.read_rows_count(license_product_sheetname,
                                                                                            license_bom_column)
                    # print(sales_row_count, license_row_count)
                    sales_boms = []
                    license_boms = []
                    for row_s in range(2, sales_row_count+1):
                        bom_data = str(sales_product_sheet.Cells(row_s, sales_bom_column).Value)
                        if sales_product_sheet.Cells(row_s, sales_bom_column).Font.Strikethrough:
                            print(bom_data)
                        else:
                            if bom_data.strip() !="":
                                sales_boms.append(bom_data)
                    # print(sales_boms)

                    for row_l in range(2, license_row_count+1):
                        bom_data_l = str(license_product_sheet.Cells(row_l, license_bom_column).Value)
                        if bom_data_l.strip() !="":
                            license_boms.append(bom_data_l)
                        else:
                            print(bom_data_l)
                    # print(license_boms)
                    print(list(set(license_boms).difference(set(sales_boms))))
                    print(list(set(sales_boms).difference(set(license_boms))))
                    print(list(set(sales_boms).intersection(set(license_boms))))

            sales_excel.close()
            license_excel.close()
except Exception as e:
    print("Exception:"+str(e))