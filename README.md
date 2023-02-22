![img.png](logo.png)
Anything can be thought of as a process


[![License](https://img.shields.io/badge/license-Apache%202-blue.svg?style=for-the-badge&label=license)](https://www.apache.org/licenses/LICENSE-2.0.html)
[![stars](https://img.shields.io/github/stars/xhongc/streamflow?style=for-the-badge&label=stars)](https://github.com/xhongc/streamflow)

## 🚀 What is StreamFlow?
> 通过可视化的图形界面进行任务流程编排和执行的系统，一款轻量级的调度编排软件。
>
## 🎉 Features

- 标准节点：支持用户自定义作业节点
- 可视化流程编排：通过拖拽方式组合标准插件节点到一个流程模板。
- 多种流程模式：支持标准插件节点的串行、并行，支持子流程，可以根据全局参数自动选择分支执行，节点失败处理机制可配置。
- 参数引擎：支持参数共享，支持参数替换。
- 可交互的任务执行：任务执行中可以随时暂停、继续、撤销，节点失败后可以重试、跳过。
- ...
## 🔨 How to Build
### 1. 本地安装
1. 安装依赖
```shell
pip install -r requirements.txt
```
```shell
python manage.py migrate
```
2. 启动celery&beat
```shell
python manage.py celery worker -Q default,er_execute,er_schedule -l info -P gevent
python manage.py celery beat -l info
```
3. 本地运行项目
```shell
python manage.py runserver 
```
### 2. docker安装
待完成
## 👍User Interface Screenshots
### 首页
![img.png](img.png)

## 自定义节点
![img_1.png](img_1.png)
![img_2.png](img_2.png)
## 💬 Contact me
各位大佬有什么意见需求可以加Q群交流
![s](WechatIMG176.jpeg)
