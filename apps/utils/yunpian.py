"""
云片网发送短信
注意要把服务器的对外ip设置到ip白名单里
"""
import json
import requests
from MxShop_Back.privacy import YUNPIAN_KEY
from MxShop_Back.privacy import MY_MOBILE


class YunPian(object):
    """云片网发送短信工具类"""

    def __init__(self, api_key):
        """构造器"""
        self.api_key = api_key
        # 单条短信接口
        self.single_send_url = "https://sms.yunpian.com/v2/sms/single_send.json"

    def send_sms(self, code, mobile):
        """向moblie发送验证码为code的短信"""
        parmas = {
            "apikey": self.api_key,
            "mobile": mobile,
            "text": "【刘知昊短信测试】您的验证码是{code}。如非本人操作，请忽略本短信。".format(code=code)
        }
        # 返回三方接口调用的response的序列化
        response = requests.post(self.single_send_url, data=parmas)
        re_dict = json.loads(response.text)
        return re_dict


if __name__ == "__main__":
    # 这里设置自己的api-key
    yun_pian = YunPian(YUNPIAN_KEY)
    yun_pian.send_sms("2019", MY_MOBILE)
