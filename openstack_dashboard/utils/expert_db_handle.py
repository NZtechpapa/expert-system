# -*- coding:utf-8 -*-

import logging
import os
import copy
import re
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from openstack_dashboard.utils import base_db_handle
from datetime import date, datetime
from horizon import exceptions
from openstack_dashboard import api
from openstack_dashboard import models
from openstack_dashboard.utils import sendmessages

LOG = logging.getLogger(__name__)

NO_LIMIT = -1
DEFAULT_MAX_QUERY = NO_LIMIT

STATEMAPPING = {
    'draft': u"草稿",
    'waitfor_check': u"待审核批准",
    'approved': u"已批准",
    'deleted': u"账号已删除",
}

OPERATORS_VALUE = base_db_handle.OPERATORS_VALUE
OPERATORS = base_db_handle.OPERATORS
MAINOPERATORS_VALUE = base_db_handle.MAINOPERATORS_VALUE
MAINOPERATORS = base_db_handle.MAINOPERATORS

SEARCHFIELDS_VALUE = {
    'expertname': u"姓名",
    'age': u"年龄",
    'email': u"邮箱",
    'zhicheng': u"职称",
    'zhiwu': u"职务",
    'suozaidaiwen': u"所在单位",
    'zuigaoxueli': u"最高学历",
    'zuigaoxuewei': u"最高学位",
    'gender': u"性别（F/M）",
    'chushengdi': u"出生地",
    'guoji': u"国籍",
    'jiguan': u"籍贯",
    'minzu': u"民族",
    'zhengzhimianmao': u"政治面貌",
    'biyeyuanxiao': u"毕业院校",
    'xianzhuanye': u"现从事专业",
}

SEARCHFIELDS = SEARCHFIELDS_VALUE.keys()

SEARCHPARAM = {
    'field1_choices': SEARCHFIELDS,
    'oper1_choices': OPERATORS,
    'field2_choices': SEARCHFIELDS,
    'oper2_choices': OPERATORS,
    'mainop_choices': MAINOPERATORS,
}

EXPERT_ATTR_DICT = {
    'rencaichenghaos': {'cls': models.ExpertTitle, 'keyidx': '', 'val': []},
    'zhuanjialeixings': {'cls': models.ExpertClass, 'keyidx': '', 'val': []},
    'expertdomains': {'cls': models.ExpertDomain, 'keyidx': 'domainserial', 'val': []},
    'formaljobs': {'cls': models.FormalJob, 'keyidx': 'formaljob_serial', 'val': []},
    'educations': {'cls': models.Education, 'keyidx': 'education_serial', 'val': []},
    'parttimejobs': {'cls': models.PartTimeJob, 'keyidx': 'parttimejob_serial', 'val': []},
    'reviewhistories': {'cls': models.ReviewHistory, 'keyidx': 'reviewhistory_serial', 'val': []},
    'xiangmuinfos': {'cls': models.XiangmuInfo, 'keyidx': 'xiangmuinfo_serial', 'val': []},
    'attachments': {'cls': models.Attachment, 'keyidx': 'attachment_serial', 'val': []},
}

def validate_expertid(func):
    def wrapper(expert, *args, **kwargs):
        if not isinstance(expert, models.Expert):
            if isinstance(expert, (int, str, unicode)):
                expertid = expert
                expert = GetExpertInstanceById(expertid, returnDict=False)
        if not expert or not isinstance(expert, models.Expert):
            return None
        return func(expert, *args, **kwargs)
    return wrapper

def validate_expertdict(func):
    def wrapper(expert, *args, **kwargs):
        if isinstance(expert, models.Expert):
            expertid = expert.id
        elif isinstance(expert, (int, str, unicode)):
            expertid = expert
        else:
            return None
        expert = GetExpertInstanceById(expertid, returnDict=True)
        if not expert:
            return None
        return func(expert, *args, **kwargs)
    return wrapper

