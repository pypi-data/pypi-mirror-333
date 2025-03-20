## 简介

pydoubao是一个用于与 Doubao（一个智能助手平台）进行对话的 Python 类模块。该模块允许开发者通过发送 HTTP 请求与 Doubao 进行交互，获取或发送文本消息。
相比于Doubao的官方 SDK，pydoubao具有以下优势：
- 免费！官方 SDK 百万token费用约$1，处理几十个文件就用完了。pydoubao 免费！
- 支持 Python 3.6+
- 支持异步发送消息
- 支持发送图片消息

## 功能

DoubaoConversation 类的构造函数接受一个包含配置信息的字典，用于建立与 Doubao 的连接。
DoubaoConversation 类的get_text_reply 方法用于发送文本消息到 Doubao，并接收回复。

## 使用示例

以下是如何使用 DoubaoConversation 类与 Doubao 进行对话的示例：
```python
import pydoubao
doubao_config = {
    "aid": 497858,
    "device_id": 7475662593640072704,
    "sid_tt": "cbe1cdc0db5c1e191c94246e2d44a30f"
}
doubao = pydoubao.DoubaoConversation(doubao_config)
print(doubao.get_text_reply("你是谁？"))
print(doubao.get_text_reply("我的上一个问题是什么？"))
```
其输出如下：
```code
我是豆包，很高兴能和你交流并为你提供帮助！ 
你的上一个问题是“你是谁？”
```
## aid、device_id 和 sid_tt 的获取
aid以及device_id获取方式：
![image](http://img.liuwenhao.ink/shared/aid-get.png)
sid_tt获取方式：
![image](http://img.liuwenhao.ink/shared/sid_tt.png)