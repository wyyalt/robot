#!/usr/bin/env python
# -*- coding: utf-8 -*-
#########################################################################
# Author: jonyqin
# Created Time: Thu 11 Sep 2014 03:55:41 PM CST
# File Name: Sample.py
# Description: WXBizMsgCrypt 使用demo文件
#########################################################################
# from.WXBizMsgCrypt import WXBizMsgCrypt, XMLParse
from .wx_biz_msg_crypt import WXBizMsgCrypt
import xml.etree.cElementTree as ET
import sys

if __name__ == "__main__":   
   #假设企业在企业微信后台上设置的参数如下
   sToken = "GheU9rPOdIIkU2uST0bgnu72XuP5V"
   sEncodingAESKey = "LKIDJfRjuV6LEDhvEndyvEALoDCNI8UHN67KbNWnR9Y"
   sCorpID = ""
   wxcpt=WXBizMsgCrypt(sToken,sEncodingAESKey,sCorpID)
   #sVerifyMsgSig=HttpUtils.ParseUrl("msg_signature")
   #ret = wxcpt.VerifyAESKey()
   #print ret
   sVerifyMsgSig="a631076a3f6821594d415e31d119ed2c1960c83f"
   #sVerifyTimeStamp=HttpUtils.ParseUrl("timestamp")
   sVerifyTimeStamp="1754038726"
   #sVerifyNonce=HttpUitls.ParseUrl("nonce")
   sVerifyNonce="4a67c351e995ad15"
   #sVerifyEchoStr=HttpUtils.ParseUrl("echostr")
   sVerifyEchoStr="fsi1xnbH4yQh0+PJxcOdhhK6TDXkjMyhEPA7xB2TGz6b+g7xyAbEkRxN/3cNXW9qdqjnoVzEtpbhnFyq6SVHyA=="
   sVerifyEchoStr=b'<xml><Encrypt><![CDATA[EvljUFkarSNWjIPlAUaDjI5P2OlrRVCrpab9LmcN65FH/j0Jq/91bN0dOkLfiT3VVHE/1T/fppGtNNIi2HSXqBFfvTHDB/pqPFof7ghjA9lZIXq38WnLJVh1rTWFmUQC7CG6JkvZtYH0pGMI1S1f+RnAARkGP1qDDPdmXWf5YyLNHvKLs/+H6Ug3eeWwO3CKZDp2YOB2S8jG3NBAd+bVQ2AE8To/N3bBBuPd96/SI9ly5z25ELLwe37FgPQ2yEgxtBNjVDQVNkZYA54DB2kmT/ZAtMBSEHaf8yc98LJRxL5iVSUIDJ/Qr6fuina0ePIIjYQvto3pKM08OWD6QLsGENtyBGUHF1FtWiozZA0I91jg+SM+kG0m5V0aU48G3PuOPT0dOMJjbEzCzcpcSySU1t+cEM8b1H6kvQyvwa47h8RGBxnnOkcUsgfFdkWVxPIEbjWmpQK4y/vJtY4zVooaP8NvDHksem/hql86j2fKlCS6DGZCBn09bGZm5NAa3k+eHxHLdDo5H51WRf1FirtbNt17R5hj4DTdRWdqDU56Fvub5k/y7DhdN4YSDR3cxTIuiI/lB7JD9e6gz1JJJq5oTC91WZ/RjvaVcy7b4EdC7NaRuf/vCC8GBnT48J/8rNfcMFqHgNFy8yZnWyexvoo/emwCd0AcdMxW5ywSrcIkSKoL17ogJhdtWZmNqejqiTUY1TBs+v/aYmgcdG1lEUc+BLY8BjM7yTW311Cd671dXeGZ0JjCA3D7IlfJd3ENpT4WQsbiV7y5pRs0EUHYgKDjkAjTo8M1SYTUy8aX574bw89zZBm6F1z8hmmAJp3bBL5iIWcJ+fD+fnjC4+FZZfqbDB9xfv45wOCP+LLs/PC+sHyVxBZMjsls029QtFrDFBkxVxAxImIzLuuR1QvNzM0cLF4/cCko1BljTQCY1QGQYWQ=]]></Encrypt></xml>'
   _, content = wxcpt.DecryptMsg(sVerifyEchoStr.decode("utf8"),sVerifyMsgSig,sVerifyTimeStamp, sVerifyNonce)

   root = ET.fromstring(content)
   import requests

   # 提取数据
   data = {
      # 从From节点提取信息
      'from_user_id': root.find('From/UserId').text,
      'from_name': root.find('From/Name').text,
      'from_alias': root.find('From/Alias').text,
      
      # 其他节点信息
      'webhook_url': root.find('WebhookUrl').text,
      'chat_id': root.find('ChatId').text,
      'get_chat_info_url': root.find('GetChatInfoUrl').text,
      'msg_id': root.find('MsgId').text,
      'chat_type': root.find('ChatType').text,
      'msg_type': root.find('MsgType').text,
      'content': root.find('Text/Content').text
   }
   print(data)

   # kwargs = {
   #    "chatid": data['chat_id'],
   #    "msgtype": "text",
   #    "text": {
   #          "content": f"当前会话ID为: {data['chat_id']}"
   #    }
   # }

   # requests.post(data['webhook_url'], json=kwargs)
   
   # ret,sEchoStr=wxcpt.VerifyURL(sVerifyMsgSig, sVerifyTimeStamp,sVerifyNonce,sVerifyEchoStr)
   # if(ret!=0):
   #    print("ERR: VerifyURL ret: " + str(ret))
   #    sys.exit(1)

   # print(sEchoStr)
   #验证URL成功，将sEchoStr返回给企业号
   #HttpUtils.SetResponse(sEchoStr)
   