def CreateExpert(**info):
    pic = info.get('picture', None)
    _expert_attr_dict = copy.deepcopy(EXPERT_ATTR_DICT)
    keys = _expert_attr_dict.keys()
    for key in keys:
        _expert_attr_dict[key]['val'] = info.get(key) or []
    tobedel_fields = ['id', 'created_at', 'picture'] + keys
    for i in tobedel_fields:
        if i in info:
            del info[i]
    info['state'] = 'draft'
    expert = ExpertSaveDB(**info)
    if pic:
        expert.picture = pic
        expert.save()
    expert_titles = _expert_attr_dict['rencaichenghaos']['val']
    if expert_titles and models.CHENGHAO_DEFAULT in expert_titles:
        expert_titles.remove(models.CHENGHAO_DEFAULT)
    for key in keys:
        val = _expert_attr_dict[key]['val']
        cls = _expert_attr_dict[key]['cls']
        for v in val:
            if key == 'rencaichenghaos':
                _ec = cls(expert=expert, rencaichenghao=v)
            elif key == 'zhuanjialeixings':
                _ec = cls(expert=expert, zhuanjialeixing=v)
            elif key == 'attachments':
                v['expert'] = expert
                CreateExpertAttachment(v, cls=cls)
                continue
            else:
                v['expert'] = expert
                _ec = cls(**v)
            _ec.save()
    return expert

def UpdateExpert(**info):
    expertid = info.get('id', None)
    if not expertid:
        return
    pic = info.get('picture', None)
    _expert_attr_dict = copy.deepcopy(EXPERT_ATTR_DICT)
    keys = _expert_attr_dict.keys()
    for key in keys:
        _expert_attr_dict[key]['val'] = info.get(key) or []
    for i in ['id', 'keystone_initial_pwd',]:
        if i in info:
            if not info[i]:
                del info[i]
    for i in keys:
        if i in info:
            del info[i]
    if pic:
        info['picture'] = ''
    models.Expert.objects.filter(id=expertid).update(**info)
    expert = GetExpertInstanceById(expertid)
    if pic:
        expert.picture = pic
        expert.save()
    for key in keys:
        val = _expert_attr_dict[key]['val']
        cls = _expert_attr_dict[key]['cls']
        keyidx = _expert_attr_dict[key]['keyidx']
        if key == 'rencaichenghaos':
            UpdateExpertTitle(expert, val)
        elif key == 'zhuanjialeixings':
            UpdateExpertClass(expert, val)
        elif key == 'attachments':
            UpdateAttachment(expert, val)
        else:
            cur = GetAllOneToManyClassData(expert, cls)
            synctable_dict(cur, val, keyidx, expert, cls)

def UpdateExpertTitle(expert, expert_titles):
    cur = GetAllExpertTitle(expert, returnNull=True)
    if expert_titles and models.CHENGHAO_DEFAULT in expert_titles:
        expert_titles.remove(models.CHENGHAO_DEFAULT)
    (tobeadd, tobedelete) = synctable(cur, expert_titles)
    for expert_title in tobeadd:
        et = models.ExpertTitle(expert=expert, rencaichenghao=expert_title)
        et.save()
    for expert_title in tobedelete:
        models.ExpertTitle.objects.filter(expert=expert, rencaichenghao=expert_title).delete()

def UpdateExpertClass(expert, expert_classes):
    cur = GetAllExpertClass(expert)
    (tobeadd, tobedelete) = synctable(cur, expert_classes)
    for expert_class in tobeadd:
        ec = models.ExpertClass(expert=expert, zhuanjialeixing=expert_class)
        ec.save()
    for expert_class in tobedelete:
        models.ExpertClass.objects.filter(expert=expert, zhuanjialeixing=expert_class).delete()

def UpdateExpertDomain(expert, expert_domains):
    cur = GetAllExpertDomain(expert)
    synctable_dict(cur, expert_domains, 'domainserial', expert, models.ExpertDomain)

def UpdateFormalJob(expert, formaljobs):
    cur = GetAllFormalJob(expert)
    synctable_dict(cur, formaljobs, 'formaljob_serial', expert, models.FormalJob)

def UpdateEducation(expert, educations):
    cur = GetAllEducation(expert)
    synctable_dict(cur, educations, 'education_serial', expert, models.Education)

def UpdatePartTimeJob(expert, ptjobs):
    cur = GetAllPartTimeJob(expert)
    synctable_dict(cur, ptjobs, 'parttimejob_serial', expert, models.PartTimeJob)

def UpdateReviewHistory(expert, rvhs):
    cur = GetAllReviewHistory(expert)
    synctable_dict(cur, rvhs, 'reviewhistory_serial', expert, models.ReviewHistory)

def UpdateXiangmuInfo(expert, xminfo):
    cur = GetAllXiangmuInfo(expert)
    synctable_dict(cur, xminfo, 'xiangmuinfo_serial', expert, models.XiangmuInfo)

def UpdateAttachment(expert, attachments):
    cur = GetAllAttachment(expert)
    synctable_dict(cur, attachments, 'attachment_serial', expert, models.Attachment,
                   create_fun=CreateExpertAttachment,
                   update_fun=UpdateExpertAttachment)

