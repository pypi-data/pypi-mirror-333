_O='serialized_data'
_N='has_access'
_M='plot_name'
_L='plot_chart_id'
_K='dist/project/plot-db/plotDB.html'
_J='edit_chart_id'
_I='edit'
_H='plot_db_chart_obj'
_G=False
_F='login'
_E='-1'
_D='bCodeMirror'
_C='menuBar'
_B=None
_A=True
import json,base64
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import project.sparta_22da4d4238.sparta_0d12b1779d.qube_bd77c02cd4 as qube_bd77c02cd4
from project.sparta_8f29384cd2.sparta_82d887a6fc.qube_83d9f0c2bd import sparta_b8b3df6a31
from project.sparta_8f29384cd2.sparta_a6d0a04f89 import qube_0fa16a97bc as qube_0fa16a97bc
from project.sparta_8f29384cd2.sparta_65ecb68b5b import qube_8c7b66e0b7 as qube_8c7b66e0b7
@csrf_exempt
@sparta_b8b3df6a31
@login_required(redirect_field_name=_F)
def sparta_4732de655b(request):
	B=request;C=B.GET.get(_I)
	if C is _B:C=_E
	A=qube_bd77c02cd4.sparta_c1601de691(B);A[_C]=7;D=qube_bd77c02cd4.sparta_d6e03fbf4d(B.user);A.update(D);A[_D]=_A;A[_J]=C;return render(B,_K,A)
@csrf_exempt
@sparta_b8b3df6a31
@login_required(redirect_field_name=_F)
def sparta_651b8ae8c9(request):
	B=request;C=B.GET.get(_I)
	if C is _B:C=_E
	A=qube_bd77c02cd4.sparta_c1601de691(B);A[_C]=10;D=qube_bd77c02cd4.sparta_d6e03fbf4d(B.user);A.update(D);A[_D]=_A;A[_J]=C;return render(B,_K,A)
@csrf_exempt
@sparta_b8b3df6a31
@login_required(redirect_field_name=_F)
def sparta_e26a9f568a(request):
	B=request;C=B.GET.get(_I)
	if C is _B:C=_E
	A=qube_bd77c02cd4.sparta_c1601de691(B);A[_C]=11;D=qube_bd77c02cd4.sparta_d6e03fbf4d(B.user);A.update(D);A[_D]=_A;A[_J]=C;return render(B,_K,A)
@csrf_exempt
@sparta_b8b3df6a31
@login_required(redirect_field_name=_F)
def sparta_1bdb7f38c2(request):
	A=request;C=A.GET.get('id');D=_G
	if C is _B:D=_A
	else:E=qube_0fa16a97bc.sparta_8658beaa7a(C,A.user);D=not E[_N]
	if D:return sparta_4732de655b(A)
	B=qube_bd77c02cd4.sparta_c1601de691(A);B[_C]=7;F=qube_bd77c02cd4.sparta_d6e03fbf4d(A.user);B.update(F);B[_D]=_A;B[_L]=C;G=E[_H];B[_M]=G.name;return render(A,'dist/project/plot-db/plotFull.html',B)
@csrf_exempt
@sparta_b8b3df6a31
def sparta_026cda8733(request,id,api_token_id=_B):
	A=request
	if id is _B:B=A.GET.get('id')
	else:B=id
	return plot_widget_func(A,B)
@csrf_exempt
@sparta_b8b3df6a31
def sparta_0c010e986a(request,dashboard_id,id,password):
	A=request
	if id is _B:B=A.GET.get('id')
	else:B=id
	C=base64.b64decode(password).decode();return plot_widget_func(A,B,dashboard_id=dashboard_id,dashboard_password=C)
@csrf_exempt
@sparta_b8b3df6a31
def sparta_56fe976f41(request,widget_id,session_id,api_token_id):return plot_widget_func(request,widget_id,session_id)
def plot_widget_func(request,plot_chart_id,session=_E,dashboard_id=_E,token_permission='',dashboard_password=_B):
	K='token_permission';I=dashboard_id;H=plot_chart_id;G='res';E=token_permission;D=request;C=_G
	if H is _B:C=_A
	else:
		B=qube_0fa16a97bc.sparta_02e99f72ee(H,D.user);F=B[G]
		if F==-1:C=_A
	if C:
		if I!=_E:
			B=qube_8c7b66e0b7.has_plot_db_access(I,H,D.user,dashboard_password);F=B[G]
			if F==1:E=B[K];C=_G
	if C:
		if len(E)>0:
			B=qube_0fa16a97bc.sparta_09a235a7b1(E);F=B[G]
			if F==1:C=_G
	if C:return sparta_4732de655b(D)
	A=qube_bd77c02cd4.sparta_c1601de691(D);A[_C]=7;L=qube_bd77c02cd4.sparta_d6e03fbf4d(D.user);A.update(L);A[_D]=_A;J=B[_H];A['b_require_password']=0 if B[G]==1 else 1;A[_L]=J.plot_chart_id;A[_M]=J.name;A['session']=str(session);A['is_dashboard_widget']=1 if I!=_E else 0;A['is_token']=1 if len(E)>0 else 0;A[K]=str(E);return render(D,'dist/project/plot-db/widgets.html',A)
@csrf_exempt
def sparta_d10e2445c3(request,token):return plot_widget_func(request,plot_chart_id=_B,token_permission=token)
@csrf_exempt
@sparta_b8b3df6a31
def sparta_aec30d98b2(request):B=request;A=qube_bd77c02cd4.sparta_c1601de691(B);A[_C]=7;C=qube_bd77c02cd4.sparta_d6e03fbf4d(B.user);A.update(C);A[_D]=_A;A[_O]=B.POST.get('data');return render(B,'dist/project/plot-db/plotGUI.html',A)
@csrf_exempt
@sparta_b8b3df6a31
@login_required(redirect_field_name=_F)
def sparta_d99756f8fb(request,id):
	K=',\n    ';B=request;C=id;F=_G
	if C is _B:F=_A
	else:G=qube_0fa16a97bc.sparta_8658beaa7a(C,B.user);F=not G[_N]
	if F:return sparta_4732de655b(B)
	L=qube_0fa16a97bc.sparta_e9ab51e5af(G[_H]);D='';H=0
	for(E,I)in L.items():
		if H>0:D+=K
		if I==1:D+=f"{E}=input_{E}"
		else:M=str(K.join([f"input_{E}_{A}"for A in range(I)]));D+=f"{E}=[{M}]"
		H+=1
	J=f"'{C}'";N=f"\n    {J}\n";O=f"Spartaqube().get_widget({N})";P=f"\n    {J},\n    {D}\n";Q=f"Spartaqube().plot({P})";A=qube_bd77c02cd4.sparta_c1601de691(B);A[_C]=7;R=qube_bd77c02cd4.sparta_d6e03fbf4d(B.user);A.update(R);A[_D]=_A;A[_L]=C;S=G[_H];A[_M]=S.name;A['plot_data_cmd']=O;A['plot_data_cmd_inputs']=Q;return render(B,'dist/project/plot-db/plotGUISaved.html',A)
@csrf_exempt
@sparta_b8b3df6a31
def sparta_c7e55227eb(request,json_vars_html):B=request;A=qube_bd77c02cd4.sparta_c1601de691(B);A[_C]=7;C=qube_bd77c02cd4.sparta_d6e03fbf4d(B.user);A.update(C);A[_D]=_A;A.update(json.loads(json_vars_html));A[_O]=B.POST.get('data');return render(B,'dist/project/plot-db/plotAPI.html',A)