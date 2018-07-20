# -*- coding:utf-8 -*-

import logging
import random
import json
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from openstack_dashboard.utils import base_db_handle
from openstack_dashboard.utils import expert_db_handle
from openstack_dashboard.models import Expert
from openstack_dashboard.models import Project
from openstack_dashboard.models import Reviewer
from openstack_dashboard.models import BindRecord
from openstack_dashboard.models import REVIEWER_AVAILABLE
from openstack_dashboard.models import REVIEWER_SELECTED
from openstack_dashboard.models import REVIEWER_UNAVAILABLE
from openstack_dashboard.models import REVIEWER_INITIAL
from openstack_dashboard.models import REVIEW_STATE_NOTSTART
from openstack_dashboard.models import REVIEW_STATE_ONGOING
from openstack_dashboard.models import REVIEW_STATE_COMMITTED

LOG = logging.getLogger(__name__)

NO_LIMIT = -1
DEFAULT_MAX_QUERY = NO_LIMIT

STATEMAPPING = {
    'draft': u"草稿",                       # 草稿，该状态下项目详细信息可以修改
    'waitfor_approve': u"待批准",           # 等待批准，该状态下，可以退回重新填写项目信息，也可开始抽取专家
    'waitfor_setrule': u"待设置抽取条件",   # 1, 抽取专家前先设置抽取条件。
                                            # 如果项目要求A条件专家若干名，B条件专家若干名，则可以分多次抽取。
                                            # 每次抽取前先设置该次抽取的条件，然后再点击抽取
                                            # 2, 设置好抽取条件后，符合条件的专家会自动加入候选专家池。
    'waitfor_bind': u"待抽取",              # 1, 已经设置好了抽取条件，符合条件的专家会自动加入候选专家池。
                                            # 2, 点击抽取将会进行随机抽取
                                            # 3, 点击管理专家池，可以删除专家，设置隐藏专家等等
    'binded': u"已抽取",                    # 1, 随机抽取已完成
                                            # 2, 点击管理专家列表，可以删除无法参与的专家
                                            # 3, 可以进行小补抽（补抽），即从既有候选专家池内再次抽取专家
                                            # 4, 也可进行大补抽（再次抽取），即重新设置抽取条件、更新候选专家池
                                            # 5, 或者进行B条件的抽取（再次抽取）
                                            # 6, 若抽取完成，则点击启动项目，项目开启
    'kickoff': u"已立项",                   # 项目启动，尚未开始评审
    'start_review': u"评审中",              # 1, 开始评审，等待评审专家填写评审报告
                                            # 2, 可以查看专家已经提交的评审报告，也可退回评审报告供专家修改
                                            # 3, 若有专家尚未提交评审报告，可以点击强制提交
    'finished': u"完成评审",                # 完成评审，搜集评审报告，评价评审内容
    'deleted': u"已删除",                   # 已删除，不可恢复
}

OPERATORS_VALUE = base_db_handle.OPERATORS_VALUE
OPERATORS = base_db_handle.OPERATORS
MAINOPERATORS_VALUE = base_db_handle.MAINOPERATORS_VALUE
MAINOPERATORS = base_db_handle.MAINOPERATORS

SEARCHFIELDS_VALUE = {
    #'serial_no': u"项目编号",
    'projectname': u"项目名称",
    'leibie': u"项目类别",
    'shenbaoriqi': u"项目申报日期（如1999-01-31）",
    'fuzeren': u"项目负责人",
    'fuzeren_dianhua': u"项目负责人电话",
    'yewuchushi': u"业务处室",
    'yewuchushi_dianhua': u"业务处室电话",
    'pingshengshijian': u"项目评审或验收时间（如1999-01-31）",
    'pingshengdidian': u"项目评审或验收地点",
    #'yanshoushijian': u"项目验收时间",
    #'yanshoudidian': u"项目验收地点",
    #'state': u"状态",
}

SEARCHFIELDS = SEARCHFIELDS_VALUE.keys()

PROJECT_MANDATORY_FIELDS = {
    'projectname': u"项目名称",
    'state': u"状态",
}

SEARCHPARAM = {
    'field1_choices': SEARCHFIELDS,
    'oper1_choices': OPERATORS,
    'field2_choices': SEARCHFIELDS,
    'oper2_choices': OPERATORS,
    'mainop_choices': MAINOPERATORS,
}

