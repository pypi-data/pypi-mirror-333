import requests
import json
import string
import random



class DoubaoConversation:
    def __init__(self,doubao_config):
        self.section_id = ""
        self.conversation_id = "0"
        if isinstance(doubao_config,dict) and "aid" in doubao_config and "device_id" in doubao_config and "sid_tt" in doubao_config and isinstance(doubao_config["aid"],int) and isinstance(doubao_config["device_id"],int) and isinstance(doubao_config["sid_tt"],str):
            self.sid_tt = doubao_config["sid_tt"]
            self.url = "https://www.doubao.com/samantha/chat/completion?aid={}&device_id={}&language=zh&region=CN&sys_region=CN".format(doubao_config["aid"],doubao_config["device_id"])
        else:
            raise Exception("doubao_config参数错误")
        
    
    def generate_hex_string(self,length):
        # 定义十六进制字符集合
        hex_chars = string.hexdigits[:16]
        # 随机选择字符并拼接成指定长度的字符串
        hex_string = ''.join(random.choice(hex_chars) for _ in range(length))
        return hex_string
    
    def generate_digits_string(self,length):
        digit_chars = string.digits[:10]
        # 随机选择字符并拼接成指定长度的字符串
        digit_string = ''.join(random.choice(digit_chars) for _ in range(length))
        return digit_string
        
    def get_text_reply(self,question="跟我打一个热情的招呼？"):
        payload = {
            "messages": [
                {
                "content": "{\"text\":\"%s\"}"%question,
                "content_type": 2001,
                "attachments": [],
                "references": []
                }
            ],
            "completion_option": {
                "is_regen": False,
                "with_suggest": False,
                "need_create_conversation": False,
                "launch_stage": 1,
                "is_replace": False,
                "is_delete": False,
                "message_from": 0,
                "event_id": "0"
            },
            "local_message_id": self.generate_hex_string(8)+"-"+self.generate_hex_string(4)+"-"+self.generate_hex_string(4)+"-"+self.generate_hex_string(4)+"-"+self.generate_hex_string(12)
        }
        if len(self.section_id)>3 and len(self.conversation_id)>3:
            payload["section_id"] = self.section_id
            payload["conversation_id"] = self.conversation_id
            payload["completion_option"]["need_create_conversation"] = False
        else:
            payload["completion_option"]["need_create_conversation"] = True
            payload["conversation_id"] ="0"
            payload["local_conversation_id"] = "local_" + self.generate_digits_string(16)
        
        headers = {
            'agw-js-conv': 'str',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
            'Cookie': f'sid_tt={self.sid_tt}',
            'Content-Type': 'application/json'
        }


        with requests.post(self.url, stream=True,headers=headers,json=payload) as response:
            if response.status_code == 200:
                for line in response.iter_lines():
                    if line:    # 忽略空行
                        decoded_line = line.decode('utf-8')
                        if decoded_line.startswith('data:'):
                            streamObj = json.loads(decoded_line[6:])
                            if "event_type" in streamObj and streamObj["event_type"] == 2001 and "event_id" in streamObj and "event_data" in streamObj:
                                event_data = streamObj["event_data"]
                                if len(event_data)>0:
                                    event_data_obj = json.loads(event_data)
                                    if "status" in event_data_obj and event_data_obj["status"] == 4:
                                        #print("*",end="") #表示收到了新数据流
                                        pass
                                    if "status" in event_data_obj and event_data_obj["status"] == 1 and "tts_content" in event_data_obj:
                                        self.conversation_id = event_data_obj["conversation_id"]
                                        self.section_id = event_data_obj["section_id"]
                                        #print("\033[K", end='')
                                        return event_data_obj["tts_content"]
        return ""







if __name__ == "__main__":
    doubao_config = {
        "aid": 123456,
        "device_id": 1234567890123456789,
        "sid_tt": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    }
    doubao = DoubaoConversation(doubao_config)
    print(doubao.get_text_reply("你是谁？"))
    print(doubao.get_text_reply("我的上一个问题是什么？"))
        



