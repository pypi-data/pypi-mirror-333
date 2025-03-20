# 初始化ptools工具类

# 导入必要的模块
import time
import json
import base64
import requests
import yaml
import subprocess
import os


# 时间处理类
class TimeUtils:
    @staticmethod
    def get_current_time(format_str='%Y-%m-%d %H:%M:%S'):
        return time.strftime(format_str, time.localtime())


# 字符串处理类
class StringUtils:
    @staticmethod
    def reverse_string(s):
        return s[::-1]


# U2自动化封装类
class U2Utils:
    def __init__(self):
        pass

    def start_u2(self):
        # 这里是U2自动化启动逻辑
        pass


# adb操作类
class AdbUtils:
    def __init__(self):
        pass

    def adb_command(self, command):
        result = subprocess.run(['adb'] + command.split(), capture_output=True, text=True)
        return result.stdout


# pc cmd操作类
class PCCmdUtils:
    def __init__(self):
        pass

    def run_cmd(self, command):
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.stdout


# adb logcat类
class AdbLogcatUtils:
    def __init__(self):
        pass

    def get_logcat(self):
        result = subprocess.run(['adb', 'logcat', '-d'], capture_output=True, text=True)
        return result.stdout


# ymal文件读写类
class YamlUtils:
    @staticmethod
    def read_yaml(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)

    @staticmethod
    def write_yaml(file_path, data):
        with open(file_path, 'w', encoding='utf-8') as f:
            yaml.safe_dump(data, f, allow_unicode=True)


# request封装类
class RequestUtils:
    @staticmethod
    def get(url, params=None):
        response = requests.get(url, params=params)
        return response.json()

    @staticmethod
    def post(url, data=None):
        response = requests.post(url, json=data)
        return response.json()


# 本地文件读写类
class FileUtils:
    @staticmethod
    def read_file(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()

    @staticmethod
    def write_file(file_path, content):
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)


# 图片和base64互转类
class ImageBase64Utils:
    @staticmethod
    def image_to_base64(file_path):
        with open(file_path, 'rb') as f:
            return base64.b64encode(f.read()).decode('utf-8')

    @staticmethod
    def base64_to_image(base64_str, file_path):
        with open(file_path, 'wb') as f:
            f.write(base64.b64decode(base64_str))