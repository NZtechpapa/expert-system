# -*- coding:utf-8 -*-

import os
from django.conf import settings
from keystoneauth1.identity import v3
from keystoneauth1 import session
from keystoneclient.v3 import client as keystone_client_v3
from openstack_dashboard import api

DEFAULT_DOMAIN = 'Default'

# Following is the anonymous user creation functions
def get_keystone_credentials_v3():
    d = {}
    d['user_domain_name'] = DEFAULT_DOMAIN
    d['project_domain_name'] = DEFAULT_DOMAIN
    d['username'] = settings.EXPERTCONSTANT['expert_admin_name']
    d['password'] = settings.EXPERTCONSTANT['expert_admin_pwd']
    d['auth_url'] = settings.OPENSTACK_KEYSTONE_URL
    d['project_name'] = settings.EXPERTCONSTANT['expert_project_name']
    return d

def get_keystone_client():
    credentials = get_keystone_credentials_v3()
    auth = v3.Password(**credentials)
    sess = session.Session(auth=auth)
    return keystone_client_v3.Client(session=sess)

def user_create(expertid, name, password, email, description=None, client=None):
    if not client:
        client = get_keystone_client()
    project = settings.EXPERTCONSTANT['expert_project_name']
    default_project = settings.EXPERTCONSTANT['expert_project_name']
    initial_role = settings.EXPERTCONSTANT['expert_uncertified_role']
    if not description:
        description = "Register from anonymous user"
    data = {'expertid': expertid}
    role_filters = {"name": initial_role}
    project_filters = {"name": project}
    roles = client.roles.list(**role_filters)
    if len(roles) != 1:
        raise Exception("Missing role %s" % initial_role)
    projects = client.projects.list(**project_filters)
    if len(projects) != 1:
        raise Exception("Missing project %s" % project)
    user = client.users.create(name, project=project, password=password,
                               email=email, description=description,
                               default_project=default_project, **data)
    client.roles.grant(roles[0], user=user, project=projects[0])
    return user

def user_delete(uid, client=None):
    if not client:
        client = get_keystone_client()
    return client.users.delete(uid)

# Following is using horizon api
def _get_role_id_by_name(request, name):
    filters = {"name": name}
    roles = api.keystone.role_list(request, filters=filters, admin=True)
    return roles[0].id if len(roles) == 1 else None

def _get_project_id_by_name(request, name):
    if request.user.project_name == name:
        return request.user.project_id
    filters = {"name": name}
    (projects, _more) = api.keystone.tenant_list(request, filters=filters, admin=True)
    return projects[0].id if len(projects) == 1 else None

def api_grant_role(request, uid, rolename=None, roleid=None, projectid=None):
    if not roleid and not rolename:
        raise Exception("Internal error, either rolename or roleid must be given")
    if not roleid:
        roleid = _get_role_id_by_name(request, rolename)
        if not roleid:
            raise Exception("Missing role %s" % rolename)
    if not projectid:
        project = settings.EXPERTCONSTANT['expert_project_name']
        projectid = _get_project_id_by_name(request, project)
        if not projectid:
            raise Exception("Missing project %s" % project)
    api.keystone.add_tenant_user_role(request,
                                      projectid,
                                      uid,
                                      roleid)

def api_user_create(request, expertid, name, password, email, description=None):
    domain = api.keystone.get_default_domain(request, False)
    projectid = _get_project_id_by_name(request, settings.EXPERTCONSTANT['expert_project_name'])
    roleid = _get_role_id_by_name(request, settings.EXPERTCONSTANT['expert_uncertified_role'])
    if not projectid or not roleid:
        return None
    kwargs = {'expertid': expertid}
    if not description:
        description = "Account for expert %s(%d)" % (name, expertid)
    new_expert = api.keystone.user_create(request,
                                          name=name,
                                          email=email,
                                          description=description,
                                          password=password,
                                          project=projectid,
                                          enabled=True,
                                          domain=domain.id,
                                          **kwargs)
    api_grant_role(request, new_expert.id, projectid=projectid, roleid=roleid)
    return new_expert

def api_user_delete(request, uid):
    return api.keystone.user_delete(request, uid)
