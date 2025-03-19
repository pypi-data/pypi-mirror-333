_E='Content-Disposition'
_D='utf-8'
_C='dashboardId'
_B='projectPath'
_A='jsonData'
import os,json,base64
from django.http import HttpResponse,Http404
from django.views.decorators.csrf import csrf_exempt
from project.sparta_8f29384cd2.sparta_fb9ec05166 import qube_41bea18a45 as qube_41bea18a45
from project.sparta_8f29384cd2.sparta_fb9ec05166 import qube_4be14fa1c6 as qube_4be14fa1c6
from project.sparta_8f29384cd2.sparta_65ecb68b5b import qube_8c7b66e0b7 as qube_8c7b66e0b7
from project.sparta_8f29384cd2.sparta_82d887a6fc.qube_83d9f0c2bd import sparta_eacf86fcd7,sparta_d929ec2b9c
@csrf_exempt
def sparta_bd3a162551(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_41bea18a45.sparta_bd3a162551(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_eacf86fcd7
def sparta_e64c117ec9(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_41bea18a45.sparta_e64c117ec9(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_eacf86fcd7
def sparta_e41af95d6c(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_41bea18a45.sparta_e41af95d6c(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_eacf86fcd7
def sparta_8ddd84b41a(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_41bea18a45.sparta_8ddd84b41a(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_eacf86fcd7
@sparta_d929ec2b9c
def sparta_256534f6fe(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_41bea18a45.sparta_256534f6fe(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_eacf86fcd7
def sparta_a574e334a5(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_41bea18a45.sparta_a574e334a5(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_eacf86fcd7
def sparta_dabd5b2b55(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_41bea18a45.sparta_dabd5b2b55(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_eacf86fcd7
def sparta_92eaed04f8(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_41bea18a45.sparta_92eaed04f8(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_eacf86fcd7
def sparta_054fedd1ab(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_41bea18a45.sparta_054fedd1ab(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_eacf86fcd7
def sparta_18bf7d6294(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_41bea18a45.sparta_18bf7d6294(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_eacf86fcd7
def sparta_7cbc121f6a(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_41bea18a45.dashboard_project_explorer_delete_multiple_resources(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_eacf86fcd7
def sparta_77793b1635(request):A=request;B=A.POST.dict();C=A.FILES;D=qube_41bea18a45.sparta_77793b1635(B,A.user,C['files[]']);E=json.dumps(D);return HttpResponse(E)
def sparta_896246dd78(path):
	A=path;A=os.path.normpath(A)
	if os.path.isfile(A):A=os.path.dirname(A)
	return os.path.basename(A)
def sparta_cf6202cd8b(path):A=path;A=os.path.normpath(A);return os.path.basename(A)
@csrf_exempt
@sparta_eacf86fcd7
def sparta_9b656ac921(request):
	E='pathResource';A=request;B=A.GET[E];B=base64.b64decode(B).decode(_D);F=A.GET[_B];G=A.GET[_C];H=sparta_cf6202cd8b(B);I={E:B,_C:G,_B:base64.b64decode(F).decode(_D)};C=qube_41bea18a45.sparta_d3eabc9c21(I,A.user)
	if C['res']==1:
		try:
			with open(C['fullPath'],'rb')as J:D=HttpResponse(J.read(),content_type='application/force-download');D[_E]='attachment; filename='+str(H);return D
		except Exception as K:pass
	raise Http404
@csrf_exempt
@sparta_eacf86fcd7
def sparta_38bbe593b3(request):
	D='attachment; filename={0}';B=request;E=B.GET[_C];F=B.GET[_B];G={_C:E,_B:base64.b64decode(F).decode(_D)};C=qube_41bea18a45.sparta_f08af50e35(G,B.user)
	if C['res']==1:H=C['zip'];I=C['zipName'];A=HttpResponse();A.write(H.getvalue());A[_E]=D.format(f"{I}.zip")
	else:A=HttpResponse();J='Could not download the application, please try again';K='error.txt';A.write(J);A[_E]=D.format(K)
	return A
@csrf_exempt
@sparta_eacf86fcd7
@sparta_d929ec2b9c
def sparta_0857ed96db(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_4be14fa1c6.sparta_0857ed96db(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_eacf86fcd7
@sparta_d929ec2b9c
def sparta_9624308c11(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_4be14fa1c6.sparta_9624308c11(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_eacf86fcd7
@sparta_d929ec2b9c
def sparta_24d5a1fd9c(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_4be14fa1c6.sparta_24d5a1fd9c(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_eacf86fcd7
@sparta_d929ec2b9c
def sparta_6967f08227(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_4be14fa1c6.sparta_6967f08227(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_eacf86fcd7
@sparta_d929ec2b9c
def sparta_89351e9cc1(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_4be14fa1c6.sparta_89351e9cc1(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_eacf86fcd7
@sparta_d929ec2b9c
def sparta_8e16165b4f(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_4be14fa1c6.sparta_8e16165b4f(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_eacf86fcd7
@sparta_d929ec2b9c
def sparta_51161f9a84(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_4be14fa1c6.sparta_51161f9a84(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_eacf86fcd7
@sparta_d929ec2b9c
def sparta_dc7780ed58(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_4be14fa1c6.sparta_dc7780ed58(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_eacf86fcd7
@sparta_d929ec2b9c
def sparta_0b2e776df7(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_4be14fa1c6.sparta_0b2e776df7(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_eacf86fcd7
@sparta_d929ec2b9c
def sparta_24eb26ee27(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_4be14fa1c6.sparta_24eb26ee27(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_eacf86fcd7
@sparta_d929ec2b9c
def sparta_dc7d375192(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_4be14fa1c6.sparta_dc7d375192(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_eacf86fcd7
@sparta_d929ec2b9c
def sparta_6ceec3e50e(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_4be14fa1c6.sparta_6ceec3e50e(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_eacf86fcd7
@sparta_d929ec2b9c
def sparta_0aadfc023b(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_4be14fa1c6.sparta_0aadfc023b(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_eacf86fcd7
@sparta_d929ec2b9c
def sparta_5f07e8560d(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_4be14fa1c6.sparta_5f07e8560d(C,A.user);E=json.dumps(D);return HttpResponse(E)