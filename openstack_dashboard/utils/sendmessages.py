# -*- coding:utf-8 -*-
import logging
LOG = logging.getLogger(__name__)

import sys
from aliyunsdkdysmsapi.request.v20170525 import SendSmsRequest
from aliyunsdkdysmsapi.request.v20170525 import QuerySendDetailsRequest
from aliyunsdkcore.client import AcsClient
import uuid
from aliyunsdkcore.profile import region_provider
from aliyunsdkcore.http import method_type as MT
from aliyunsdkcore.http import format_type as FT
import const

"""
短信业务调用接口示例，版本号：v20170525

Created on 2017-06-12

"""
try:
    reload(sys)
    sys.setdefaultencoding('utf8')
except NameError:
    pass
except Exception as err:
    raise err

# 注意：不要更改
REGION = "cn-hangzhou"
PRODUCT_NAME = "Dysmsapi"
DOMAIN = "dysmsapi.aliyuncs.com"

acs_client = AcsClient(const.ACCESS_KEY_ID, const.ACCESS_KEY_SECRET, REGION)
region_provider.add_endpoint(PRODUCT_NAME, REGION, DOMAIN)


# 通知验证邮箱，邮件模板
TEMPLATE_VERIFY_EMAIL = u"""
"""

# 通知验证手机，短信模板
TEMPLATE_VERIFY_PHONE = u"""
"""

# 通知参与评审邮件模板，短信模板
TEMPLATE_NOTIFY_REVIEW_PROJECT = u"""%(expertname)s|%(projectname)s|%(pingshengshijian)s|%(pingshengdidian)s|%(fuzeren)s|%(fuzeren_dianhua)s"""

def send_mail(email, message):
    LOG.error(u"Send mail to %s with message %s" % (email, message))
    pass

def send_sms(mobile, message):
    LOG.error(u"Send sms to %s with message %s" % (mobile, message))
    __business_id = uuid.uuid1()
    # print(__business_id)
    messages = message.split("|")
    params = "{\"expertname\":\""+messages[0]+"\",\"projectname\":\""+messages[1]+"\",\"pingshengshijian\":\""+messages[2]+"\",\"pingshengdidian\":\""+messages[3]+"\",\"fuzeren\":\""+messages[4]+"\",\"fuzeren_dianhua\":\""+messages[5]+"\"}"
    # params = u'{"name":"wqb","code":"12345678","address":"bz","phone":"13000000000"}'
    LOG.error(send_sms(__business_id, mobile, "兰州市科学技术局", "SMS_145599426", params))

    pass




def send_sms(business_id, phone_numbers, sign_name, template_code, template_param=None):
    smsRequest = SendSmsRequest.SendSmsRequest()
    # 申请的短信模板编码,必填
    smsRequest.set_TemplateCode(template_code)

    # 短信模板变量参数
    if template_param is not None:
        smsRequest.set_TemplateParam(template_param)

    # 设置业务请求流水号，必填。
    smsRequest.set_OutId(business_id)

    # 短信签名
    smsRequest.set_SignName(sign_name)

    # 数据提交方式
    # smsRequest.set_method(MT.POST)

    # 数据提交格式
    # smsRequest.set_accept_format(FT.JSON)

    # 短信发送的号码列表，必填。
    smsRequest.set_PhoneNumbers(phone_numbers)

    # 调用短信发送接口，返回json
    smsResponse = acs_client.do_action_with_exception(smsRequest)

    # TODO 业务处理

    return smsResponse






