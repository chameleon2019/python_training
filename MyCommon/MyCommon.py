import datetime
import logging
import subprocess
import hashlib
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)


class MyCommon:
    # 生成时间戳
    @staticmethod
    def get_formated_time(rule="%Y-%m-%d-%H-%M-%S"):
        now_time = datetime.datetime.now()
        formated_time = now_time.strftime(rule)
        return formated_time

    # 获取日志名称
    @staticmethod
    def get_log_name(logname, log_ext="log"):
        return logname + '_' + MyCommon.get_formated_time() + '.'+log_ext

    # fastcopy拷贝文件
    @staticmethod
    def fastcopy(fastcopy_path, log_position, src_dir, dst_dir):
        copy_command = fastcopy_path.strip() \
                       + " /cmd=diff /auto_close /no_ui /error_stop=FALSE /balloon=FALSE /verify /filelog=" \
                       + log_position + " " \
                       + src_dir + " /to=" \
                       + dst_dir
        logging.debug(copy_command)
        try:
            a = subprocess.Popen(copy_command, shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            a.wait()
            return True, dst_dir
        except Exception as e:
            error_message = "拷贝" + src_dir + "到" + dst_dir + "失败，请检查：" + str(e)
            return False, error_message

    # 根据fastcopy日志检查fastcopy的结果
    @staticmethod
    def check_fastcopy_log(log_position):
        f = open(log_position, encoding='utf-8')
        content = f.readlines()
        copy_info = []
        for item in content:
            if item.startswith("<Source>"):
                source = item.split("  ")[1].strip()
            if item.startswith("<DestDir>"):
                target = item.split(" ")[1].strip()
            if item.startswith('TotalTime'):
                used_time = item.split("=")[1].strip().split(" ")[0]
            if item.startswith("Result"):
                error_files = item.split("Result : ")[1].strip().split("/")[0].strip().split(":")[1].strip()
                error_dirs = item.split("(")[1].strip().split("/")[1].strip().split("(")[0].split(":")[1].strip()[:-1]
                result = source + ' ' + target + ' ' + used_time + ' ' + error_files + ' ' + error_dirs
                logging.debug(result)
                each_copy = [source, target, used_time, error_files, error_dirs]
                copy_info.append(each_copy)
        return copy_info

    # 比较MD5判断是否相同
    @staticmethod
    def compare_md5(file1, file2):
        md5_1 = hashlib.md5(open(file1, 'rb').read()).hexdigest()
        md5_2 = hashlib.md5(open(file2, 'rb').read()).hexdigest()
        if md5_1 == md5_2:
            return True
        else:
            return False

    # 去除列表重复值
    @staticmethod
    def purify_list(ori_list):
        new_list = list(set(ori_list))
        new_list.sort(key=ori_list.index)
        return new_list

    # 去除列表中的空值
    @staticmethod
    def remove_empty_element(ori_list):
        for item in ori_list:
            if item.strip() == "":
                ori_list.remove(item)
        return ori_list