def CreateExpertAttachment(attachment, cls=models.Attachment):
    f = attachment.get('attachment_file', None)
    if not f:
        return
    del attachment['attachment_file']
    fname = attachment.get('attachment_name', '')
    if not fname:
        attachment['attachment_name'] = f.name
    _ec = cls(**attachment)
    _ec.save()
    _ec.attachment_file = f
    _ec.save()

def UpdateExpertAttachment(old_attachment, new_attachment, cls=models.Attachment):
    if not (type(old_attachment) is cls and type(new_attachment) is dict):
        return
    f = new_attachment.get('attachment_file', None)
    isUpdate = bool(new_attachment['attachment_file'] and \
                    new_attachment['attachment_file'] != old_attachment.attachment_file)
    if isUpdate:
        new_attachment['attachment_file'] = ''
        fname = new_attachment.get('attachment_name', '')
        if not fname:
            new_attachment['attachment_name'] = f.name
    else:
        fname = new_attachment.get('attachment_name', '')
        if not fname:
            new_attachment['attachment_name'] = os.path.basename(old_attachment.attachment_file)
    _ec = cls(**new_attachment)
    _ec.save()
    if isUpdate:
        _ec.attachment_file = f
        _ec.save()

def synctable(current, new):
    tobeadd = []
    tobedelete = copy.deepcopy(current)
    for n in new:
        if n in current:
            tobedelete.remove(n)
        else:
            tobeadd.append(n)
    return (tobeadd, tobedelete)

def synctable_dict(current, new, keyword, expert, cls, create_fun=None, update_fun=None):
    tobecreated = []
    tobeupdated = []
    new_dict = {}
    keys = [ n[keyword] for n in new ]

    # Construct the key array for new data
    for n in new:
        new_dict[n[keyword]] = n

    # If the old key not in the new key array, delete the old data
    # Else try to update it
    for c in current:
        key = eval("c.%s" % keyword)
        if not key in keys:
            c.delete()
        else:
            keys.remove(key)
            n = new_dict[key]
            n['id'] = c.id
            n['expert'] = expert
            tobeupdated.append((c, n))

    # If the new key not in the old data, try to create it
    for key in keys:
        n = new_dict[key]
        n['expert'] = expert
        tobecreated.append(n)

    for (c, n) in tobeupdated:
        if not update_fun:
            ec = cls(**n)
            ec.save()
        else:
            update_fun(c, n, cls=cls)

    for n in tobecreated:
        if not create_fun:
            ec = cls(**n)
            ec.save()
        else:
            create_fun(n, cls=cls)

def ExpertSaveDB(**info):
    try:
        expert = models.Expert(**info)
        expert.save()
        return expert
    except Exception,e:
        raise Exception(u"数据库保存失败，错误消息：%s" % e.message)

# TODO add decorator to replace the start,length logic
def GetExperts(start=0, length=DEFAULT_MAX_QUERY):
    if length == NO_LIMIT and start == 0:
        return models.Expert.objects.all()
    elif length == NO_LIMIT:
        return models.Expert.objects.all()[start:]
    else:
        return models.Expert.objects.all()[start:(start+length)]

def FilterExperts(start=0, length=DEFAULT_MAX_QUERY, **args):
    if length == NO_LIMIT and start == 0:
        return models.Expert.objects.filter(**args)
    elif length == NO_LIMIT:
        return models.Expert.objects.filter(**args)[start:]
    else:
        return models.Expert.objects.filter(**args)[start:(start+length)]

def get_initial_user_data(GetRequest, default=False):
    if default:
        default = {
            'field1': 'expertname',
            'oper1': 'exact',
            'field2': 'zuigaoxueli',
            'oper2': 'exact',
        }
    else:
        default = None
    return base_db_handle.get_initial_user_data(
               GetRequest,
               SEARCHFIELDS,
               OPERATORS,
               MAINOPERATORS,
               default=default)

def get_birthday(today, age):
    try:
        born = today.replace(year=(today.year-age))
    except ValueError: # raised when birth date is February 29 and the current year is not a leap year
        born = today.replace(year=(today.year-age), month=2, day=28)
    return born

def dict2filter(filters, d):
    for key in d:
        filter_adapt(filters, key, 'exact', d[key])

