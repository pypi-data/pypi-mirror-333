_I='error.txt'
_H='zipName'
_G='utf-8'
_F='attachment; filename={0}'
_E='appId'
_D='res'
_C='Content-Disposition'
_B='projectPath'
_A='jsonData'
import json,base64
from django.http import HttpResponse,Http404
from django.views.decorators.csrf import csrf_exempt
from project.sparta_8f29384cd2.sparta_a6953654d4 import qube_f29636d3f5 as qube_f29636d3f5
from project.sparta_8f29384cd2.sparta_a6953654d4 import qube_c1b8cdd656 as qube_c1b8cdd656
from project.sparta_8f29384cd2.sparta_ccd7e0da68 import qube_67447782f4 as qube_67447782f4
from project.sparta_8f29384cd2.sparta_82d887a6fc.qube_83d9f0c2bd import sparta_eacf86fcd7
@csrf_exempt
@sparta_eacf86fcd7
def sparta_5daf0dec43(request):
	D='files[]';A=request;E=A.POST.dict();B=A.FILES
	if D in B:C=qube_f29636d3f5.sparta_524586ce69(E,A.user,B[D])
	else:C={_D:1}
	F=json.dumps(C);return HttpResponse(F)
@csrf_exempt
@sparta_eacf86fcd7
def sparta_b739228637(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_f29636d3f5.sparta_2d4c9acb99(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_eacf86fcd7
def sparta_29f33dc2a9(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_f29636d3f5.sparta_6539e946d6(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_eacf86fcd7
def sparta_cc79d4d2fa(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_f29636d3f5.sparta_c59e69fc1b(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_eacf86fcd7
def sparta_24a7582c14(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_c1b8cdd656.sparta_09fe6c8610(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_eacf86fcd7
def sparta_9d0c217deb(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_f29636d3f5.sparta_1048403f40(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_eacf86fcd7
def sparta_83679e704d(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_f29636d3f5.sparta_e7d8de31d5(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_eacf86fcd7
def sparta_b9489d1de6(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_f29636d3f5.sparta_866f20a121(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_eacf86fcd7
def sparta_b4f4a0a672(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_f29636d3f5.sparta_373767c36f(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_eacf86fcd7
def sparta_dd0fe715d9(request):
	F='filePath';E='fileName';A=request;B=A.GET[E];G=A.GET[F];H=A.GET[_B];I=A.GET[_E];J={E:B,F:G,_E:I,_B:base64.b64decode(H).decode(_G)};C=qube_f29636d3f5.sparta_d3eabc9c21(J,A.user)
	if C[_D]==1:
		try:
			with open(C['fullPath'],'rb')as K:D=HttpResponse(K.read(),content_type='application/force-download');D[_C]='attachment; filename='+str(B);return D
		except Exception as L:pass
	raise Http404
@csrf_exempt
@sparta_eacf86fcd7
def sparta_c798cde2e5(request):
	E='folderName';B=request;F=B.GET[_B];D=B.GET[E];G={_B:base64.b64decode(F).decode(_G),E:D};C=qube_f29636d3f5.sparta_5c923ad42a(G,B.user)
	if C[_D]==1:H=C['zip'];I=C[_H];A=HttpResponse();A.write(H.getvalue());A[_C]=_F.format(f"{I}.zip")
	else:A=HttpResponse();J=f"Could not download the folder {D}, please try again";K=_I;A.write(J);A[_C]=_F.format(K)
	return A
@csrf_exempt
@sparta_eacf86fcd7
def sparta_8ae4311e4e(request):
	B=request;D=B.GET[_E];E=B.GET[_B];F={_E:D,_B:base64.b64decode(E).decode(_G)};C=qube_f29636d3f5.sparta_f08af50e35(F,B.user)
	if C[_D]==1:G=C['zip'];H=C[_H];A=HttpResponse();A.write(G.getvalue());A[_C]=_F.format(f"{H}.zip")
	else:A=HttpResponse();I='Could not download the application, please try again';J=_I;A.write(I);A[_C]=_F.format(J)
	return A