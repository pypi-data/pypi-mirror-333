_L='bPublicUser'
_K='developer_name'
_J='developer_id'
_I='b_require_password'
_H='developer_obj'
_G='default_project_path'
_F='bCodeMirror'
_E='menuBar'
_D='dist/project/homepage/homepage.html'
_C='res'
_B=None
_A=True
import os,json,getpass,platform
from pathlib import Path
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.static import serve
from django.http import FileResponse,Http404
from urllib.parse import unquote
from django.conf import settings as conf_settings
import project.sparta_22da4d4238.sparta_0d12b1779d.qube_bd77c02cd4 as qube_bd77c02cd4
from project.sparta_8f29384cd2.sparta_82d887a6fc.qube_83d9f0c2bd import sparta_b8b3df6a31
from project.sparta_8f29384cd2.sparta_dca4038ce5 import qube_bf69fee706 as qube_bf69fee706
from project.sparta_8f29384cd2.sparta_ccd7e0da68.qube_56413a793d import sparta_21526a056d
@csrf_exempt
@sparta_b8b3df6a31
@login_required(redirect_field_name='login')
def sparta_5498569831(request):
	B=request
	if not conf_settings.IS_DEV_VIEW_ENABLED:A=qube_bd77c02cd4.sparta_c1601de691(B);return render(B,_D,A)
	qube_bf69fee706.sparta_3496a3178e();A=qube_bd77c02cd4.sparta_c1601de691(B);A[_E]=12;D=qube_bd77c02cd4.sparta_d6e03fbf4d(B.user);A.update(D);A[_F]=_A
	def E(path):
		A=Path(path)
		if not A.exists():A.mkdir(parents=_A)
	F=sparta_21526a056d();C=os.path.join(F,'developer');E(C);A[_G]=C;return render(B,'dist/project/developer/developer.html',A)
@csrf_exempt
def sparta_d75f21fe43(request,id):
	B=request
	if not conf_settings.IS_DEV_VIEW_ENABLED:A=qube_bd77c02cd4.sparta_c1601de691(B);return render(B,_D,A)
	if id is _B:C=B.GET.get('id')
	else:C=id
	D=False
	if C is _B:D=_A
	else:
		E=qube_bf69fee706.has_developer_access(C,B.user);G=E[_C]
		if G==-1:D=_A
	if D:return sparta_5498569831(B)
	A=qube_bd77c02cd4.sparta_c1601de691(B);A[_E]=12;H=qube_bd77c02cd4.sparta_d6e03fbf4d(B.user);A.update(H);A[_F]=_A;F=E[_H];A[_G]=F.project_path;A[_I]=0 if E[_C]==1 else 1;A[_J]=F.developer_id;A[_K]=F.name;A[_L]=B.user.is_anonymous;return render(B,'dist/project/developer/developerRun.html',A)
@csrf_exempt
@sparta_b8b3df6a31
@login_required(redirect_field_name='login')
def sparta_d47c4fd288(request,id):
	B=request
	if not conf_settings.IS_DEV_VIEW_ENABLED:A=qube_bd77c02cd4.sparta_c1601de691(B);return render(B,_D,A)
	if id is _B:C=B.GET.get('id')
	else:C=id
	D=False
	if C is _B:D=_A
	else:
		E=qube_bf69fee706.has_developer_access(C,B.user);G=E[_C]
		if G==-1:D=_A
	if D:return sparta_5498569831(B)
	A=qube_bd77c02cd4.sparta_c1601de691(B);A[_E]=12;H=qube_bd77c02cd4.sparta_d6e03fbf4d(B.user);A.update(H);A[_F]=_A;F=E[_H];A[_G]=F.project_path;A[_I]=0 if E[_C]==1 else 1;A[_J]=F.developer_id;A[_K]=F.name;A[_L]=B.user.is_anonymous;return render(B,'dist/project/developer/developerDetached.html',A)
def sparta_38f326ccf8(request,project_path,file_name):A=project_path;A=unquote(A);return serve(request,file_name,document_root=A)