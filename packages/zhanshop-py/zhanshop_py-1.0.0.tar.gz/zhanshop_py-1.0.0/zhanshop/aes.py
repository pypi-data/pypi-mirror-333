# +----------------------------------------------------------------------
# | zhanshop-py    [ 2024/1/1 上午12:00 ]
# +----------------------------------------------------------------------
# | Copyright (c) 2011~2024 zhangqiquan All rights reserved.
# +----------------------------------------------------------------------
# | Author: Administrator <768617998@qq.com>
# +----------------------------------------------------------------------

import base64

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

from zhanshop.app import App
from zhanshop.config import Config
from zhanshop.hash import Hash
from zhanshop.log import Log


class Aes():
    key = None
    iv = None
    def __init__(self):
        appKey = App.make(Config).get("app.app_key")
        md5 = Hash.md5(appKey)
        self.key = md5[0:16].encode()
        self.iv = md5[16:32].encode()

    def encode(self, text):
        """
        aes加密
        @param text:
        @return:
        """
        text = text.encode()
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        ciphertext = cipher.encrypt(pad(text, AES.block_size))
        return base64.b64encode(ciphertext).decode('utf-8')

    def decode(self, text):
        """
        aes解密
        @param text:
        @return:
        """
        try:
            btext = base64.b64decode(text)
            cipher_dec = AES.new(self.key, AES.MODE_CBC, self.iv)
            detext = unpad(cipher_dec.decrypt(btext), AES.block_size)
            return detext.decode('utf-8')
        except Exception as e:
            App.make(Log).warn("Aes.decode("+text+") 解码错误: "+str(e))

        return ""