import sys, os, shutil, time
import zipfile


def compressZip(sourcePath, target):
    targetPath = os.path.dirname(target)
    if not os.path.exists(targetPath):
        os.mkdir(targetPath)

    tarZip = zipfile.ZipFile(target, 'w', zipfile.ZIP_STORED)
    fileList = []
    for root, dirs, files in os.walk(sourcePath):
        for file in files:
            fileList.append(os.path.join(root, file))

    print(fileList)

    for filename in fileList:
        tarZip.write(filename, filename[len(sourcePath):])
    tarZip.close()
    print('compress file successfully!')
    return True

def replace_file(hedex_file):
    file_name = os.path.basename(hedex_file)
    hedex_file_path = os.path.dirname(hedex_file)
    real_hdx_file_path = os.path.join(hedex_file_path,'temp')
    if not os.path.exists(real_hdx_file_path):
        os.makedirs(real_hdx_file_path)
    real_hdx_file = os.path.join(real_hdx_file_path, file_name)
    shutil.copy(hedex_file, real_hdx_file)
    hdx_extract_path = os.path.join(hedex_file_path, 'temp_all')
    if not os.path.exists(hdx_extract_path):
        os.makedirs(hdx_extract_path)
    replace_dir = os.path.join(hedex_file_path, 'replace')
    if not os.path.exists(replace_dir):
        return False, "不存在replace文件夹"
    to_replace_file = []
    compare_replace_file = []
    for replace_filepath, dirs, files in os.walk(replace_dir):
        for file in files:
            replace_file = os.path.join(replace_filepath, file)
            to_replace_file.append(replace_file)
    for file in to_replace_file:
        compare_replace_file.append(file.replace(replace_dir, 'resources').replace('\\', '/'))

    with zipfile.ZipFile(hedex_file) as f:
        for name in f.namelist():
            if name.endswith('.hdx'):
                hdx = name
                f.extract(hdx, hdx_extract_path)
                hdx_path = os.path.join(hdx_extract_path, hdx.replace("/", '\\'))
                new_hdx_path = hdx_path.replace('.hdx', '_new.hdx')

                if not os.path.exists(hdx_path):
                    print("extract_nok")
                else:
                    hdx_f = zipfile.ZipFile(hdx_path)
                    new_hdx_f = zipfile.ZipFile(new_hdx_path, 'w')
                    for each_hdx_file in hdx_f.infolist():

                        file_data = hdx_f.read(each_hdx_file.filename)
                        if each_hdx_file.filename in compare_replace_file:
                            print(each_hdx_file.filename + ' 已替换')
                            index = compare_replace_file.index(each_hdx_file.filename)
                            change_file = to_replace_file[index]
                            file_data = open(change_file, 'rb').read()
                        new_hdx_f.writestr(each_hdx_file, file_data)
                    hdx_f.close()
                    new_hdx_f.close()
                    shutil.copy(new_hdx_path, hdx_path)
                    os.remove(new_hdx_path)
            else:
                pass

    f.close()
    result_path = os.path.join(os.path.dirname(hedex_file), 'result')
    if not os.path.exists(result_path):
        os.makedirs(result_path)
    compressZip(hdx_extract_path, os.path.join(result_path, file_name))
    shutil.rmtree(hdx_extract_path)
    shutil.rmtree(real_hdx_file_path)
