_O='Please send valid data'
_N='dist/project/auth/resetPasswordChange.html'
_M='captcha'
_L='password'
_K='POST'
_J=False
_I='login'
_H='error'
_G='form'
_F='email'
_E='res'
_D='home'
_C='manifest'
_B='errorMsg'
_A=True
import json,hashlib,uuid
from datetime import datetime
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings as conf_settings
from django.urls import reverse
import project.sparta_22da4d4238.sparta_0d12b1779d.qube_bd77c02cd4 as qube_bd77c02cd4
from project.forms import ConnexionForm,RegistrationTestForm,RegistrationBaseForm,RegistrationForm,ResetPasswordForm,ResetPasswordChangeForm
from project.sparta_8f29384cd2.sparta_82d887a6fc.qube_83d9f0c2bd import sparta_b8b3df6a31
from project.sparta_8f29384cd2.sparta_82d887a6fc import qube_83d9f0c2bd as qube_83d9f0c2bd
from project.sparta_4d4c908de3.sparta_094a02ffbe import qube_8c8c54a166 as qube_8c8c54a166
from project.models import LoginLocation,UserProfile
from project.logger_config import logger
def sparta_10de208115():return{'bHasCompanyEE':-1}
def sparta_a257d70373(request):B=request;A=qube_bd77c02cd4.sparta_c1601de691(B);A[_C]=qube_bd77c02cd4.sparta_ab7a20c9e0();A['forbiddenEmail']=conf_settings.FORBIDDEN_EMAIL;return render(B,'dist/project/auth/banned.html',A)
@sparta_b8b3df6a31
def sparta_c54daa96e6(request):
	C=request;B='/';A=C.GET.get(_I)
	if A is not None:D=A.split(B);A=B.join(D[1:]);A=A.replace(B,'$@$')
	return sparta_5f55f5d1c3(C,A)
def sparta_bd8d67bc5a(request,redirectUrl):return sparta_5f55f5d1c3(request,redirectUrl)
def sparta_5f55f5d1c3(request,redirectUrl):
	E=redirectUrl;A=request;logger.debug('Welcome to loginRedirectFunc')
	if A.user.is_authenticated:return redirect(_D)
	G=_J;H='Email or password incorrect'
	if A.method==_K:
		C=ConnexionForm(A.POST)
		if C.is_valid():
			I=C.cleaned_data[_F];J=C.cleaned_data[_L];F=authenticate(username=I,password=J)
			if F:
				if qube_83d9f0c2bd.sparta_46b6eeed08(F):return sparta_a257d70373(A)
				login(A,F);K,L=qube_bd77c02cd4.sparta_acb4d647fc();LoginLocation.objects.create(user=F,hostname=K,ip=L,date_login=datetime.now())
				if E is not None:
					D=E.split('$@$');D=[A for A in D if len(A)>0]
					if len(D)>1:M=D[0];return redirect(reverse(M,args=D[1:]))
					return redirect(E)
				return redirect(_D)
			else:G=_A
		else:G=_A
	C=ConnexionForm();B=qube_bd77c02cd4.sparta_c1601de691(A);B.update(qube_bd77c02cd4.sparta_862ad283d7(A));B[_C]=qube_bd77c02cd4.sparta_ab7a20c9e0();B[_G]=C;B[_H]=G;B['redirectUrl']=E;B[_B]=H;B.update(sparta_10de208115());return render(A,'dist/project/auth/login.html',B)
def sparta_7482a114e8(request):
	B='public@spartaqube.com';A=User.objects.filter(email=B).all()
	if A.count()>0:C=A[0];login(request,C)
	return redirect(_D)
@sparta_b8b3df6a31
def sparta_0e965404c6(request):
	A=request
	if A.user.is_authenticated:return redirect(_D)
	E='';D=_J;F=qube_83d9f0c2bd.sparta_9f5bd0c966()
	if A.method==_K:
		if F:B=RegistrationForm(A.POST)
		else:B=RegistrationBaseForm(A.POST)
		if B.is_valid():
			I=B.cleaned_data;H=None
			if F:
				H=B.cleaned_data['code']
				if not qube_83d9f0c2bd.sparta_1ba213f588(H):D=_A;E='Wrong guest code'
			if not D:
				J=A.META['HTTP_HOST'];G=qube_83d9f0c2bd.sparta_900159f8f3(I,J)
				if int(G[_E])==1:K=G['userObj'];login(A,K);return redirect(_D)
				else:D=_A;E=G[_B]
		else:D=_A;E=B.errors.as_data()
	if F:B=RegistrationForm()
	else:B=RegistrationBaseForm()
	C=qube_bd77c02cd4.sparta_c1601de691(A);C.update(qube_bd77c02cd4.sparta_862ad283d7(A));C[_C]=qube_bd77c02cd4.sparta_ab7a20c9e0();C[_G]=B;C[_H]=D;C[_B]=E;C.update(sparta_10de208115());return render(A,'dist/project/auth/registration.html',C)
