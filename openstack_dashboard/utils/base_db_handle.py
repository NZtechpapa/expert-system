# -*- coding:utf-8 -*-

import logging
from datetime import date, datetime

LOG = logging.getLogger(__name__)

NO_LIMIT = -1
DEFAULT_MAX_QUERY = NO_LIMIT

OPERATORS_VALUE = {
    'exact': u"=（等于）",
    'gt': u"＞（大于）",
    'gte': u"≥（大于或等于）",
    'lt': u"＜（小于）",
    'lte': u"≤（小于或等于）",
    'iexact': u"字符串相等（忽略大小写）",
    'contains': u"包含（字符）",
    'icontains': u"包含（忽略大小写）",
    'regex': u"匹配正则表达式",
    'iregex': u"匹配正则表达式（忽略大小写）",
    'startswith': u"以字符串开头",
    'endswith': u"以字符串结尾",
    'istartswith': u"以字符串开头（忽略大小写）",
    'iendswith': u"以字符串结尾（忽略大小写）",
}

OPERATORS = [
    'exact',
    'gt',
    'gte',
    'lt',
    'lte',
    'iexact',
    'contains',
    'icontains',
    'regex',
    'iregex',
    'startswith',
    'endswith',
    'istartswith',
    'iendswith',
]

MAINOPERATORS_VALUE = {
    'and': u"与",
    'or': u"或",
    'exclude': u"排除",
}

MAINOPERATORS = [
    'and',
    'or',
    'exclude',
]

def get_initial_user_data(GetRequest, searchfields, operators, mainoperators, default=None):
    field1 = GetRequest.get('field1', '')
    oper1 = GetRequest.get('oper1', '').lower()
    value1 = GetRequest.get('value1', '')
    field2 = GetRequest.get('field2', '')
    oper2 = GetRequest.get('oper2', '').lower()
    value2 = GetRequest.get('value2', '')
    mainop = GetRequest.get('mainop', '')
    user_data = {}
    if not default:
        if not (field1 in searchfields and oper1 in operators and value1):
            return user_data
        elif not (field2 in searchfields and oper2 in operators and value2 and mainop in mainoperators):
            user_data = {
                'field1': field1,
                'oper1': oper1,
                'value1': value1,}
            return user_data
    else:
        # Give default value
        if field1 not in searchfields:
            field1 = default['field1']
            oper1 = default['oper1']
        elif oper1 not in operators:
            oper1 = default['oper1']
        if field2 not in searchfields:
            field2 = default['field2']
            oper2 = default['oper2']
        elif oper2 not in operators:
            oper2 = default['oper2']
        if mainop not in mainoperators:
            mainop = ""
    user_data = {
        'field1': field1,
        'oper1': oper1,
        'value1': value1,
        'field2': field2,
        'oper2': oper2,
        'value2': value2,
        'mainop': mainop,}
    return user_data

def generate_filter(user_data, filter_adapt_fun):
    filters1 = []
    filters2 = []
    operator = ''
    if 'filter' in user_data:
        _filter = user_data['filter']
        if type(_filter) is dict:
            filters1 = [_filter]

    if not user_data['field1']:
        return (filters1, filters2, operator)
    else:
        field1 = user_data['field1']
        oper1 = user_data['oper1']
        value1 = user_data['value1']
        filter_adapt_fun(filters1, field1, oper1, value1)

    if not 'mainop' in user_data or not 'field2' in user_data or \
       not user_data['field2'] or not user_data['mainop']:
        return (filters1, filters2, operator)
    else:
        field2 = user_data['field2']
        oper2 = user_data['oper2']
        value2 = user_data['value2']
        filter_adapt_fun(filters2, field2, oper2, value2)
        operator = user_data['mainop']

    return (filters1, filters2, operator)

def generateCondition(filter_words):
    condition = {}
    var = filter_words.get('var', None)
    operator = filter_words.get('operator', None)
    words = filter_words.get('words', None)
    if var and words and operator in OPERATORS:
        condition["%s__%s" % (var, operator)] = words
    return condition

def generateConditions(filters_words):
    conditions = []
    filters = {}

    if type(filters_words) is dict:
        return generateCondition(filters_words)
    if type(filters_words) is not list:
        return filters
    for filter_words in filters_words:
        var = filter_words.get('var', None)
        operator = filter_words.get('operator', None)
        words = filter_words.get('words', None)
        if var and words and (operator in OPERATORS):
            if (var, operator) in conditions:
                continue
            conditions.append( (var, operator) )
            filters["%s__%s" % (var, operator)] = words
    return filters

def QueryTable(GetFunc, FilterFunc, filters1, filters2=[], operator='', excluders=[], start=0, length=DEFAULT_MAX_QUERY):
    _res = []
    if not filters1 or not type(filters1) in [list, dict]:
        _res = GetFunc(start=0, length=NO_LIMIT)
        return ExcludeTable(_res, excluders=excluders, start=start, length=length)
    condition1 = generateConditions(filters1)
    if not condition1:
        _res = GetFunc(start=0, length=NO_LIMIT)
        return ExcludeTable(_res, excluders=excluders, start=start, length=length)

    if not filters2 or not type(filters2) in [list, dict] or not operator in ['and', 'or', 'exclude']:
        _res = FilterFunc(start=0, length=NO_LIMIT, **condition1)
        return ExcludeTable(_res, excluders=excluders, start=start, length=length)
    condition2 = generateConditions(filters2)
    if not condition2:
        _res = FilterFunc(start=0, length=NO_LIMIT, **condition1)
        return ExcludeTable(_res, excluders=excluders, start=start, length=length)

    # filters1 is dict or list, and valid
    # filters2 is dict or list, and valid
    # Query both filters1 and filters2 are fulfilled
    if operator == 'and':
        filters = []
        if type(filters1) is dict:
            filters.append(filters1)
        else:
            filters.extend(filters1)
        if type(filters2) is dict:
            filters.append(filters2)
        else:
            filters.extend(filters2)
        conditions = generateConditions(filters)
        _res = FilterFunc(start=0, length=NO_LIMIT, **conditions)
    elif operator == 'or':
        res1 = FilterFunc(start=0, length=NO_LIMIT, **condition1)
        res2 = FilterFunc(start=0, length=NO_LIMIT, **condition2)
        _res = res1 | res2
    elif operator == 'exclude':
        res1 = FilterFunc(start=0, length=NO_LIMIT, **condition1)
        _res = res1.exclude(**condition2)
    return ExcludeTable(_res, excluders=excluders, start=start, length=length)

def ExcludeTable(result, excluders=[], start=0, length=DEFAULT_MAX_QUERY):
    res = result
    if excluders:
        exclude_condition = generateConditions(excluders)
        if exclude_condition:
            res = result.exclude(**exclude_condition)

    if start == 0 and length == NO_LIMIT:
        return res
    elif length == NO_LIMIT:
        return res[start:]
    else:
        return res[start:(start+length)]

#def MandatoryCheck(fields, checkid=True, **info):
#    for i in fields:
#        if not checkid and i == 'id':
#            continue
#        if i =='state':
#            continue
#        if not i in info or not info[i]:
#            raise Exception(u"缺少必要参数：%s" % fields[i])
#    return True

def GetInstanceById(model_class, instance, returnDict=False):
    if isinstance(instance, model_class):
        instanceid = instance.id
    else:
        instanceid = instance
    query = {'id': instanceid}
    results = model_class.objects.filter(**query)
    if len(results) is not 1:
        return None
    elif not returnDict:
        return results[0]
    else:
        return results.values()[0]

