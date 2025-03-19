_U='projectPath'
_T='kernelSize'
_S='kernelVenv'
_R='kernel_size'
_Q='main_ipynb_fullpath'
_P='kernel_manager_uuid'
_O='main.ipynb'
_N='-kernel__last_update'
_M='kernel_cpkl_unpicklable'
_L='kernel'
_K='luminoLayout'
_J='description'
_I='slug'
_H='is_static_variables'
_G=False
_F='unpicklable'
_E='name'
_D='kernelManagerUUID'
_C='res'
_B=True
_A=None
import os,sys,gc,json,base64,shutil,zipfile,io,uuid,subprocess,cloudpickle,platform,getpass
from django.conf import settings
from django.db.models import Q
from django.utils.text import slugify
from datetime import datetime,timedelta
from pathlib import Path
from dateutil import parser
import pytz
UTC=pytz.utc
from django.contrib.humanize.templatetags.humanize import naturalday
from project.sparta_8f29384cd2.sparta_63edf7d78c import qube_5af9e48ff5 as qube_5af9e48ff5
from project.models_spartaqube import Kernel,KernelShared,ShareRights
from project.sparta_8f29384cd2.sparta_ccd7e0da68.qube_67447782f4 import sparta_85e1a912d2,sparta_a8c61e81ec
from project.sparta_8f29384cd2.sparta_ccd7e0da68.qube_56413a793d import sparta_21526a056d
from project.sparta_8f29384cd2.sparta_47f0106b48.qube_2d0baaf631 import sparta_2bf050f749,sparta_fe33ff5f82,sparta_7e4cf39db2,sparta_126c1b60c4
from project.sparta_8f29384cd2.sparta_ccd7e0da68.qube_88f6ef1985 import sparta_6dd866c6b7,sparta_9386dcf5bb
from project.sparta_8f29384cd2.sparta_b817db0711.qube_0783bc334a import sparta_309795cbf8
from project.logger_config import logger
def sparta_374b5d65b7():A=sparta_21526a056d();B=os.path.join(A,_L);return B
def sparta_6faeb64289(user_obj):
	A=qube_5af9e48ff5.sparta_9c3e29af31(user_obj)
	if len(A)>0:B=[A.user_group for A in A]
	else:B=[]
	return B
def sparta_1b2981db11(user_obj,kernel_manager_uuid):from project.sparta_8f29384cd2.sparta_2283960592 import qube_47219f2032 as B;E=B.sparta_8a41a7d617(user_obj,kernel_manager_uuid);A=B.sparta_a7ece6e5a2(E);logger.debug('get_cloudpickle_kernel_variables res_dict');logger.debug(A);C=A['picklable'];logger.debug('kernel_cpkl_picklable');logger.debug(type(C));logger.debug("res_dict['unpicklable']");logger.debug(type(A[_F]));D=cloudpickle.loads(A[_F]);logger.debug(_M);logger.debug(type(D));return C,D
def sparta_7659a10d5b(user_obj):
	I='%Y-%m-%d';C=user_obj;J=sparta_374b5d65b7();D=sparta_6faeb64289(C)
	if len(D)>0:B=KernelShared.objects.filter(Q(is_delete=0,user_group__in=D,kernel__is_delete=0)|Q(is_delete=0,user=C,kernel__is_delete=0))
	else:B=KernelShared.objects.filter(Q(is_delete=0,user=C,kernel__is_delete=0))
	if B.count()>0:B=B.order_by(_N)
	E=[]
	for F in B:
		A=F.kernel;K=F.share_rights;G=_A
		try:G=str(A.last_update.strftime(I))
		except:pass
		H=_A
		try:H=str(A.date_created.strftime(I))
		except Exception as L:logger.debug(L)
		M=os.path.join(J,A.kernel_manager_uuid,_O);E.append({_P:A.kernel_manager_uuid,_E:A.name,_I:A.slug,_J:A.description,_Q:M,_R:A.kernel_size,'has_write_rights':K.has_write_rights,'last_update':G,'date_created':H})
	return E
def sparta_40009fbe54(user_obj):
	B=user_obj;C=sparta_6faeb64289(B)
	if len(C)>0:A=KernelShared.objects.filter(Q(is_delete=0,user_group__in=C,kernel__is_delete=0)|Q(is_delete=0,user=B,kernel__is_delete=0))
	else:A=KernelShared.objects.filter(Q(is_delete=0,user=B,kernel__is_delete=0))
	if A.count()>0:A=A.order_by(_N);return[A.kernel.kernel_manager_uuid for A in A]
	return[]
def sparta_afec022fa0(user_obj,kernel_manager_uuid):
	B=user_obj;D=Kernel.objects.filter(kernel_manager_uuid=kernel_manager_uuid).all()
	if D.count()>0:
		A=D[0];E=sparta_6faeb64289(B)
		if len(E)>0:C=KernelShared.objects.filter(Q(is_delete=0,user_group__in=E,kernel__is_delete=0,kernel=A)|Q(is_delete=0,user=B,kernel__is_delete=0,kernel=A))
		else:C=KernelShared.objects.filter(is_delete=0,user=B,kernel__is_delete=0,kernel=A)
		F=_G
		if C.count()>0:
			H=C[0];G=H.share_rights
			if G.is_admin or G.has_write_rights:F=_B
		if F:return A
