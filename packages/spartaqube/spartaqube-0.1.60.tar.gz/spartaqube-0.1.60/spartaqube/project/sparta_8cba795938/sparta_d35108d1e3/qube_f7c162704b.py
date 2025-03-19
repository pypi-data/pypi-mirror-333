_K='bPublicUser'
_J='notebook_name'
_I='notebook_id'
_H='b_require_password'
_G='notebook_obj'
_F='default_project_path'
_E='bCodeMirror'
_D='menuBar'
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
import project.sparta_22da4d4238.sparta_0d12b1779d.qube_bd77c02cd4 as qube_bd77c02cd4
from project.sparta_8f29384cd2.sparta_82d887a6fc.qube_83d9f0c2bd import sparta_b8b3df6a31
from project.sparta_8f29384cd2.sparta_027dc65844 import qube_fdbbe48852 as qube_fdbbe48852
from project.sparta_8f29384cd2.sparta_ccd7e0da68.qube_56413a793d import sparta_21526a056d
@csrf_exempt
@sparta_b8b3df6a31
@login_required(redirect_field_name='login')
def sparta_567c20f1b6(request):
	B=request;A=qube_bd77c02cd4.sparta_c1601de691(B);A[_D]=13;D=qube_bd77c02cd4.sparta_d6e03fbf4d(B.user);A.update(D);A[_E]=_A
	def E(path):
		A=Path(path)
		if not A.exists():A.mkdir(parents=_A)
	F=sparta_21526a056d();C=os.path.join(F,'notebook');E(C);A[_F]=C;return render(B,'dist/project/notebook/notebook.html',A)
@csrf_exempt
def sparta_5895e8ce53(request,id):
	B=request
	if id is _B:C=B.GET.get('id')
	else:C=id
	D=False
	if C is _B:D=_A
	else:
		E=qube_fdbbe48852.sparta_04024a5454(C,B.user);G=E[_C]
		if G==-1:D=_A
	if D:return sparta_567c20f1b6(B)
	A=qube_bd77c02cd4.sparta_c1601de691(B);A[_D]=12;H=qube_bd77c02cd4.sparta_d6e03fbf4d(B.user);A.update(H);A[_E]=_A;F=E[_G];A[_F]=F.project_path;A[_H]=0 if E[_C]==1 else 1;A[_I]=F.notebook_id;A[_J]=F.name;A[_K]=B.user.is_anonymous;return render(B,'dist/project/notebook/notebookRun.html',A)
@csrf_exempt
@sparta_b8b3df6a31
@login_required(redirect_field_name='login')
def sparta_e1db746f48(request,id):
	B=request
	if id is _B:C=B.GET.get('id')
	else:C=id
	D=False
	if C is _B:D=_A
	else:
		E=qube_fdbbe48852.sparta_04024a5454(C,B.user);G=E[_C]
		if G==-1:D=_A
	if D:return sparta_567c20f1b6(B)
	A=qube_bd77c02cd4.sparta_c1601de691(B);A[_D]=12;H=qube_bd77c02cd4.sparta_d6e03fbf4d(B.user);A.update(H);A[_E]=_A;F=E[_G];A[_F]=F.project_path;A[_H]=0 if E[_C]==1 else 1;A[_I]=F.notebook_id;A[_J]=F.name;A[_K]=B.user.is_anonymous;return render(B,'dist/project/notebook/notebookDetached.html',A)