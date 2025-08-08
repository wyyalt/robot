import requests
import logging
import xml.etree.cElementTree as ET

from django.http import HttpResponse
from rest_framework.views import APIView
from yixue.utils.wx_biz_msg_crypt import WXBizMsgCrypt


logger = logging.getLogger('yixue')

class RobotAPIView(APIView):

    def get_wxcpt(self, request):
        token = ""
        encoding_aes_key = ""
        wxcpt = WXBizMsgCrypt(token, encoding_aes_key, "")
        return wxcpt

    @property
    def msg_signature(self):
        return self.request.GET.get("msg_signature")
    
    @property
    def timestamp(self):
        return self.request.GET.get("timestamp")
    
    @property
    def nonce(self):
        return self.request.GET.get("nonce")
    
    @property
    def echostr(self):
        return self.request.GET.get("echostr")

    def get(self, request):
        logger.info("get request")
        
        wxcpt = self.get_wxcpt(request)
        ret, sEchoStr=wxcpt.VerifyURL(self.msg_signature, self.timestamp, self.nonce, self.echostr)
        if not ret == 0:
            logger.info("ret: {}".format(ret))

        return HttpResponse(sEchoStr)

    def post(self, request):
        content = request.body
        wxcpt = self.get_wxcpt(request)
        ret, content = wxcpt.DecryptMsg(content.decode("utf8"), self.msg_signature, self.timestamp, self.nonce)
        logger.info("e: {}".format(ret))
        logger.info("content: {}".format(content))
        root = ET.fromstring(content)

        # 提取数据
        data = {
            'from_user_id': root.find('From/UserId').text,
            'from_name': root.find('From/Name').text,
            'from_alias': root.find('From/Alias').text,
            'webhook_url': root.find('WebhookUrl').text,
            'chat_id': root.find('ChatId').text,
            'get_chat_info_url': root.find('GetChatInfoUrl').text,
            'msg_id': root.find('MsgId').text,
            'chat_type': root.find('ChatType').text,
            'msg_type': root.find('MsgType').text,
            'content': root.find('Text/Content').text
        }

        kwargs = {
            "chatid": data['chat_id'],
            "msgtype": "text",
            "text": {
                "content": f"当前会话ID为: {data['chat_id']}"
            }
        }

        requests.post(data['webhook_url'], json=kwargs)

        return HttpResponse("ok")
    