from urllib.parse import urlparse,urlunparse
from django.contrib.auth.decorators import login_required
from django.conf import settings as conf_settings
from django.shortcuts import render
import project.sparta_22da4d4238.sparta_0d12b1779d.qube_bd77c02cd4 as qube_bd77c02cd4
from project.models import UserProfile
from project.sparta_8f29384cd2.sparta_82d887a6fc.qube_83d9f0c2bd import sparta_b8b3df6a31
from project.sparta_8cba795938.sparta_b7b0a2582b.qube_2659e46571 import sparta_10de208115
@sparta_b8b3df6a31
@login_required(redirect_field_name='login')
def sparta_e588da9b44(request,idSection=1):
	B=request;D=UserProfile.objects.get(user=B.user);E=D.avatar
	if E is not None:E=D.avatar.avatar
	C=urlparse(conf_settings.URL_TERMS)
	if not C.scheme:C=urlunparse(C._replace(scheme='http'))
	F={'item':1,'idSection':idSection,'userProfil':D,'avatar':E,'url_terms':C};A=qube_bd77c02cd4.sparta_c1601de691(B);A.update(qube_bd77c02cd4.sparta_d6e03fbf4d(B.user));A.update(F);G='';A['accessKey']=G;A['menuBar']=4;A.update(sparta_10de208115());return render(B,'dist/project/auth/settings.html',A)