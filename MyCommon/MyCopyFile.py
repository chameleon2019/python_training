import os
import shutil
import logging
from MyCommon.MyCommon import MyCommon
logging.basicConfig(level=logging.INFO, format=' %(asctime)s - %(levelname)s - %(message)s')


class MyCopyFile:
    def __init__(self, src, dst):
        self.src = src
        self.src_exist = True
        if not os.path.exists(self.src):
            error_message = "源文件或文件夹不存在——" + src
            self.src_exist = False
            self.src_not_exist_message = error_message
        self.src_type = self.judge_file_dir(self.src)
        self.dst = dst
        self.dst_exist = True
        if not os.path.exists(self.dst):
            self.dst_exist = False
        self.dst_type = self.judge_file_dir(self.dst)

    # 拷贝函数
    def copy(self, fastcopy=False, fastcopy_path='', log_position=''):
        if self.src_type == "file":
            if self.dst_type == "file":
                dst_dir = os.path.dirname(self.dst)
                if not os.path.exists(dst_dir):
                    os.makedirs(dst_dir)
                logging.debug("拷贝文件——" + "Source: " + self.src + ". Destination: " + self.dst)
                shutil.copyfile(self.src, self.dst)
                if MyCommon.compare_md5(self.src, self.dst):
                    return True, self.dst
                else:
                    error_message = "拷贝" + self.src + "到：" + self.dst + "失败。"
                    return False, error_message
            elif self.dst_type == "dir":
                logging.debug("拷贝文件至文件夹——" + "Source: " + self.src + ". Destination: " + self.dst)
                return self.copy_file_to_dir()
            else:
                error_message = "目的路径非文件或文件夹，请检查：" + self.dst
                return False, error_message
        elif self.src_type == "dir":
            if self.dst_type == "dir":
                if fastcopy:
                    return self.fastcopy_dir_to_dir(fastcopy_path, log_position)
                else:
                    return self.copy_dir_to_dir()
        else:
            error_message = "源路径非文件或文件夹，请检查：" + self.src
            return False, error_message

    # 判断路径是文件夹还是文件
    @staticmethod
    def judge_file_dir(file_path):
        if os.path.exists(file_path):
            if os.path.isdir(file_path):
                return "dir"
            elif os.path.isfile(file_path):
                return "file"
            else:
                return None
        else:
            paths = file_path.split("\\")
            last_element = paths[len(paths) - 1]
            logging.debug(last_element)
            if len(last_element.split(".")) > 1:
                return "file"
            else:
                return "dir"

    # 改写tostr
    def __str__(self):
        object_desc = '---------------------------new_to_str------------------------------'
        for name, value in vars(self).items():
            object_desc += '\n' + '%s=%s' % (name, value)
        object_desc += '\n' + '---------------------------new_to_str_end-----------------------------'
        return object_desc

    # 拷贝文件到文件夹
    def copy_file_to_dir(self):
        filename = os.path.basename(self.src)
        dst_file = os.path.join(self.dst, filename)
        try:
            if not os.path.exists(self.dst):
                os.makedirs(self.dst)
        except Exception as e:
            error_message = '创建文件夹失败：' + self.dst + "：" + str(e)
            return False, error_message
        shutil.copyfile(self.src, dst_file)
        if os.path.exists(dst_file):
            return True, dst_file
        else:
            error_message = '目的文件拷贝失败，请检查是否有文件已经存在并被占用：' + dst_file
            return False, error_message

    # 拷贝文件夹到文件夹
    def copy_dir_to_dir(self):
        filename = os.path.basename(self.src)
        dst_file = os.path.join(self.dst, filename)
        names = os.listdir(self.src)
        try:
            if not os.path.exists(self.dst):
                os.makedirs(self.dst)
        except Exception as e:
            error_message = '创建文件夹失败：' + self.dst + str(e)
            return False, error_message
        try:
            for name in names:
                srcname = os.path.join(self.src, name)
                if os.path.isdir(srcname):
                    self.copy_dir_to_dir()
                else:
                    shutil.copy2(srcname, dst_file)
            return True, self.dst
        except Exception as e:
            error_message = str(e)
            return False, error_message

    # 拷贝文件夹到文件夹（fastcopy）
    def fastcopy_dir_to_dir(self, fastcopy_path, log_position):
        return MyCommon.fastcopy(fastcopy_path, log_position, self.src, self.dst)
