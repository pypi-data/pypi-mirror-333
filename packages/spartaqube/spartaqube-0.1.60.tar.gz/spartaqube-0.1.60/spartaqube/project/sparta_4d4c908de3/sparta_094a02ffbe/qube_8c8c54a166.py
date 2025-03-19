_C='isAuth'
_B='jsonData'
_A='res'
import json
from django.contrib.auth import logout
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from project.sparta_8f29384cd2.sparta_82d887a6fc import qube_83d9f0c2bd as qube_83d9f0c2bd
from project.sparta_22da4d4238.sparta_0d12b1779d.qube_bd77c02cd4 import sparta_5c73022983
from project.logger_config import logger
@csrf_exempt
def sparta_900159f8f3(request):A=json.loads(request.body);B=json.loads(A[_B]);return qube_83d9f0c2bd.sparta_900159f8f3(B)
@csrf_exempt
def sparta_7817933bd9(request):logout(request);A={_A:1};B=json.dumps(A);return HttpResponse(B)
@csrf_exempt
def sparta_b3465d051b(request):
	if request.user.is_authenticated:A=1
	else:A=0
	B={_A:1,_C:A};C=json.dumps(B);return HttpResponse(C)
def sparta_29644ce6ac(request):
	B=request;from django.contrib.auth import authenticate as F,login;from django.contrib.auth.models import User as C;G=json.loads(B.body);D=json.loads(G[_B]);H=D['email'];I=D['password'];E=0
	try:
		A=C.objects.get(email=H);A=F(B,username=A.username,password=I)
		if A is not None:login(B,A);E=1
	except C.DoesNotExist:pass
	J={_A:1,_C:E};K=json.dumps(J);return HttpResponse(K)