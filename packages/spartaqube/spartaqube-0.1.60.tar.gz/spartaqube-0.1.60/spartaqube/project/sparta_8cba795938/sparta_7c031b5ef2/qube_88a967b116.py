_C='bCodeMirror'
_B='menuBar'
_A=True
import os,json,getpass,platform
from pathlib import Path
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import project.sparta_22da4d4238.sparta_0d12b1779d.qube_bd77c02cd4 as qube_bd77c02cd4
from project.sparta_8f29384cd2.sparta_82d887a6fc.qube_83d9f0c2bd import sparta_b8b3df6a31
from project.sparta_8f29384cd2.sparta_a6d0a04f89 import qube_0fa16a97bc as qube_0fa16a97bc
from project.sparta_8f29384cd2.sparta_65ecb68b5b import qube_8c7b66e0b7 as qube_8c7b66e0b7
from project.sparta_8f29384cd2.sparta_ccd7e0da68.qube_56413a793d import sparta_21526a056d
@csrf_exempt
@sparta_b8b3df6a31
@login_required(redirect_field_name='login')
def sparta_938e1f1cf3(request):
	B=request;C=B.GET.get('edit')
	if C is None:C='-1'
	A=qube_bd77c02cd4.sparta_c1601de691(B);A[_B]=9;E=qube_bd77c02cd4.sparta_d6e03fbf4d(B.user);A.update(E);A[_C]=_A;A['edit_chart_id']=C
	def F(path):
		A=Path(path)
		if not A.exists():A.mkdir(parents=_A)
	G=sparta_21526a056d();D=os.path.join(G,'dashboard');F(D);A['default_project_path']=D;return render(B,'dist/project/dashboard/dashboard.html',A)
@csrf_exempt
def sparta_d20c514a26(request,id):
	A=request
	if id is None:B=A.GET.get('id')
	else:B=id
	return sparta_c5a2e7752f(A,B)
def sparta_c5a2e7752f(request,dashboard_id,session='-1'):
	G='res';E=dashboard_id;B=request;C=False
	if E is None:C=_A
	else:
		D=qube_8c7b66e0b7.has_dashboard_access(E,B.user);H=D[G]
		if H==-1:C=_A
	if C:return sparta_938e1f1cf3(B)
	A=qube_bd77c02cd4.sparta_c1601de691(B);A[_B]=9;I=qube_bd77c02cd4.sparta_d6e03fbf4d(B.user);A.update(I);A[_C]=_A;F=D['dashboard_obj'];A['b_require_password']=0 if D[G]==1 else 1;A['dashboard_id']=F.dashboard_id;A['dashboard_name']=F.name;A['bPublicUser']=B.user.is_anonymous;A['session']=str(session);return render(B,'dist/project/dashboard/dashboardRun.html',A)