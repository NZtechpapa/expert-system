# -*- coding:utf-8 -*-
import logging
LOG = logging.getLogger(__name__)

# 通知验证邮箱，邮件模板
TEMPLATE_VERIFY_EMAIL = u"""
"""

# 通知验证手机，短信模板
TEMPLATE_VERIFY_PHONE = u"""
"""

# 通知参与评审邮件模板，短信模板
TEMPLATE_NOTIFY_REVIEW_PROJECT = u"""尊敬的 %(expertname)s %(experttitle)s：
您已被系统抽选为项目【%(projectname)s】的评审专家。
项目评审（或验收）将于 %(pingshengshijian)s， 在 %(pingshengdidian)s 进行。
项目的负责人是：%(fuzeren)s，负责人电话为：%(fuzeren_dianhua)s。
请确认您是否能够参与该项目的评审。
"""

def send_mail(email, message):
    LOG.error(u"Send mail to %s with message %s" % (email, message))
    pass

def send_sms(mobile, message):
    LOG.error(u"Send sms to %s with message %s" % (email, message))
    pass

