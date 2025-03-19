import os,json,getpass,platform
from pathlib import Path
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings as conf_settings
import project.sparta_22da4d4238.sparta_0d12b1779d.qube_bd77c02cd4 as qube_bd77c02cd4
from project.sparta_8f29384cd2.sparta_82d887a6fc.qube_83d9f0c2bd import sparta_b8b3df6a31
from project.sparta_8f29384cd2.sparta_a6d0a04f89 import qube_0fa16a97bc as qube_0fa16a97bc
from project.sparta_8f29384cd2.sparta_65ecb68b5b import qube_8c7b66e0b7 as qube_8c7b66e0b7
def sparta_4b0fbcb7ae():
	A=platform.system()
	if A=='Windows':return'windows'
	elif A=='Linux':return'linux'
	elif A=='Darwin':return'mac'
	else:return
@csrf_exempt
@sparta_b8b3df6a31
@login_required(redirect_field_name='login')
def sparta_103b941749(request):
	E='template';D='developer';B=request
	if not conf_settings.IS_DEV_VIEW_ENABLED:A=qube_bd77c02cd4.sparta_c1601de691(B);return render(B,'dist/project/homepage/homepage.html',A)
	A=qube_bd77c02cd4.sparta_c1601de691(B);A['menuBar']=12;F=qube_bd77c02cd4.sparta_d6e03fbf4d(B.user);A.update(F);A['bCodeMirror']=True;G=os.path.dirname(__file__);C=os.path.dirname(os.path.dirname(G));H=os.path.join(C,'static');I=os.path.join(H,'js',D,E,'frontend');A['frontend_path']=I;J=os.path.dirname(C);K=os.path.join(J,'django_app_template',D,E,'backend');A['backend_path']=K;return render(B,'dist/project/developer/developerExamples.html',A)