def filter_adapt(f, v, o, w):
    if v != 'age':
        f.append({'var': v, 'operator': o, 'words': w})
        return
    if not o in ['exact', 'gt', 'gte', 'lt', 'lte']:
        return
    try:
        age = int(w)
    except ValueError:
        return
    today = date.today()
    if age < 0 or (o == 'gt' and age == 0) or (age + 2) > today.year:
        return
    var = 'born'
    if o in ['gt', 'gte']:
        """
        Assuming today is 2020-02-29
        Man who born <= 2016-02-29                   is 4+ years old
        Man who born <= 2017-02-28                   is 3+ years old
        Man who born <= 2018-02-28                   is 2+ years old
        """
        if o == 'gt':
            age = age + 1
        oper = 'lte'
        born = get_birthday(today, age)
        f.append({'var': var, 'operator': oper, 'words': born})
    elif o in ['lt', 'lte']:
        """
        Assuming today is 2020-02-29
        Man who born >   2015-02-28                   is 4- year
        Man who born >   2016-02-29                   is 3- year
        Man who born >   2017-02-28                   is 2- year
        """
        if o == 'lte':
            age = age + 1
        oper = 'gt'
        born = get_birthday(today, age)
        f.append({'var': var, 'operator': oper, 'words': born})
    else:
        """
        Assuming today is 2020-02-29
        Man who born <= 2016-02-29                   is 4+ years old
        Man who born >  2015-02-28                   is 4- year
        Man who born    2015-02-28 < X <= 2016-02-29 is 4  years old

        Man who born <= 2017-02-28                   is 3+ years old
        Man who born >  2016-02-29                   is 3- year
        Man who born    2016-02-29 < X <= 2017-02-28 is 3  years old

        Man who born <= 2018-02-28                   is 2+ years old
        Man who born >  2017-02-28                   is 2- year
        Man who born    2017-02-28 < X <= 2018-02-28 is 2  years old
        """
        oper = 'gt'
        born = get_birthday(today, age + 1)
        f.append({'var': var, 'operator': oper, 'words': born})

        oper = 'lte'
        born = get_birthday(today, age)
        f.append({'var': var, 'operator': oper, 'words': born})

def generate_filter(user_data):
    return base_db_handle.generate_filter(user_data, filter_adapt)

def generateCondition(filter_words):
    return base_db_handle.generateCondition(filter_words)

def generateConditions(filters_words):
    return base_db_handle.generateConditions(filter_words)

def QueryExperts(filters1, filters2=[], operator='', excluders=[], start=0, length=DEFAULT_MAX_QUERY):
    return base_db_handle.QueryTable(
               GetExperts,
               FilterExperts,
               filters1,
               filters2=filters2,
               operator=operator,
               excluders=excluders,
               start=start,
               length=length)

def DomainBasedQueryExperts(domains, filters=[], excluders=[]):
    res = []
    sql_filters = {}
    sql_excluders = []
    if filters:
        sql_filters = base_db_handle.generateConditions(filters)
    for excluder in excluders:
        sql_excluders.append(base_db_handle.generateConditions(excluder))
    if isinstance(domains, (str, unicode)):
        sql_filters['expertdomain__domainname__exact'] = domains
    elif isinstance(domains, list) and len(domains) is 1:
        sql_filters['expertdomain__domainname__exact'] = domains[0]
    elif isinstance(domains, list):
        regex_str = '|'.join(domains)
        sql_filters['expertdomain__domainname__regex'] = regex_str
    res = FilterExperts(start=0, length=NO_LIMIT, **sql_filters)
    for sql_excluder in sql_excluders:
        res = res.exclude(**sql_excluder)
    return res

def SubmitExpertInfo(expertid):
    return ChangeExpertState(expertid, ['draft'], 'waitfor_check')

def WithdrawExpertReq(expertid):
    return ChangeExpertState(expertid, ['waitfor_check', 'approved',], 'draft')

def CheckExpertInfo(expertid):
    return ChangeExpertState(expertid, ['waitfor_check'], 'approved')

@validate_expertid
def AccountCreated(expert, new_user):
    expert.keystone_uuid = new_user.id
    expert.save()
    return expert

def DeleteExpertRecord(expertid):
    return ChangeExpertState(expertid, ['draft', 'waitfor_check', 'approved',], 'deleted', delete=True)

@validate_expertid
def DeleteExpertFromDB(expert):
    expert.delete()

def GetExpertInstanceByKeystoneUsername(username):
    info = {'keystone_username': username}
    return FilterExperts(**info)

