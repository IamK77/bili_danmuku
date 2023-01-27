# bili_danmuku

## 使用

建议使用虚拟环境运行

`pip install virtualenv`

`virtualenv -p python3.9 .venv`

在当前根目录执行以下指令

``.venv\Scripts\activate``

进入虚拟环境来运行程序

``pip install -r requirements.txt``

安装依赖的第三方库

运行``python start_danmu.py``

## 配置

首次运行会生成config.yaml文件, 填写配置项再次运行即可

MySQL中若没有指定表名会自动生成表

## TODO

支持sqlite

提升程序稳定性
