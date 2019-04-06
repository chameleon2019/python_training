import re
import logging
import os
import sys
logging.basicConfig(level=logging.INFO, format=' %(asctime)s - %(levelname)s - %(message)s')


class MyDirLists:
    def __init__(self, path, dir_filter=".*", file_filter=".*", level=0, needed_level=0):
        self.original_path = path   # 原始路径
        self.path_type = ""     # 原始路径的类型：多个路径还是一个路径
        self.selected_dirs = []     # 需要处理的文件夹集合
        self.all_dirs = []      # 读取到的所有的文件夹集合
        self.all_certain_level_dirs = []    # 规定了读取深度的时候的文件夹
        self.level = 0  # 最大读取深度
        self.needed_level = 0   # 需要读取的深度
        self.selected_dirs_with_level = {}  # 带级别的需要处理的文件夹字典
        self.selected_certain_level_dirs = []   # 读取的特定级别的文件夹列表
        self.all_dirs_with_level = {}  # 所有文件夹，带级别
        self.init_status = True     # 初始化状态：成功还是失败
        self.init_failure_reason = ""   # 初始化失败的原因
        self.dir_filter = dir_filter    # 文件夹过滤器
        self.file_filter = file_filter  # 文件过滤器
        self.selected_files = []    # 读取的文件结果
        self.all_max_level = 0  # 所有文件中最大深度
        self.selected_max_level = 0     # 读取出文件的最大深度
        self.dir_rule = None    # 文件夹筛选规则
        self.file_rule = None   # 文件筛选规则
        # 判断原始路径类型
        if type(self.original_path) == list:
            self.path_type = "list"
            if level != 0:
                error_message = "原始路径为列表时，不支持统计文件夹级别，设置的level会重置为0。"
                logging.warning(error_message)
                self.level = 0
        elif type(self.original_path) == str:
            self.path_type = "str"
            self.level = level
            self.needed_level = needed_level
            if self.level < 0:
                error_message = "Level值不能小于0：" + str(self.level)
                self.init_status = False
                self.init_failure_reason = error_message
        else:
            error_message = "路径不是路径列表或者字符串形式。"
            self.init_status = False
            self.init_failure_reason = error_message
        # 获取dir筛选规则
        if self.dir_filter != ".*":
            try:
                self.dir_rule = re.compile(self.dir_filter)
            except Exception as e:
                error_message = "路径过滤器设置错误" + self.dir_filter + "， 请检查：" + str(e)
                self.init_status = False
                self.init_failure_reason = error_message
        if self.file_filter != ".*":
            try:
                self.file_rule = re.compile(self.file_filter)
            except Exception as e:
                error_message = "文件名过滤器设置错误：" + self.file_filter + "， 请检查：" + str(e)
                self.init_status = False
                self.init_failure_reason = error_message
        # 确定目的文件夹
        self.read_certain_dirs_in_dir()
        # 确定目的文件夹中的目的文件
        self.read_files_in_selected_dirs()

    # 多个文件夹过滤
    def get_dirs_m(self, path, dir_rule=None):
        self.all_dirs.append(path)
        if dir_rule is not None:
            dir_name = os.path.basename(path)
            if dir_rule.search(dir_name) is not None:
                self.selected_dirs.append(path)
        else:
            self.selected_dirs.append(path)
        children = os.listdir(path)
        for child in children:
            child_dir = os.path.join(path, child)
            if os.path.isdir(child_dir):
                self.get_dirs_m(child_dir, dir_rule)

    # 单个文件夹过滤
    def get_dirs(self, path, dir_rule=None, level=0):
        self.all_dirs.append(path)
        self.all_dirs_with_level[path] = self.count_dir_level(path)
        if level > 0:
            level = level - 1
            if dir_rule is not None:
                dir_name = os.path.basename(path)
                if dir_rule.search(dir_name) is not None:
                    self.selected_dirs.append(path)
                    self.selected_dirs_with_level[path] = self.count_dir_level(path)
            else:
                self.selected_dirs.append(path)
                self.selected_dirs_with_level[path] = self.count_dir_level(path)
            children = os.listdir(path)
            for child in children:
                child_dir = os.path.join(path, child)
                if os.path.isdir(child_dir):
                    if level != 0:
                        self.get_dirs(child_dir, dir_rule, level)
        else:
            if dir_rule is not None:
                dir_name = os.path.basename(path)
                if dir_rule.search(dir_name) is not None:
                    self.selected_dirs.append(path)
                    self.selected_dirs_with_level[path] = self.count_dir_level(path)
            else:
                self.selected_dirs.append(path)
                self.selected_dirs_with_level[path] = self.count_dir_level(path)

            children = os.listdir(path)
            for child in children:
                child_dir = os.path.join(path, child)
                if os.path.isdir(child_dir):
                    self.get_dirs(child_dir, dir_rule, level)

    def read_certain_dirs_in_dir(self):
        # 获取输入的原始层级
        # if self.path_type == "str":
        #     ori_level = self.level
        ori_level = self.level
        path = self.original_path
        # # 判断输入的path是多个path，还是一个path
        if type(path) == list:
            for item in path:
                # 判断是否有效
                if os.path.isdir(item):
                    self.get_dirs_m(path=item, dir_rule=self.dir_rule)
                else:
                    error_message = item + "——非有效目录，已忽略！"
                    logging.error(error_message)
        elif type(path) == str:
            if os.path.isdir(path):
                self.get_dirs(path, self.dir_rule, ori_level)
            else:
                error_message = path + "——非有效目录"
                logging.error(error_message)
                sys.exit()
            if self.needed_level != 0:
                for each_dir in self.selected_dirs_with_level.keys():
                    if self.selected_dirs_with_level[each_dir] == self.needed_level:
                        self.selected_certain_level_dirs.append(each_dir)
            if self.needed_level != 0:
                for each_dir in self.all_dirs_with_level.keys():
                    if self.all_dirs_with_level[each_dir] == self.needed_level:
                        self.all_certain_level_dirs.append(each_dir)
            if len(self.all_dirs_with_level) > 0:
                self.all_max_level = self.all_dirs_with_level[
                    max(self.all_dirs_with_level, key=self.all_dirs_with_level.get)]
            if len(self.selected_dirs_with_level) > 0:
                self.selected_max_level = self.selected_dirs_with_level[
                    max(self.selected_dirs_with_level, key=self.selected_dirs_with_level.get)]
            if self.level > 0 and len(self.selected_certain_level_dirs) == 0:
                logging.info("此级别文件夹内无匹配文件夹：" + str(self.level))
                # sys.exit()
        else:
            error_message = "要处理的文件" + path + "非目录或目录列表"
            logging.error(error_message)

    def read_files_in_selected_dirs(self):
        for path in self.selected_dirs:
            for file in os.listdir(path):
                file_path = os.path.join(path, file)
                if re.match(self.file_filter, file):
                    self.selected_files.append(file_path)

    def list_all_member(self):
        for name, value in vars(self).items():
            print('%s=%s' % (name, value))

    def count_dir_level(self, dst_dir, src_dir=""):
        if src_dir == "":
            src_dir = self.original_path
        spliter = '\\'
        len_src = len(src_dir.split(spliter))
        len_dst = len(dst_dir.split(spliter))
        level = len_dst-len_src
        return level+1

    @staticmethod
    def write_list_to_txt(datalist, result_txt_path):
        try:
            pathdir, basename = os.path.split(result_txt_path)
            if not os.path.exists(pathdir):
                os.makedirs(pathdir)
            file = open(result_txt_path, "w")
            file.truncate()
        except Exception as e:
            error_message = "路径不正确，请检查" + str(e)
            logging.error(error_message)
            sys.exit()
        for i in datalist:
            file.writelines(i + '\n')
        file.close()
        logging.info("已保存至" + result_txt_path)