def GetExpertInstanceById(expertid, returnDict=False):
    return base_db_handle.GetInstanceById(models.Expert, expertid, returnDict=returnDict)

def GetAllOneToManyClassData(expert, Class, returnDict=False):
    if isinstance(expert, models.Expert):
        result = Class.objects.filter(expert__id=expert.id)
    elif isinstance(expert, (str, int, unicode)):
        result = Class.objects.filter(expert__id=expert)
    else:
        return []
    if returnDict:
        return result.values()
    else:
        return result

def GetAllExpertTitle(expert, returnNull=False):
    result = GetAllOneToManyClassData(expert, models.ExpertTitle)
    if result:
        return [t.rencaichenghao for t in result]
    elif returnNull:
        return []
    else:
        return [models.CHENGHAO_DEFAULT]

def GetAllExpertClass(expert):
    result = GetAllOneToManyClassData(expert, models.ExpertClass)
    if result:
        return [t.zhuanjialeixing for t in result]
    else:
        return []

def GetAllExpertDomain(expert, returnDict=False):
    return GetAllOneToManyClassData(expert, models.ExpertDomain, returnDict=returnDict)

def GetAllFormalJob(expert, returnDict=False):
    return GetAllOneToManyClassData(expert, models.FormalJob, returnDict=returnDict)

def GetAllEducation(expert, returnDict=False):
    return GetAllOneToManyClassData(expert, models.Education, returnDict=returnDict)

def GetAllPartTimeJob(expert, returnDict=False):
    return GetAllOneToManyClassData(expert, models.PartTimeJob, returnDict=returnDict)

def GetAllReviewHistory(expert, returnDict=False):
    return GetAllOneToManyClassData(expert, models.ReviewHistory, returnDict=returnDict)

def GetAllXiangmuInfo(expert, returnDict=False):
    return GetAllOneToManyClassData(expert, models.XiangmuInfo, returnDict=returnDict)

def GetAllAttachment(expert, returnDict=False):
    return GetAllOneToManyClassData(expert, models.Attachment, returnDict=returnDict)

@validate_expertid
def ChangeExpertState(expert, from_states, to_state, delete=False):
    if type(from_states) is str:
        from_states = [from_states]
    if not expert.state in from_states:
        return None
    expert.state = to_state
    if delete:
        now = datetime.now()
        expert.deleted_at = now
    expert.save()
    return expert

def generate_slices_fields(src_fields, num):
    result = ()
    for i in range(1, 1 + num):
        for src in src_fields:
            result += ("%s%d" %(src, i),)
    return result

def get_expertid_from_keystone_user(request, redirect=None):
    expertid = None
    try:
        user = api.keystone.user_get(request, request.user.id, admin=False)
        expertid = getattr(user, 'expertid', None)
    except Exception:
        if redirect:
            exceptions.handle(request,
                              _('Unable to retrieve user information.'),
                              redirect=redirect)
            return None

    if not expertid and redirect:
        try:
            raise exceptions.NotFound(_('Can not find index in the expert table for the current user'))
        except Exception:
            exceptions.handle(request,
                              u"非法用户",
                              redirect=redirect)
    return expertid

def get_all_expert_names(experts):
    names = [ e.expertname if e.expertname else u"无名氏（%d）" % e.id for e in experts ]
    return ', '.join(names)

def format_value(val):
    if not val:
        rst = u"＜空＞"
    elif isinstance(val, str):
        rst = format_str(val)
    elif isinstance(val, date):
        rst = format_date(val)
    elif isinstance(val, datetime):
        rst = format_datetime(val)
    else:
        rst = val
    return rst

def format_date(val):
    return u"%04d年%02d月%02d日" % (val.year, val.month, val.day)

def format_datetime(now):
    return u"%04d年%02d月%02d日%02d点%02d分%02d秒" % (now.year, now.month, now.day,
                                                      now.hour, now.minute, now.second)

def format_str(val):
    return unicode(val, "utf-8")

def generate_notify_info(expertinfo, project_info={}):
    info = {}
    _title_patten_boshi = re.compile(ur".*博士.*")
    _title_patten_jiaoshou = re.compile(ur".*教授.*")
    for key in expertinfo:
        if key == 'id':
            continue
        val = expertinfo[key]
        val = format_value(val)
        if key == 'gender' and not 'experttitle' in info:
            if val == u"男":
                info['experttitle'] = u"先生"
            elif val == u"女":
                info['experttitle'] = u"女士"
        elif key in ['zuigaoxueli', 'zuigaoxuewei', 'zhicheng']:
            if _title_patten_boshi.match(val):
                info['experttitle'] = u"博士"
            elif _title_patten_jiaoshou.match(val):
                info['experttitle'] = u"教授"
        info[key] = val
    if not 'experttitle' in info:
        info['experttitle'] = u""

    for key in project_info:
        if key == 'id':
            continue
        val = project_info[key]
        val = format_value(val)
        info[key] = val
    return info

