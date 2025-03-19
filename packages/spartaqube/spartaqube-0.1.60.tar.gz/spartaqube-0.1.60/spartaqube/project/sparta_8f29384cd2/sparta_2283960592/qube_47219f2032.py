_V='kernels'
_U='CommandLine'
_T='%Y-%m-%d %H:%M:%S'
_S='created_time'
_R='created_time_str'
_Q='workspace_variables'
_P='app.settings'
_O='venvName'
_N='kernelType'
_M='Windows'
_L='kernel_process_obj'
_K='spawnKernel.py'
_J='port'
_I='PPID'
_H='kernel_manager_uuid'
_G='name'
_F='-1'
_E=False
_D='kernelManagerUUID'
_C=True
_B='res'
_A=None
import os,sys,gc,socket,subprocess,threading,platform,psutil,zmq,json,base64,shutil,zipfile,io,uuid,cloudpickle
from django.conf import settings
from django.db.models import Q
from django.utils.text import slugify
from datetime import datetime,timedelta
from pathlib import Path
from dateutil import parser
import pytz
UTC=pytz.utc
from django.contrib.humanize.templatetags.humanize import naturalday
from project.models import KernelProcess
from project.sparta_8f29384cd2.sparta_47f0106b48.qube_2d0baaf631 import sparta_fe33ff5f82,sparta_7e4cf39db2,sparta_126c1b60c4
from project.sparta_8f29384cd2.sparta_2283960592.qube_5d2c283999 import SenderKernel
from project.logger_config import logger
def sparta_ab5045bbcd():
	with socket.socket(socket.AF_INET,socket.SOCK_STREAM)as A:A.bind(('',0));return A.getsockname()[1]
class SqKernelManager:
	def __init__(A,kernel_manager_uuid,type,name,user,user_kernel=_A,project_folder=_A,notebook_exec_id=_F,dashboard_exec_id=_F,venv_name=_A):
		C=user_kernel;B=user;A.kernel_manager_uuid=kernel_manager_uuid;A.type=type;A.name=name;A.user=B;A.kernel_user_logged=B;A.project_folder=project_folder
		if C is _A:C=B
		A.user_kernel=C;A.venv_name=venv_name;A.notebook_exec_id=notebook_exec_id;A.dashboard_exec_id=dashboard_exec_id;A.is_init=_E;A.created_time=datetime.now()
	def create_kernel(A,django_settings_module=_A):
		if A.notebook_exec_id!=_F:A.user_kernel=sparta_7e4cf39db2(A.notebook_exec_id)
		if A.dashboard_exec_id!=_F:A.user_kernel=sparta_126c1b60c4(A.dashboard_exec_id)
		G=os.path.dirname(__file__);H=sparta_fe33ff5f82(A.user_kernel);C=sparta_ab5045bbcd();I=sys.executable;J=A.venv_name if A.venv_name is not _A else _F
		def L(pipe):
			for A in iter(pipe.readline,''):logger.debug(A,end='')
			pipe.close()
		E=os.environ.copy();E['ZMQ_PROCESS']='1';logger.debug(f"SPAWN PYTHON KERNEL {C}");K=subprocess.Popen([I,_K,str(H),str(C),J],stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=_C,cwd=G,env=E);F=K.pid;D=datetime.now().astimezone(UTC);B=sparta_8a41a7d617(A.user,A.kernel_manager_uuid)
		if B is _A:B=KernelProcess.objects.create(kernel_manager_uuid=A.kernel_manager_uuid,port=C,pid=F,date_created=D,user=A.user,name=A.name,type=A.type,notebook_exec_id=A.notebook_exec_id,dashboard_exec_id=A.dashboard_exec_id,venv_name=A.venv_name,project_folder=A.project_folder,last_update=D)
		else:B.port=C;B.pid=F;B.name=A.name;B.type=A.type;B.notebook_exec_id=A.notebook_exec_id;B.dashboard_exec_id=A.dashboard_exec_id;B.venv_name=A.venv_name;B.project_folder=A.project_folder;B.last_update=D;B.save()
		return{_B:1,_L:B}
