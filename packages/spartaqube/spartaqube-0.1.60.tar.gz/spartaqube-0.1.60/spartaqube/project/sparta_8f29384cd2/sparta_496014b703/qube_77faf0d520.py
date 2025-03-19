_F='is_owner'
_E=True
_D='has_reshare_rights'
_C='has_write_rights'
_B='is_admin'
_A=False
import json,base64,hashlib,re,uuid,pandas as pd
from datetime import datetime,timedelta
from dateutil import parser
import pytz
UTC=pytz.utc
from django.db.models import Q
from django.conf import settings as conf_settings
from django.contrib.auth.models import User
from django.contrib.humanize.templatetags.humanize import naturalday
from django.forms.models import model_to_dict
from project.models import User,UserProfile
from project.sparta_8f29384cd2.sparta_63edf7d78c import qube_5af9e48ff5 as qube_5af9e48ff5
def sparta_e381aa94a0(is_owner=_A):return{_F:is_owner,_B:_E,_C:_E,_D:_E}
def sparta_935d2bdba1():return{_F:_A,_B:_A,_C:_A,_D:_A}
def sparta_012d31b0e0(user_obj,portfolio_obj):
	B=portfolio_obj;A=user_obj
	if B.user==A:return sparta_e381aa94a0(_E)
	F=qube_5af9e48ff5.sparta_9c3e29af31(A);E=[A.userGroup for A in F]
	if len(E)>0:D=PortfolioShared.objects.filter(Q(is_delete=0,userGroup__in=E,portfolio=B)&~Q(portfolio__user=A)|Q(is_delete=0,user=A,portfolio=B))
	else:D=PortfolioShared.objects.filter(is_delete=0,user=A,portfolio=B)
	if D.count()==0:return sparta_935d2bdba1()
	G=D[0];C=G.ShareRights
	if C.is_delete:return sparta_935d2bdba1()
	return{_F:_A,_B:C.is_admin,_C:C.has_write_rights,_D:C.has_reshare_rights}
def sparta_6037282186(user_obj,universe_obj):
	B=universe_obj;A=user_obj
	if B.user==A:return sparta_e381aa94a0()
	F=qube_5af9e48ff5.sparta_9c3e29af31(A);E=[A.userGroup for A in F]
	if len(E)>0:D=UniverseShared.objects.filter(Q(is_delete=0,userGroup__in=E,universe=B)&~Q(universe__user=A)|Q(is_delete=0,user=A,universe=B))
	else:D=UniverseShared.objects.filter(is_delete=0,user=A,universe=B)
	if D.count()==0:return sparta_935d2bdba1()
	G=D[0];C=G.ShareRights
	if C.is_delete:return sparta_935d2bdba1()
	return{_B:C.is_admin,_C:C.has_write_rights,_D:C.has_reshare_rights}