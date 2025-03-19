from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from project.sparta_8f29384cd2.sparta_82d887a6fc.qube_83d9f0c2bd import sparta_b8b3df6a31
from project.sparta_8f29384cd2.sparta_c6427943bf import qube_4789605937 as qube_4789605937
from project.models import UserProfile
import project.sparta_22da4d4238.sparta_0d12b1779d.qube_bd77c02cd4 as qube_bd77c02cd4
@sparta_b8b3df6a31
@login_required(redirect_field_name='login')
def sparta_39ce4d19bc(request):
	E='avatarImg';B=request;A=qube_bd77c02cd4.sparta_c1601de691(B);A['menuBar']=-1;F=qube_bd77c02cd4.sparta_d6e03fbf4d(B.user);A.update(F);A[E]='';C=UserProfile.objects.filter(user=B.user)
	if C.count()>0:
		D=C[0];G=D.avatar
		if G is not None:H=D.avatar.image64;A[E]=H
	A['bInvertIcon']=0;return render(B,'dist/project/helpCenter/helpCenter.html',A)
@sparta_b8b3df6a31
@login_required(redirect_field_name='login')
def sparta_27c2b359fc(request):
	A=request;B=UserProfile.objects.filter(user=A.user)
	if B.count()>0:C=B[0];C.has_open_tickets=False;C.save()
	return sparta_39ce4d19bc(A)