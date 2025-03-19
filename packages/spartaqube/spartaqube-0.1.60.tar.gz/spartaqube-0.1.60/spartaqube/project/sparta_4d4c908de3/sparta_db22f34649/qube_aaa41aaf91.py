_A='jsonData'
import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings as conf_settings
from project.models import UserProfile
from project.sparta_8f29384cd2.sparta_2b0da2b63b import qube_d3c777a4a3 as qube_d3c777a4a3
from project.sparta_8f29384cd2.sparta_c6427943bf import qube_4789605937 as qube_4789605937
from project.sparta_8f29384cd2.sparta_82d887a6fc.qube_83d9f0c2bd import sparta_eacf86fcd7
@csrf_exempt
@sparta_eacf86fcd7
def sparta_b867b13182(request):
	B=request;I=json.loads(B.body);C=json.loads(I[_A]);A=B.user;D=0;E=UserProfile.objects.filter(user=A)
	if E.count()>0:
		F=E[0]
		if F.has_open_tickets:
			C['userId']=F.user_profile_id;G=qube_4789605937.sparta_355baa4dc6(A)
			if G['res']==1:D=int(G['nbNotifications'])
	H=qube_d3c777a4a3.sparta_b867b13182(C,A);H['nbNotificationsHelpCenter']=D;J=json.dumps(H);return HttpResponse(J)
@csrf_exempt
@sparta_eacf86fcd7
def sparta_079ba05cbf(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_d3c777a4a3.sparta_09c2e5a469(C,A.user);E=json.dumps(D);return HttpResponse(E)