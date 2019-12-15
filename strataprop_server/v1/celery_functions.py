#!/usr/bin/env python
# -*- coding: utf-8 -*-

from strataprop_server import celery,app, db
import re
import sys
reload(sys)
sys.setdefaultencoding('utf8')

@celery.task
def task_download_report(emails_list=None, filters=None, member=None):
    print("")
    # from strataprop_server.v1.task_management.web_download_task_functions import download_task_via_email
    # from strataprop_server.v1.models.member_basic_info import MemberBasicInfo
    # member = MemberBasicInfo.get_member_details(member)
    # download_task_via_email(emails_list, filters, member)
