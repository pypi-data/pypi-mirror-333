_A='jsonData'
import json,inspect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.forms.models import model_to_dict
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings as conf_settings
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.hashers import make_password
from project.sparta_8f29384cd2.sparta_b6047b9129 import qube_6855a41cc7 as qube_6855a41cc7
from project.sparta_8f29384cd2.sparta_82d887a6fc.qube_83d9f0c2bd import sparta_eacf86fcd7
@csrf_exempt
@sparta_eacf86fcd7
def sparta_5d98c626f3(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_6855a41cc7.sparta_5d98c626f3(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_eacf86fcd7
def sparta_bd59b16ca3(request):
	C='userObj';B=request;D=json.loads(B.body);E=json.loads(D[_A]);F=B.user;A=qube_6855a41cc7.sparta_bd59b16ca3(E,F)
	if A['res']==1:
		if C in list(A.keys()):login(B,A[C]);A.pop(C,None)
	G=json.dumps(A);return HttpResponse(G)
@csrf_exempt
@sparta_eacf86fcd7
def sparta_ea106a177b(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=A.user;E=qube_6855a41cc7.sparta_ea106a177b(C,D);F=json.dumps(E);return HttpResponse(F)
@csrf_exempt
@sparta_eacf86fcd7
def sparta_73c1e09da1(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_6855a41cc7.sparta_73c1e09da1(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_eacf86fcd7
def sparta_a1e39c97e0(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_6855a41cc7.sparta_a1e39c97e0(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_eacf86fcd7
def sparta_1887b42125(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_6855a41cc7.sparta_1887b42125(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
def sparta_c3cfe371ec(request):A=json.loads(request.body);B=json.loads(A[_A]);C=qube_6855a41cc7.token_reset_password_worker(B);D=json.dumps(C);return HttpResponse(D)
@csrf_exempt
@sparta_eacf86fcd7
def sparta_68bf0440d1(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_6855a41cc7.network_master_reset_password(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
def sparta_6dae6f66ab(request):A=json.loads(request.body);B=json.loads(A[_A]);C=qube_6855a41cc7.sparta_6dae6f66ab(B);D=json.dumps(C);return HttpResponse(D)
@csrf_exempt
def sparta_d17acf8b70(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_6855a41cc7.sparta_d17acf8b70(A,C);E=json.dumps(D);return HttpResponse(E)