def sparta_dad3a1a910(request):A=request;B=qube_bd77c02cd4.sparta_c1601de691(A);B[_C]=qube_bd77c02cd4.sparta_ab7a20c9e0();return render(A,'dist/project/auth/registrationPending.html',B)
def sparta_2d586ba6c7(request,token):
	A=request;B=qube_83d9f0c2bd.sparta_1eb11776d1(token)
	if int(B[_E])==1:C=B['user'];login(A,C);return redirect(_D)
	D=qube_bd77c02cd4.sparta_c1601de691(A);D[_C]=qube_bd77c02cd4.sparta_ab7a20c9e0();return redirect(_I)
def sparta_a5fde9ca88(request):logout(request);return redirect(_I)
def sparta_8821596ec3(request):
	A=request
	if A.user.is_authenticated:
		if A.user.email=='cypress_tests@gmail.com':A.user.delete()
	logout(A);return redirect(_I)
def sparta_aacb1b1d7c(request):A={_E:-100,_B:'You are not logged...'};B=json.dumps(A);return HttpResponse(B)
@csrf_exempt
def sparta_43c0014aeb(request):
	A=request;E='';F=_J
	if A.method==_K:
		B=ResetPasswordForm(A.POST)
		if B.is_valid():
			H=B.cleaned_data[_F];I=B.cleaned_data[_M];G=qube_83d9f0c2bd.sparta_43c0014aeb(H.lower(),I)
			try:
				if int(G[_E])==1:C=qube_bd77c02cd4.sparta_c1601de691(A);C.update(qube_bd77c02cd4.sparta_862ad283d7(A));B=ResetPasswordChangeForm(A.POST);C[_C]=qube_bd77c02cd4.sparta_ab7a20c9e0();C[_G]=B;C[_F]=H;C[_H]=F;C[_B]=E;return render(A,_N,C)
				elif int(G[_E])==-1:E=G[_B];F=_A
			except Exception as J:logger.debug('exception ');logger.debug(J);E='Could not send reset email, please try again';F=_A
		else:E=_O;F=_A
	else:B=ResetPasswordForm()
	D=qube_bd77c02cd4.sparta_c1601de691(A);D.update(qube_bd77c02cd4.sparta_862ad283d7(A));D[_C]=qube_bd77c02cd4.sparta_ab7a20c9e0();D[_G]=B;D[_H]=F;D[_B]=E;D.update(sparta_10de208115());return render(A,'dist/project/auth/resetPassword.html',D)
@csrf_exempt
def sparta_baa34c1502(request):
	D=request;E='';B=_J
	if D.method==_K:
		C=ResetPasswordChangeForm(D.POST)
		if C.is_valid():
			I=C.cleaned_data['token'];F=C.cleaned_data[_L];J=C.cleaned_data['password_confirmation'];K=C.cleaned_data[_M];G=C.cleaned_data[_F].lower()
			if len(F)<6:E='Your password must be at least 6 characters';B=_A
			if F!=J:E='The two passwords must be identical...';B=_A
			if not B:
				H=qube_83d9f0c2bd.sparta_baa34c1502(K,I,G.lower(),F)
				try:
					if int(H[_E])==1:L=User.objects.get(username=G);login(D,L);return redirect(_D)
					else:E=H[_B];B=_A
				except Exception as M:E='Could not change your password, please try again';B=_A
		else:E=_O;B=_A
	else:return redirect('reset-password')
	A=qube_bd77c02cd4.sparta_c1601de691(D);A.update(qube_bd77c02cd4.sparta_862ad283d7(D));A[_C]=qube_bd77c02cd4.sparta_ab7a20c9e0();A[_G]=C;A[_H]=B;A[_B]=E;A[_F]=G;A.update(sparta_10de208115());return render(D,_N,A)