def validate_projectid(func):
    def wrapper(project, *args, **kwargs):
        if not isinstance(project, Project):
            if isinstance(project, (int, str, unicode)):
                projectid = project
                project = GetProjectInstanceById(projectid, returnDict=False)
        if not project or not isinstance(project, Project):
            return None
        return func(project, *args, **kwargs)
    return wrapper

def validate_expertid(func):
    def wrapper(project, expert, *args, **kwargs):
        if not isinstance(expert, Expert):
            if isinstance(expert, (int, str, unicode)):
                expertid = expert
                expert = GetExpertInstanceById(expertid, returnDict=False)
        if not expert or not isinstance(expert, Expert):
            return None
        return func(project, expert, *args, **kwargs)
    return wrapper

def validate_bindrecid(func):
    def wrapper(bindrec, *args, **kwargs):
        if not isinstance(bindrec, BindRecord):
            if isinstance(bindrec, (int, str, unicode)):
                bindrecid = bindrec
                bindrec = GetBindRecordById(bindrecid)
        if not bindrec or not isinstance(bindrec, BindRecord):
            return None
        return func(bindrec, *args, **kwargs)
    return wrapper

def raise_403_for_invalide_project(func):
    def wrapper(project, *args, **kwargs):
        if not isinstance(project, Project):
            if isinstance(project, (int, str, unicode)):
                projectid = project
                project = GetProjectInstanceById(projectid, returnDict=False)
        if not project or not isinstance(project, Project):
            raise exceptions.NotAuthorized(
                _('No authority to visit project with id %s') % str(project))
        return func(project, *args, **kwargs)
    return wrapper

def GetProjects(start=0, length=DEFAULT_MAX_QUERY):
    if length == NO_LIMIT and start == 0:
        return Project.objects.all()
    elif length == NO_LIMIT:
        return Project.objects.all()[start:]
    else:
        return Project.objects.all()[start:(start+length)]

def FilterProjects(start=0, length=DEFAULT_MAX_QUERY, **args):
    if length == NO_LIMIT and start == 0:
        return Project.objects.filter(**args)
    elif length == NO_LIMIT:
        return Project.objects.filter(**args)[start:]
    else:
        return Project.objects.filter(**args)[start:(start+length)]