@validate_expertdict
def notify_expert(expert, mseeage_template, project_info={}):
    info = generate_notify_info(expert, project_info=project_info)
    message = mseeage_template % info
    if expert['email']:
        sendmessages.send_mail(expert['email'], message)
    if expert['mobile']:
        sendmessages.send_sms(expert['mobile'], message)
    return True

def test_import_data():
    for i in range(1,21):
        y = 1960 + ((i*2) % 48)
        m = (i % 12) + 1
        d = i % 28
        email="expert%d@test%d.com" % (i, i)
        e = {'expertname': "expert%02d" % i,
             'born': date(y, m, d),
             'email': email,
             'keystone_username': email,
             'keystone_initial_pwd': email,
             'suozaidaiwei': u"单位%d" % (i % 5),
             'expertdomains': [
                 {'domainserial': 1, 'domainname': u"领域%d" % (i % 3 + 10),
                  'domainkeywords': 'kw%d' % (i % 3 + 10), 'domaintype': models.DOMAIN_TYPE[0][0] },
                 {'domainserial': 2, 'domainname': u"领域%d" % (i % 3 + 20),
                  'domainkeywords': 'kw%d' % (i % 3 + 10), 'domaintype': models.DOMAIN_TYPE[1][0] },
                 {'domainserial': 3, 'domainname': u"领域%d" % (i % 3 + 30),
                  'domainkeywords': 'kw%d' % (i % 3 + 10), 'domaintype': models.DOMAIN_TYPE[2][0] },
                 {'domainserial': 4, 'domainname': u"领域%d" % (i % 3 + 40),
                  'domainkeywords': 'kw%d' % (i % 3 + 10), 'domaintype': models.DOMAIN_TYPE[3][0] },
             ]
            }
        _expert = CreateExpert(**e)
        SubmitExpertInfo(_expert)
        CheckExpertInfo(_expert)

def test1():
    ud1 = {
        'field1': 'name',
        'oper1': 'icontains',
        'value1': 'expert',
        'field2': 'age',
        'oper2': 'exact',
        'value2': '30',
        'mainop': 'and',}
    flt1 = generate_filter(ud1)
    (filters1, filters2, operator) = flt1
    return QueryExperts(filters1, filters2, operator)

def test2():
    ud1 = {
	'field1': 'name',
	'oper1': 'icontains',
	'value1': '专家',
	'field2': 'age',
	'oper2': 'gt',
	'value2': '12',
	'mainop': 'and',}
    flt1 = generate_filter(ud1)
    (filters1, filters2, operator) = flt1
    return QueryExperts(filters1, filters2, operator)

def test3():
    ud1 = {
        'field1': 'name',
        'oper1': 'icontains',
        'value1': 'expert1',
        'field2': 'age',
        'oper2': 'gt',
        'value2': '18',
        'mainop': 'or',}
    flt1 = generate_filter(ud1)
    (filters1, filters2, operator) = flt1
    return QueryExperts(filters1, filters2, operator)

def test4():
    ud1 = {
        'field1': 'name',
        'oper1': 'icontains',
        'value1': 'expert',
        'field2': 'age',
        'oper2': 'gt',
        'value2': '13',
        'mainop': 'exclude',}
    flt1 = generate_filter(ud1)
    (filters1, filters2, operator) = flt1
    return QueryExperts(filters1, filters2, operator)

def test5():
    ud1 = {
        'field1': 'name',
        'oper1': 'contains',
        'value1': 'expert',
        'field2': 'age',
        'oper2': 'gt',
        'value2': '29',
        'mainop': 'and',}
    flt1 = generate_filter(ud1)
    (filters1, filters2, operator) = flt1
    return QueryExperts(filters1, filters2, operator)

def test6():
    ud1 = {
        'field1': 'name',
        'oper1': 'contains',
        'value1': 'expert',
        'field2': 'email',
        'oper2': 'contains',
        'value2': 'expert1',
        'mainop': 'and',}
    flt1 = generate_filter(ud1)
    (filters1, filters2, operator) = flt1
    return QueryExperts(filters1, filters2, operator)

