import base64
import ipaddress
import re
from urllib.parse import urlparse


class Str():
    @staticmethod
    def explode(separator, str):
        return str.split(separator)

    @staticmethod
    def addslashes(str):
        str = str.replace('\\', '\\\\')
        str = str.replace('"', '\\\"')
        str = str.replace("'", "\\\'" )
        return str

    @staticmethod
    def toToFloat(str, default=0):
        try:
            return float(str)
        except ValueError:
            return default

    @staticmethod
    def toToBool(str, default=False):
        if(str == "" or str == "0" or str == 0 or str == 'false'): return False
        try:
            return bool(str)
        except ValueError:
            return default

    @staticmethod
    def toInt(str, default=0):
        try:
            return int(str)
        except ValueError:
            return default

    @staticmethod
    def replace(str, oldStr, newStr):
        """
        字符串替换
        @param str:
        @param oldStr:
        @param newStr:
        @return:
        """
        if type(oldStr) == list:
            for val in oldStr:
                str = str.replace(val, newStr)
            return str
        else:
            return str.replace(oldStr, newStr)

    @staticmethod
    def substr(string, start, length=None):
        """
        字符串截取
        @param string:
        @param start:
        @param length:
        @return:
        """
        if length is None:
            return string[start:]
        else:
            return string[start:start + length]

    @staticmethod
    def extractUrl(content):
        """
        提取内容中的url
        :param content:
        :return:
        """
        url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        return re.findall(url_pattern, content)

    @staticmethod
    def camelize(uncamelizedWords, separator = '_'):
        """
        下划线转驼峰
        :param uncamelizedWords:
        :param separator:
        :return:
        """
        uncamelizedWords = separator+(uncamelizedWords.lower().replace(separator, " "))
        uncamelizedWords = uncamelizedWords.title()
        uncamelizedWords = uncamelizedWords.replace(" ", "")
        uncamelizedWords = uncamelizedWords.lstrip(separator)
        return uncamelizedWords[0].lower() + uncamelizedWords[1:]

    @staticmethod
    def uncamelize(camelCaps, separator = '_'):
        """
        驼峰命名转下划线命名
        :param separator:
        :return:
        """
        repl = '\\1'+separator+'\\2'
        name = re.sub('(.)([A-Z][a-z]+)', repl, camelCaps)
        return re.sub('([a-z0-9])([A-Z])', repl, camelCaps).lower()

    @staticmethod
    def ipType(ip):
        try:
            # 尝试将字符串转换为IP地址对象
            ip_addr = ipaddress.ip_address(ip)

            # 判断IP地址的类型
            if isinstance(ip_addr, ipaddress.IPv4Address):
                return 'ipv4'
            elif isinstance(ip_addr, ipaddress.IPv6Address):
                return 'ipv6'
        except ValueError:
            return None

    @staticmethod
    def parseStr(str):
        try:
            return dict(item.split('=') for item in str.split('&'))
        except Exception:
            return {}

    @staticmethod
    def base64Encode(str):
        # 将消息转换为bytes类型
        msg_bytes = str.encode('utf-8')
        # 进行base64编码
        encoded_bytes = base64.b64encode(msg_bytes)
        # 将编码后的bytes类型转换为字符串类型并返回
        return encoded_bytes.decode('utf-8')

    @staticmethod
    def base64Decode(str):
        """
        解码Base64字符串
        :param str:
        :return:
        """
        # 将编码后的字符串类型转换为bytes类型
        encoded_bytes = str.encode('utf-8')
        # 进行base64解码
        decoded_bytes = base64.b64decode(encoded_bytes)
        # 将解码后的bytes类型转换为字符串类型并返回
        return decoded_bytes.decode('utf-8')
    @staticmethod
    def parseUrl(url):


        result = urlparse(url)

        parse = {
            'scheme': result.scheme,
            'host': result.hostname,
            'path': result.path,
            'params': result.params,
            'query': result.query,
            'fragment': result.fragment,
            'username': result.username,
            'password': result.password,
            'hostname': result.hostname,
            'port': 0
        }

        if(result.netloc != "" and result.netloc != None):
            arr = Str.explode(":", result.netloc)
            parse["host"] = arr[0]
            if(len(arr) == 2):
                parse["port"] = int(arr[1])

        if (parse["port"] == 0 and result.path.isdigit()):
            parse["port"] = int(result.path)

        if(parse["host"] == "" or parse["host"] == None):
            parse["host"] = result.scheme
        return parse
    @staticmethod
    def isCarnumplate(str):
        str = str.replace("·", "")
        pattern = re.compile(r'^('
         r'[\u4e00-\u9fa5][A-Z]{1}[A-Z0-9]{4}警|'
         r'[\u4e00-\u9fa5][A-Z]{1}[A-Z0-9]{5}警|'  # 普通警车
         r'[\u4e00-\u9fa5][A-Z]{1}[A-Z0-9]{6}警|'  # 新能源警车
         
         r'应急[A-Z0-9]{4}|'
         r'应急[A-Z0-9]{5}|'
         r'应急[A-Z0-9]{6}|'
         
         r'[\u4e00-\u9fa5][A-Z]{1}[A-Z0-9]{4}应急|'
         r'[\u4e00-\u9fa5][A-Z]{1}[A-Z0-9]{5}应急|'  # 普通应急车
         r'[\u4e00-\u9fa5][A-Z]{1}[A-Z0-9]{6}应急|'  # 新能应急车
         
         r'[\u4e00-\u9fa5][A-Z]{1}[A-Z0-9]{4}学|'
         r'[\u4e00-\u9fa5][A-Z]{1}[A-Z0-9]{5}学|'  # 普通教练车
         r'[\u4e00-\u9fa5][A-Z]{1}[A-Z0-9]{6}学|'  # 新能教练车
         
         r'[军海空北沈兰济南广成][A-Z]\d{4}|'  # 军车
         r'[军海空北沈兰济南广成][A-Z]\d{5}|'  # 军车
                             
         r'(使|领)[A-Z0-9]{4}|'  # 使领馆车
         r'(使|领)[A-Z0-9]{5}|'  # 使领馆车
         r'(使|领)[A-Z0-9]{6}|'  # 使领馆车
                             
         r'[A-Z0-9]{4}(使|领)|'  # 使领馆车
         r'[A-Z0-9]{5}(使|领)|'  # 使领馆车
         r'[A-Z0-9]{6}(使|领)|'  # 使领馆车
                             
         r'[\u4e00-\u9fa5][A-Z]{1}[A-Z0-9]{4}(使|领)|'
         r'[\u4e00-\u9fa5][A-Z]{1}[A-Z0-9]{5}(使|领)|'
         r'[\u4e00-\u9fa5][A-Z]{1}[A-Z0-9]{6}(使|领)|'
                             
         r'[\u4e00-\u9fa5][A-Z]{1}[A-Z0-9]{5}|'  # 普通燃油车
         r'[\u4e00-\u9fa5][A-Z]{1}[A-Z0-9]{6}|'  # 新能源车
         r')$')

        if(bool(pattern.match(str))):
            return str
        return "";
