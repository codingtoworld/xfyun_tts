# -*- coding: utf-8 -*-

import base64
import json
import time
import hashlib
import requests
import os.path
from sys import argv
import codecs
import subprocess


class xfyun_tts:
    api_url = "http://api.xfyun.cn/v1/service/v1/tts"   # api url
    API_KEY = "fbebb5e5550912b63b03e16491546484"        # APP KEY
    APP_ID = "5c78da89"                                 # APP ID
    OUTPUT_PATH = "./"                                  # out put path of voice file

    def __init__(self):
        """
        Params can find in https://doc.xfyun.cn/rest_api/%E8%AF%AD%E9%9F%B3%E5%90%88%E6%88%90.html
        """
        self.Param = {
            "auf": "audio/L16;rate=16000",              # voice rate
            "aue": "lame",                              # voice encoding. raw(wav) or lame(mp3)
            "voice_name": "xiaoyan",                    # xiaoyan x_xiaofeng
            "speed": "50",                              # voice speed [0,100]
            "volume": "80",                             # voice volume [0,100]
            "pitch": "50",                              # voice pitch [0,100]
            "engine_type": "aisound"                    # aisound | intp65 | intp65_en
        }

    def text_to_mp3(self, _text, _id):
        param_str = json.dumps(self.Param)              # 得到明文字符串
        param_utf8 = param_str.encode('utf8')           # 得到utf8编码(bytes类型)
        param_b64 = base64.b64encode(param_utf8)        # 得到base64编码(bytes类型)
        param_b64str = param_b64.decode('utf8')         # 得到base64字符串

        time_now = str(int(time.time()))
        checksum = (self.API_KEY + time_now + param_b64str).encode('utf8')
        checksum_md5 = hashlib.md5(checksum).hexdigest()
        header = {
            "X-Appid": self.APP_ID,
            "X-CurTime": time_now,
            "X-Param": param_b64str,
            "X-CheckSum": checksum_md5
        }

        body = {
            "text": _text
        }

        # HTTP POST
        response = requests.post(self.api_url, data=body, headers=header)
        response_head = response.headers['Content-Type']

        if response_head == "audio/mpeg":
            save_file = os.path.join(self.OUTPUT_PATH, _id + '.mp3')
            out_file = open(save_file, 'wb')
            data = response.content
            out_file.write(data)
            out_file.close()
            print('Out Put File: ' + save_file)
        else:
            print(response.content.decode('utf8'))


if __name__ == '__main__':
    text = ""
    xftts = xfyun_tts()

    if len(argv) == 1:                                          # no input file
        text = input("Please input the text：")
    else:
        text_file = argv[1]
        if os.path.isfile(text_file):
            f = codecs.open(text_file, 'r', encoding='utf-8')
            text = f.read()
            f.close()
        else:
            text = argv[1]

    _l = len(text)
    seek = 300
    i = 0
    combinf = []
    if seek >= _l:
        xftts.text_to_mp3(text, str(i))
    else:
        while seek < _l:
            txt = text[seek - 300:seek]
            xftts.text_to_mp3(txt, str(i))
            combinf.append(str(i)+'.mp3')
            i += 1
            seek += 300
            if seek >= _l:
                seek = _l
                txt = text[seek - 300:seek]
                xftts.text_to_mp3(txt, str(i))
                combinf.append(str(i)+'.mp3')
        args = 'ffmpeg.exe -i "concat:%s" -acodec copy output.mp3' % '|'.join(combinf)
        subprocess.call(args, shell=True)
