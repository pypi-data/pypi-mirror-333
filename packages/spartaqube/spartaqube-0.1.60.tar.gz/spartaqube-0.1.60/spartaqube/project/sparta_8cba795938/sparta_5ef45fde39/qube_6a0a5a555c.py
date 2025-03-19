_A='menuBar'
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
from project.sparta_8f29384cd2.sparta_2283960592 import qube_47219f2032 as qube_47219f2032
from project.sparta_8f29384cd2.sparta_fb9ec05166 import qube_4dbbaf8fe9 as qube_4dbbaf8fe9
from project.sparta_8f29384cd2.sparta_ccd7e0da68.qube_56413a793d import sparta_21526a056d
@csrf_exempt
@sparta_b8b3df6a31
@login_required(redirect_field_name='login')
def sparta_7b3bc8d434(request):A=request;B=qube_bd77c02cd4.sparta_c1601de691(A);B[_A]=-1;C=qube_bd77c02cd4.sparta_d6e03fbf4d(A.user);B.update(C);return render(A,'dist/project/homepage/homepage.html',B)
@csrf_exempt
@sparta_b8b3df6a31
@login_required(redirect_field_name='login')
def sparta_4df72f0cb1(request,kernel_manager_uuid):
	D=kernel_manager_uuid;C=True;B=request;E=False
	if D is None:E=C
	else:
		F=qube_47219f2032.sparta_8a41a7d617(B.user,D)
		if F is None:E=C
	if E:return sparta_7b3bc8d434(B)
	def H(path):
		A=Path(path)
		if not A.exists():A.mkdir(parents=C)
	K=sparta_21526a056d();G=os.path.join(K,'kernel');H(G);I=os.path.join(G,D);H(I);J=os.path.join(I,'main.ipynb')
	if not os.path.exists(J):
		L=qube_4dbbaf8fe9.sparta_3a338a2623()
		with open(J,'w')as M:M.write(json.dumps(L))
	A=qube_bd77c02cd4.sparta_c1601de691(B);A['default_project_path']=G;A[_A]=-1;N=qube_bd77c02cd4.sparta_d6e03fbf4d(B.user);A.update(N);A['kernel_name']=F.name;A['kernelManagerUUID']=F.kernel_manager_uuid;A['bCodeMirror']=C;A['bPublicUser']=B.user.is_anonymous;return render(B,'dist/project/sqKernelNotebook/sqKernelNotebook.html',A)