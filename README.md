# Python 调用科大讯飞语音合成接口，实现文字转语音

## 注册科大讯飞账户

1、注册科大讯飞账户，然后新建一个应用，使用“在线语音合成”服务

2、使用WEBAPI调用方式,系统将分配APPID和APPKEY

3、将自己的外网ip地址添加白名单

## 使用
1、安装Python环境（开发环境是Python 3.6），下载本项目main.py程序

2、将系统将分配APPID和APPKEY替换掉代码中的对应值

3、[下载ffmpeg软件](https://www.ffmpeg.org/download.html)，用于超长文件的多音频文件合并。

3、准备好文本


### 命令行输入文本

直接运行：python main.py

系统将提示你输入文本，运行结束后，即可看到生成的mp3文件；


### 使用文件输入

运行：python main.py 文本文件名

系统将自动运行并对超长的文本进行分割