def sparta_45437e8167(kernel_process_obj):A=SenderKernel(websocket=_A,port=kernel_process_obj.port);return A.sync_get_kernel_size()
def sparta_548fe35f60(kernel_process_obj):A=SenderKernel(websocket=_A,port=kernel_process_obj.port);return A.sync_get_kernel_workspace_variables()
def sparta_1343419921(kernel_process_obj,venv_name):A=SenderKernel(websocket=_A,port=kernel_process_obj.port);return A.sync_activate_venv(venv_name)
def sparta_2fac5f26a3(kernel_process_obj,kernel_varname):A=SenderKernel(websocket=_A,port=kernel_process_obj.port);return A.sync_get_kernel_variable_repr(kernel_varname)
def sparta_bef5eda752(kernel_process_obj,var_name,var_value):A=SenderKernel(websocket=_A,port=kernel_process_obj.port);return A.sync_set_workspace_variable(var_name,var_value)
def set_workspace_cloudpickle_variables(kernel_process_obj,cloudpickle_kernel_variables):A=SenderKernel(websocket=_A,port=kernel_process_obj.port);return A.sync_set_workspace_cloudpickle_variables(cloudpickle_kernel_variables)
def sparta_a7ece6e5a2(kernel_process_obj):A=SenderKernel(websocket=_A,port=kernel_process_obj.port);return A.sync_get_cloudpickle_kernel_variables()
def sparta_4effe235a4(pid):
	logger.debug('Force Kill Process now from kernel manager')
	if platform.system()==_M:return sparta_da805f4cc3(pid)
	else:return sparta_8be3fa3af8(pid)