def get_initial_user_data(GetRequest, default=False):
    if default:
        default = {
            'field1': 'projectname',
            'oper1': 'exact',
            'field2': 'fuzeren',
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

def dict2filter(filters, d):
    for key in d:
        filter_adapt(filters, key, 'exact', d[key])

def filter_adapt(f, v, o, w):
    f.append({'var': v, 'operator': o, 'words': w})

def generate_filter(user_data):
    return base_db_handle.generate_filter(user_data, filter_adapt)

def generateCondition(filter_words):
    return base_db_handle.generateCondition(filter_words)

def generateConditions(filters_words):
    return base_db_handle.generateConditions(filter_words)

def QueryProjects(filters1, filters2=[], operator='', excluders=[], start=0, length=DEFAULT_MAX_QUERY):
    return base_db_handle.QueryTable(
               GetProjects,
               FilterProjects,
               filters1,
               filters2=filters2,
               operator=operator,
               excluders=excluders,
               start=start,
               length=length)

def UpdateProject(**info):
    projectid = info['id']
    project = GetProjectInstanceById(projectid)
    tobedel_fields = ['id',]
    for i in tobedel_fields:
        if i in info:
            del info[i]
    if not project:
        raise Exception(u"无法查询到项目[%s]" % projectid)
    if project.state != 'draft':
        raise Exception(u"项目状态异常，状态=%s" % project.state)
    info['updated_at'] = timezone.now()
    Project.objects.filter(id=projectid).update(**info)

def CreateProject(**info):
    for i in ['id', 'created_at']:
        if i in info:
            del info[i]
    info['state'] = 'draft'
    project = ProjectSaveDB(**info)
    return project

def ProjectSaveDB(**info):
    try:
        project = Project(**info)
        project.save()
        return project
    except Exception,e:
        raise Exception(u"数据库保存失败，错误消息：%s" % e.message)

def SubmitProjectInfo(project):
    return ChangeProjectState(project, ['draft'], 'waitfor_approve')

def WithdrawProjectReq(project):
    return ChangeProjectState(project, ['waitfor_approve',], 'draft')

def ApproveProjectReq(project):
    return ChangeProjectState(project, ['waitfor_approve'], 'waitfor_setrule')

def RejectProjectReq(project):
    return ChangeProjectState(project, ['waitfor_approve',], 'draft')

def AlreadySetRule(project):
    return ChangeProjectState(project, ['waitfor_setrule'], 'waitfor_bind')

def BindedExperts(project):
    return ChangeProjectState(project, ['waitfor_bind'], 'binded')

def AddtionalBindExperts(project):
    return ChangeProjectState(project, ['binded'], 'waitfor_bind')

def StartNewBind(project):
    return ChangeProjectState(project, ['waitfor_bind', 'binded'], 'waitfor_setrule')

def KickoffProject(project):
    return ChangeProjectState(project, ['binded'], 'kickoff')

def StartReviewProject(project):
    return ChangeProjectState(project, ['kickoff'], 'start_review')

def FinishReviewProject(project):
    return ChangeProjectState(project, ['start_review'], 'finished')

def DeleteProjectRecord(project):
    return ChangeProjectState(project, ['draft', 'waitfor_bind', 'binded', 'kickoff', ], 'deleted')

@validate_projectid
def SaveStartReviewDescription(project, description):
    project.startreviewdescription = description
    project.save()
    return project

def GetProjectInstanceById(projectid, returnDict=False):
    return base_db_handle.GetInstanceById(Project, projectid, returnDict=returnDict)

def RecordTime(project, to_state):
    now = timezone.now()
    if to_state == 'start_review':
        project.started_at = now
    elif to_state == 'finished':
        project.finished_at = now
    elif to_state == 'deleted':
        project.deleted_at = now

@validate_projectid
def ChangeProjectState(project, from_states, to_state):
    if type(from_states) is str:
        from_states = [from_states]
    if not project.state in from_states:
        return None
    project.state = to_state
    RecordTime(project, to_state)
    project.save()
    return project

@validate_projectid
def BindReviewerAndExpert(project, experts, project_expected_states, reviewer_expected_states):
    if project.state not in project_expected_states:
        return experts
    for expert in experts:
        reviewer = GetReviewerInstanceById(project, expert.id,
                                           project_expected_states=project_expected_states,
                                           reviewer_expected_states=reviewer_expected_states)
        expert.isPrioritized = reviewer.isPrioritized
        expert.isnotified = reviewer.isnotified
        expert.review_state = reviewer.review_state
    return experts

@validate_projectid
def GetCandidateOrReviewer(project):
    regex = '[%s%s]' % (REVIEWER_AVAILABLE, REVIEWER_SELECTED)
    experts = Expert.objects.filter(reviewer__project__exact=project, reviewer__state__regex=regex)
    return experts

@validate_projectid
def GetAvailableCandidate(project, need_reviewer_info=False):
    project_expected_states = ['waitfor_setrule', 'waitfor_bind', 'binded']
    reviewer_expected_state = REVIEWER_AVAILABLE
    experts = Expert.objects.filter(reviewer__project__exact=project,
                                    reviewer__state__exact=reviewer_expected_state)
    if not need_reviewer_info:
        return experts
    return BindReviewerAndExpert(project, experts, project_expected_states, [reviewer_expected_state])

@validate_projectid
def GetUnavailableReviewer(project):
    experts = Expert.objects.filter(reviewer__project__exact=project,
                                    reviewer__state__exact=REVIEWER_UNAVAILABLE)
    return experts

@validate_projectid
def GetBindedReviewers(project, need_reviewer_info=False):
    project_expected_states = ['waitfor_setrule', 'waitfor_bind', 'binded',
                               'kickoff', 'start_review', 'finished']
    reviewer_expected_state = REVIEWER_SELECTED
    experts = Expert.objects.filter(reviewer__project__exact=project,
                                    reviewer__state__exact=reviewer_expected_state)
    if not need_reviewer_info:
        return experts
    return BindReviewerAndExpert(project, experts, project_expected_states, [reviewer_expected_state])

@validate_projectid
def GetUnavailableCandidate(project):
    return Expert.objects.filter(reviewer__project__exact=project,
                                 reviewer__state__exact=REVIEWER_UNAVAILABLE)

@validate_projectid
def GetNonNotifiedReviewers(project):
    return Expert.objects.filter(reviewer__project__exact=project,
                                 reviewer__state__exact=REVIEWER_SELECTED,
                                 reviewer__isnotified__exact=False)

@validate_projectid
def GetAllExpertReviewer(project):
    return project.reviewers.all()

@validate_projectid
def NotifiedReviewers(project, experts):
    for expert in experts:
        if isinstance(expert, Expert):
            SetReviewerNotified(project, expert.id)
        else:
            SetReviewerNotified(project, expert)
    return project

@expert_db_handle.validate_expertid
def GetReviewerProjects(expert):
    projs = Project.objects.filter(reviewer__expert__exact=expert,
                                   reviewer__state__exact=REVIEWER_SELECTED,
                                   state__regex='(start_review|finished)')
    for proj in projs:
        reviewers = proj.reviewer_set.filter(expert=expert)
        if not len(reviewers) == 1:
            proj.review_state = 'ERROR'
        else:
            proj.review_state = reviewers[0].review_state
    return projs

@raise_403_for_invalide_project
def GetReviewerInstanceById(project, expertid, project_expected_states=['start_review'],
                                               reviewer_expected_states=[REVIEWER_SELECTED]):
    _input = {'projectid': str(project.id), 'expertid': expertid}
    if not project.state in project_expected_states:
        raise exceptions.NotAuthorized(
            _('No authority to visit project with id %(projectid)s') % _input)
    reviewer_state_regex = '[%s]' % (''.join(reviewer_expected_states))
    reviewers = project.reviewer_set.filter(
        expert__id=expertid, state__regex=reviewer_state_regex)
    if not len(reviewers) == 1:
        raise exceptions.NotAuthorized(
            _('Expert %(expertid)s has no authority to visit project with id %(projectid)s') % _input)
    return reviewers[0]

@validate_projectid
def SetReviewerNotified(project, expertid):
    reviewer = GetReviewerInstanceById(project, expertid,
                                       project_expected_states=['waitfor_setrule', 'waitfor_bind', 'binded'],
                                       reviewer_expected_states=[REVIEWER_SELECTED])
    reviewer.isnotified = True
    reviewer.save()
    return reviewer

@validate_projectid
def CleanCandidates(project):
    for expert in GetAvailableCandidate(project):
        UpdateReviewerState(project, expert, REVIEWER_AVAILABLE, REVIEWER_INITIAL)
    return ProjectFinishCurrentBind(project)

@validate_projectid
def ProjectFinishCurrentBind(project):
    if project.current_bindrec:
        FinishCurrentBind(project.current_bindrec)
        project.current_bindrec = None
        project.save()
    return project

@validate_projectid
def AddCandidates(project, experts):
    all_candidates = GetAvailableCandidate(project)
    all_binded_reviewers = GetBindedReviewers(project)
    all_unavailable_experts = GetUnavailableCandidate(project)
    has_in_pool = []
    has_in_project = []
    has_unavailable = []
    for expert in experts:
        if expert in all_binded_reviewers:
            has_in_project.append(expert)
        elif expert in all_candidates:
            has_in_pool.append(expert)
        elif expert in all_unavailable_experts:
            has_unavailable.append(expert)
        else:
            CreateReviewer(project, expert)
    return (project, has_in_pool, has_in_project, has_unavailable)

@validate_projectid
def AddExpertsIntoProject(project, experts):
    all_candidates = GetAvailableCandidate(project)
    all_binded_reviewers = GetBindedReviewers(project)

    not_in_pool = []
    has_in_project = []
    for expert in experts:
        if expert in all_binded_reviewers:
            has_in_project.append(expert)
        elif not expert in all_candidates:
            not_in_pool.append(expert)
        else:
            UpdateReviewerState(project, expert, REVIEWER_AVAILABLE, REVIEWER_SELECTED)
    return (project, not_in_pool, has_in_project)

@validate_projectid
@validate_expertid
def RemoveExpertFromProject(project, expert):
    UpdateReviewerState(project, expert, REVIEWER_SELECTED, REVIEWER_UNAVAILABLE)
    return project

@validate_projectid
@validate_expertid
def RemoveCandidate(project, expert):
    UpdateReviewerState(project, expert, REVIEWER_AVAILABLE, REVIEWER_UNAVAILABLE)
    return project

@validate_projectid
@validate_expertid
def RevertUnavailableReviewer(project, expert):
    UpdateReviewerState(project, expert, REVIEWER_UNAVAILABLE, REVIEWER_INITIAL)
    return project

@validate_projectid
@validate_expertid
def CreateReviewer(project, expert):
    (r, res) = Reviewer.objects.get_or_create(project=project, expert=expert)
    r.state = REVIEWER_AVAILABLE
    r.save()
    return r

@validate_projectid
def CreateBindRecord(project, data, bind_number):
    if project.state != 'waitfor_setrule':
        return None
    conditions = {}
    for i in ['field1', 'oper1', 'value1', 'field2', 'oper2', 'value2', 'mainop']:
        if i in data:
            conditions[i] = data[i]
    b = BindRecord.objects.create(project=project, conditions=json.dumps(conditions),
                                  bind_number=bind_number)
    b.save()
    project.current_bindrec = b.id
    project.save()
    return b

@validate_bindrecid
def UpdateReviewerNum(bindrec, num, comments):
    old_num = bindrec.reviewer_number
    bindrec.reviewer_number = num
    now = timezone.now()
    if not old_num:
        bindrec.binded_at = now
    else:
        bindrec.rebinded_at = now
    comments = comments if comments else u"无"
    if bindrec.bind_comments:
        new_comments = json.loads(bindrec.bind_comments)
    else:
        new_comments = {}
    new_comments[now.strftime('%s')] = u"时间：%s\n抽取人数：%d\n说明：%s" % (
        now.strftime('%Y-%m-%d'), num, comments)
    bindrec.bind_comments = json.dumps(new_comments)
    bindrec.save()
    return bindrec

@validate_bindrecid
def UpdateCandidateNum(bindrec, num):
    bindrec.candidate_number = num
    bindrec.save()
    return bindrec

@validate_bindrecid
def FinishCurrentBind(bindrec):
    now = timezone.now()
    bindrec.finished_at = now
    bindrec.save()
    return bindrec

def GetBindRecordById(bindrec):
    return base_db_handle.GetInstanceById(BindRecord, bindrec, returnDict=False)

@validate_projectid
def PrioritizeExpertInProject(project, expertid):
    return UpdateReviewerPrioritize(project, expertid, True)

@validate_projectid
def DeprioritizeExpertInProject(project, expertid):
    return UpdateReviewerPrioritize(project, expertid, False)

@validate_projectid
def UpdateReviewerPrioritize(project, expertid, isPrioritized):
    reviewer = GetReviewerInstanceById(project, expertid,
                                       project_expected_states=['waitfor_bind', 'binded'],
                                       reviewer_expected_states=[REVIEWER_AVAILABLE])
    reviewer.isPrioritized = isPrioritized
    reviewer.save()
    return reviewer

@validate_projectid
@validate_expertid
def UpdateReviewerState(project, expert, from_state, to_state):
    reviewer = GetReviewerInstanceById(project, expert.id,
                                       project_expected_states=['waitfor_setrule', 'waitfor_bind', 'binded'],
                                       reviewer_expected_states=[from_state])
    now = timezone.now()
    reviewer.state = to_state
    if to_state == REVIEWER_SELECTED:
        reviewer.selected_at = now
    elif to_state == REVIEWER_UNAVAILABLE:
        reviewer.deleted_at = now
    reviewer.save()
    return reviewer

@validate_projectid
def UpdateReviewComments(project, expertid, comments, comments_attachments):
    reviewer = GetReviewerInstanceById(project, expertid,
                                       project_expected_states=['start_review'],
                                       reviewer_expected_states=[REVIEWER_SELECTED])
    reviewer.review_state = REVIEW_STATE_ONGOING
    reviewer.comments = comments
    isDelete = bool(not comments_attachments and reviewer.comments_attachments)
    isCreate = bool(comments_attachments and not reviewer.comments_attachments)
    isUpdate = bool(comments_attachments and reviewer.comments_attachments \
        and (comments_attachments != reviewer.comments_attachments))
    if isDelete or isUpdate:
        reviewer.comments_attachments = ''
    reviewer.save()
    if isCreate or isUpdate:
        reviewer.comments_attachments = comments_attachments
        reviewer.save()
    return reviewer

@validate_projectid
def UpdateReviewState(project, expertid, from_states, to_state):
    reviewer = GetReviewerInstanceById(project, expertid,
                                       project_expected_states=['start_review'],
                                       reviewer_expected_states=[REVIEWER_SELECTED])
    if reviewer.review_state in from_states:
        reviewer.review_state = to_state
        reviewer.save()
    else:
        _input = {'projectid': str(project), 'expertid': expertid}
        raise exceptions.BadRequest(
            _('Expert %(expertid)s comments for project with id %(projectid)s can not be changed') % _input)

@validate_projectid
def GetReviewerReviewState(project, expertid):
    reviewer = GetReviewerInstanceById(project, expertid,
                                       project_expected_states=['start_review', 'finished'],
                                       reviewer_expected_states=[REVIEWER_SELECTED])
    return reviewer.review_state

@validate_projectid
def CommitReviewResult(project, expertid):
    UpdateReviewState(project, expertid, [REVIEW_STATE_ONGOING], REVIEW_STATE_COMMITTED)

@validate_projectid
def ForceCommitReviewResult(project, expertid):
    UpdateReviewState(project, expertid, [REVIEW_STATE_NOTSTART, REVIEW_STATE_ONGOING], REVIEW_STATE_COMMITTED)

@validate_projectid
def ReturnReviewResult(project, expertid):
    UpdateReviewState(project, expertid, [REVIEW_STATE_COMMITTED], REVIEW_STATE_ONGOING)

@validate_projectid
def CommentExpertReview(project, expertid, comments):
    reviewer = GetReviewerInstanceById(project, expertid,
                                       project_expected_states=['finished'],
                                       reviewer_expected_states=[REVIEWER_SELECTED])
    _comments = ""
    if reviewer.comments_on_comments:
        _comments = u"%s\n\n=======================\n" % reviewer.comments_on_comments
    reviewer.comments_on_comments = u"%s%s" % (_comments, comments)
    reviewer.save()
    return project

@validate_projectid
def AllReviewSubmitted(project):
    _input = {'projectid': str(project.id)}
    if not project.state in ['start_review']:
        raise exceptions.NotAuthorized(
            _('No authority to visit project with id %(projectid)s') % _input)
    reviewers = project.reviewer_set.filter(state__exact=REVIEWER_SELECTED)
    for r in reviewers:
        if not r.review_state == REVIEW_STATE_COMMITTED:
            return False
    return True

@validate_projectid
def RandomBindExpert(project, count):
    _all_candidates = GetAvailableCandidate(project, need_reviewer_info=True)
    all_prioritized_candidates = [ e for e in _all_candidates if e.isPrioritized ]
    all_non_prioritized_candidates = [ e for e in _all_candidates if not e.isPrioritized ]
    selected_experts = []
    t1 = len(all_prioritized_candidates)
    t2 = len(all_non_prioritized_candidates)
    ta = t1 + t2
    count = ta if count > ta else count
    if count == 0:
        return []
    c1 = count if t1 > count else t1
    c2 = count - c1;

    if c1 == t1:
        selected_experts = all_prioritized_candidates
        all_prioritized_candidates = []
    else:
        for r in range(t1, (t1 - c1), -1):
            selected_id = random.randint(0, r - 1)
            selected_experts.append(all_prioritized_candidates.pop(selected_id))
    if c2 > 0:
        for r in range(t2, (t2 - c2), -1):
            selected_id = random.randint(0, r - 1)
            selected_experts.append(all_non_prioritized_candidates.pop(selected_id))

    (project, not_in_pool, has_in_project) = AddExpertsIntoProject(project, selected_experts)
    for e in has_in_project:
        selected_experts.pop(e)
    return selected_experts

def test_import_data():
    for i in range(1, 20):
        p = {'projectname': "project%02d" % i,
             'fuzeren': "负责人%02d" % i,
             'shenbaodanwei': "单位%d" % (i%5),
             'shenbaoriqi': "20%02d-%02d-%02d" % (i%15, i%12+1, i%28+1),
             'pingshengshijian': "20%02d-%02d-%02d" % (i%15+1, i%11+2, i%18+11),
             'leibie': "项目类别%02d" % i,
             'yewuchushi': "业务处室%02d" % i,
             'chouqurenshu': "%02d" % i,
            }
        CreateProject(**p)

def test0():
    Expert.objects.all().delete()
    Project.objects.all().delete()

def test1():
    for i in range(1,3):
        p = {'projectname': "project%d" % i,}
        CreateProject(**p)

def test2(pid, es):
    AddCandidates(pid, es)

def test3(pid, es):
    nes = []
    for i in range(0, len(es)):
        if i % 2 == 0:
            nes.append(es[i])
    AddExpertsIntoProject(pid, nes)

def test4(projectid, expertid):
    return RemoveExpertsFromProject(projectid, expertid)

