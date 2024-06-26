import  datetime
import hashlib
import base64
import json
#发送短信脚本
import requests  #发http/https请求
#根据https://doc.yuntongxun.com/pe/5a533de33b8496dd00dce07c容联云文档编写
#短信接入
class YunTongXin():
    base_url = 'https://app.cloopen.com:8883'   #相当于请求头中的host  host+url为完整的请求地址

    def __init__(self,accountSid,accountToken, appId,templateId):
        self.accountSid = accountSid #账户ID
        self.accountToken = accountToken  #授权令牌
        self.appId = appId  #应用id
        self.templateId = templateId #模板id

    def get_request_url(self,sig):    #url为请求网址，请求地址为请求网址后面加的路径
        #/2013-12-26/Accounts/{accountSid}/SMS/{funcdes}?sig={SigParameter} 业务url
        #完整的url为base_url+业务url
        self.url = self.base_url + '/2013-12-26/Accounts/%s/SMS/TemplateSMS?sig=%s'%(self.accountSid,sig)
        return self.url

    def get_timestamp(self):  #生成时间戳
        return datetime.datetime.now().strftime('%Y%m%d%H%M%S')

    def get_sig(self,timestamp):
        #生成业务url中的sig
        s = self.accountSid + self.accountToken + timestamp
        m = hashlib.md5()  #md5处理，使用hashlib
        m.update(s.encode())
        return  m.hexdigest().upper()

    def get_request_header(self,timestamp):
        #生成请求头
        s = self.accountSid + ':' + timestamp
        auth = base64.b64encode(s.encode()).decode()   #base64编码之后是字节串，使用decode方法转化为字符串
        return {
            'Accept':'application/json',
            'Content-Type':'application/json;charset=utf-8',
            'Authorization':auth
        }

    def get_request_body(self,phone,code):  #请求体，要传的参数
        return {
            "to": phone,
            "appId": self.appId,
            "templateId": self.templateId,
            "datas": [code, "3"]   #code验证码3分钟内有效
        }

    def request_api(self,url,header,body):
        res= requests.post(url, headers=header, data=body)
        return res.text


    def run(self,phone,code):  #执行函数
        #获取时间戳
        timestamp = self.get_timestamp()
        #生成签名
        sig = self.get_sig(timestamp)
        #生成业务url
        url = self.get_request_url(sig)
        # print(url)
        #生成请求头
        header = self.get_request_header(timestamp)
        # print(header)
        #生成请求体
        body = self.get_request_body(phone,code)
        #发请求
        data = self.request_api(url,header,json.dumps(body))
        return data

if __name__ == '__main__':  #验证脚本
    #accountSid,accountToken, appId,templateId
    config = {
        "accountSid":"8aaf0708837e29e601838901ec26025c",
        "accountToken":"0e243c7fb930434d8517d57cfb6e7202",
        "appId": "8aaf0708837e29e601838901ed1f0263",
        "templateId": "1"
    }
    yun = YunTongXin(**config)  #**变为关键字传参
    res= yun.run("15636910352", "021227")
    print(res)