def sparta_fd92da39c0(json_data,user_obj):
	D=user_obj;from project.sparta_8f29384cd2.sparta_2283960592 import qube_47219f2032 as I;A=json_data[_D];B=I.sparta_8a41a7d617(D,A)
	if B is _A:return{_C:-1,'errorMsg':'Kernel not found'}
	E=sparta_374b5d65b7();J=os.path.join(E,A,_O);K=B.venv_name;F=_A;G=_G;H=_G;C=sparta_afec022fa0(D,A)
	if C is not _A:G=_B;F=C.lumino_layout;H=C.is_static_variables
	return{_C:1,_L:{'basic':{'is_kernel_saved':G,_H:H,_P:A,_E:B.name,'kernel_venv':K,'kernel_type':B.type,'project_path':E,_Q:J},'lumino':{'lumino_layout':F}}}
def sparta_c23300330e(json_data,user_obj):
	D=user_obj;A=json_data;logger.debug('Save notebook');logger.debug(A);logger.debug(A.keys());L=A['isKernelSaved']
	if L:return sparta_6fa8056149(A,D)
	C=datetime.now().astimezone(UTC);G=A[_D];M=A[_K];N=A[_E];O=A[_J];E=sparta_374b5d65b7();E=sparta_85e1a912d2(E);H=A[_H];P=A.get(_S,_A);Q=A.get(_T,0);B=A.get(_I,'')
	if len(B)==0:B=A[_E]
	I=slugify(B);B=I;J=1
	while Kernel.objects.filter(slug=B).exists():B=f"{I}-{J}";J+=1
	K=_A;F=[]
	if H:K,F=sparta_1b2981db11(D,G)
	R=Kernel.objects.create(kernel_manager_uuid=G,name=N,slug=B,description=O,is_static_variables=H,lumino_layout=M,project_path=E,kernel_venv=P,kernel_variables=K,kernel_size=Q,date_created=C,last_update=C,last_date_used=C,spartaqube_version=sparta_309795cbf8());S=ShareRights.objects.create(is_admin=_B,has_write_rights=_B,has_reshare_rights=_B,last_update=C);KernelShared.objects.create(kernel=R,user=D,share_rights=S,is_owner=_B,date_created=C);logger.debug(_M);logger.debug(F);return{_C:1,_F:F}
def sparta_6fa8056149(json_data,user_obj):
	F=user_obj;A=json_data;logger.debug('update_kernel_notebook');logger.debug(A);D=A[_D];B=sparta_afec022fa0(F,D)
	if B is not _A:
		K=datetime.now().astimezone(UTC);D=A[_D];L=A[_K];M=A[_E];N=A[_J];E=A[_H];O=A.get(_S,_A);P=A.get(_T,0);C=A.get(_I,'')
		if len(C)==0:C=A[_E]
		G=slugify(C);C=G;H=1
		while Kernel.objects.filter(slug=C).exists():C=f"{G}-{H}";H+=1
		E=A[_H];I=_A;J=[]
		if E:I,J=sparta_1b2981db11(F,D)
		B.name=M;B.description=N;B.slug=C;B.kernel_venv=O;B.kernel_size=P;B.is_static_variables=E;B.kernel_variables=I;B.lumino_layout=L;B.last_update=K;B.save()
	return{_C:1,_F:J}
def sparta_812df63094(json_data,user_obj):0
def sparta_f0ba66be9d(json_data,user_obj):A=sparta_85e1a912d2(json_data[_U]);return sparta_6dd866c6b7(A)
def sparta_93eec43b59(json_data,user_obj):A=sparta_85e1a912d2(json_data[_U]);return sparta_9386dcf5bb(A)
def sparta_4da1351ed6(json_data,user_obj):
	C=user_obj;B=json_data;logger.debug('SAVE LYUMINO LAYOUT KERNEL NOTEBOOK');logger.debug('json_data');logger.debug(B);I=B[_D];E=Kernel.objects.filter(kernel_manager_uuid=I).all()
	if E.count()>0:
		A=E[0];F=sparta_6faeb64289(C)
		if len(F)>0:D=KernelShared.objects.filter(Q(is_delete=0,user_group__in=F,kernel__is_delete=0,kernel=A)|Q(is_delete=0,user=C,kernel__is_delete=0,kernel=A))
		else:D=KernelShared.objects.filter(is_delete=0,user=C,kernel__is_delete=0,kernel=A)
		G=_G
		if D.count()>0:
			J=D[0];H=J.share_rights
			if H.is_admin or H.has_write_rights:G=_B
		if G:K=B[_K];A.lumino_layout=K;A.save()
	return{_C:1}
def sparta_7bbed313d7(json_data,user_obj):
	from project.sparta_8f29384cd2.sparta_2283960592 import qube_47219f2032 as A;C=json_data[_D];B=A.sparta_8a41a7d617(user_obj,C)
	if B is not _A:D=A.sparta_45437e8167(B);return{_C:1,_R:D}
	return{_C:-1}
def sparta_5e08828e6d(json_data,user_obj):
	B=json_data[_D];A=sparta_afec022fa0(user_obj,B)
	if A is not _A:A.is_delete=_B;A.save()
	return{_C:1}