def sparta_da805f4cc3(pid):
	try:subprocess.run(['taskkill','/F','/PID',str(pid)],check=_C,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
	except subprocess.CalledProcessError:logger.debug(f"Failed to kill process {pid}. It may not exist.")
def sparta_8be3fa3af8(pid):
	try:subprocess.run(['kill','-9',str(pid)],check=_C,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
	except subprocess.CalledProcessError:logger.debug(f"Failed to kill process {pid}. It may not exist.")
def sparta_8f450373d8(kernel_process_obj):A=kernel_process_obj.pid;sparta_4effe235a4(A)
def sparta_8a41a7d617(user_obj,kernel_manager_uuid):
	A=KernelProcess.objects.filter(user=user_obj,kernel_manager_uuid=kernel_manager_uuid,is_delete=_E)
	if A.count()>0:return A[0]
def sparta_c48efc7c67(json_data,user_obj,b_return_model=_E):
	E=user_obj;A=json_data;logger.debug('Create new kernel');logger.debug(A);H=A[_D];B=int(A[_N]);I=A.get(_G,'undefined');C=A.get('fullpath',_A);J=A.get('notebookExecId',_F);K=A.get('dashboardExecId',_F);D=A.get(_O,'')
	if len(D)==0:D=_A
	if C is not _A:C=os.path.dirname(C)
	F=SqKernelManager(H,B,I,E,user_kernel=E,project_folder=C,notebook_exec_id=J,dashboard_exec_id=K,venv_name=D)
	if B==3 or B==4 or B==5:G=F.create_kernel(django_settings_module=_P)
	else:G=F.create_kernel()
	if b_return_model:return G
	return{_B:1}
def sparta_e2c1e15a7b(json_data,user_obj):
	C=user_obj;D=json_data[_D];A=sparta_8a41a7d617(C,D)
	if A is not _A:
		sparta_8f450373d8(A);B=A.type;F=A.name;G=A.project_folder;H=A.notebook_exec_id;I=A.dashboard_exec_id;J=A.user_kernel;K=A.venv_name;E=SqKernelManager(D,B,F,C,user_kernel=J,project_folder=G,notebook_exec_id=H,dashboard_exec_id=I,venv_name=K)
		if B==3 or B==4 or B==5:E.create_kernel(django_settings_module=_P)
		else:E.create_kernel()
	return{_B:1}
def sparta_c699806bd7(json_data,user_obj):
	A=json_data
	if _D in A:
		C=A[_D];D=A['env_name'];B=sparta_8a41a7d617(user_obj,C)
		if B is not _A:sparta_1343419921(B,D)
	return{_B:1}
def sparta_8ceef831ba(json_data,user_obj):
	B=json_data[_D];A=sparta_8a41a7d617(user_obj,B)
	if A is not _A:C=sparta_45437e8167(A);D=sparta_548fe35f60(A);return{_B:1,'kernel':{_Q:D,_H:B,'kernel_size':C,'type':A.type,_G:A.name,_R:str(A.date_created.strftime(_T)),_S:naturalday(parser.parse(str(A.date_created)))}}
	return{_B:-1}
def sparta_d5117713d0(json_data,user_obj):
	A=json_data;C=A[_D];D=A['varName'];B=sparta_8a41a7d617(user_obj,C)
	if B is not _A:E=sparta_2fac5f26a3(B,D);return{_B:1,'htmlReprDict':E}
	return{_B:-1}
def sparta_282fdd1025(json_data,user_obj):
	C=json_data;D=C[_D];A=sparta_8a41a7d617(user_obj,D)
	if A is not _A:
		B=C.get(_G,_A)
		if B is not _A:A.name=B;A.save();sparta_bef5eda752(A,_G,B)
	return{_B:1}
def sparta_990defd865():
	if platform.system()==_M:return sparta_ba31cc5c36()
	else:return sparta_7a5b612a90()
def sparta_ba31cc5c36():
	try:
		D=subprocess.run('wmic process where "name=\'python.exe\'" get ProcessId,ParentProcessId,CommandLine /FORMAT:CSV',shell=_C,capture_output=_C,text=_C);C=[];E=D.stdout.splitlines()
		for F in E[2:]:
			A=F.split(',')
			if len(A)<4:continue
			B=A[1].strip();G=A[2].strip();H=A[3].strip();I=B.split(' ')
			if _K in B:C.append({'PID':G,_I:H,_U:B,_J:I[3]})
		return C
	except Exception as J:logger.debug(f"Error finding parent process of spawnKernel.py: {J}");return[]
def sparta_7a5b612a90():
	try:
		D=subprocess.run("ps -eo pid,ppid,command | grep '[s]pawnKernel.py'",shell=_C,capture_output=_C,text=_C);A=[];E=D.stdout.strip().split('\n')
		for F in E:
			B=F.strip().split(maxsplit=2)
			if len(B)<3:continue
			G,H,C=B;I=C.split(' ');A.append({'PID':G,_I:H,_U:C,_J:I[3]})
		return A
	except Exception as J:logger.debug(f"Error finding parent process of spawnKernel.py: {J}");return[]
def sparta_12cc39c2e7(json_data,user_obj):
	I='b_require_workspace_variables';C=user_obj;B=json_data;J=B.get('b_require_size',_E);K=B.get(I,_E);L=B.get(I,_E);D=[]
	if L:from project.sparta_8f29384cd2.sparta_4703a5685b import qube_4cdfa35c2e as M;D=M.sparta_40009fbe54(C)
	N=sparta_990defd865();E=[(A[_I],A[_J])for A in N];O=KernelProcess.objects.filter(pid__in=[A[0]for A in E],port__in=[A[1]for A in E],user=C).distinct();F=[]
	for A in O:
		G=_A
		if J:G=sparta_45437e8167(A)
		H=[]
		if K:H=sparta_548fe35f60(A)
		F.append({_H:A.kernel_manager_uuid,_Q:H,'type':A.type,_G:A.name,_R:str(A.date_created.strftime(_T)),_S:naturalday(parser.parse(str(A.date_created))),'size':G,'isStored':_C if A.kernel_manager_uuid in D else _E})
	return{_B:1,_V:F}
def sparta_a4f23c0b09(json_data,user_obj):
	B=user_obj;from project.sparta_8f29384cd2.sparta_4703a5685b import qube_4cdfa35c2e as D;A=D.sparta_7659a10d5b(B);C=sparta_12cc39c2e7(json_data,B)
	if C[_B]==1:E=C[_V];F=[A[_H]for A in E];A=[A for A in A if A[_H]not in F];return{_B:1,'kernel_library':A}
	return{_B:-1}
def sparta_aff790babc(json_data,user_obj):
	B=json_data[_D];A=sparta_8a41a7d617(user_obj,B)
	if A is not _A:sparta_8f450373d8(A)
	return{_B:1}
def sparta_128ab9645f(json_data,user_obj):
	A=KernelProcess.objects.filter(user=user_obj,is_delete=_E)
	if A.count()>0:
		for B in A:sparta_8f450373d8(B)
	return{_B:1}
def sparta_60856a6f5c(json_data,user_obj):
	C=user_obj;B=json_data;D=B[_D];from project.sparta_8f29384cd2.sparta_4703a5685b import qube_4cdfa35c2e as I;G=I.sparta_afec022fa0(C,D);A=sparta_8a41a7d617(C,D)
	if A is not _A:
		E=A.venv_name
		if E is _A:E=''
		B={_N:100,_D:D,_G:A.name,_O:E};F=sparta_c48efc7c67(B,C,_C)
		if F[_B]==1:
			A=F[_L]
			if G.is_static_variables:
				H=G.kernel_variables
				if H is not _A:set_workspace_cloudpickle_variables(A,H)
		return{_B:F[_B]}
	return{_B:-1}
def sparta_dc70087516(json_data,user_obj):return{_B:1}