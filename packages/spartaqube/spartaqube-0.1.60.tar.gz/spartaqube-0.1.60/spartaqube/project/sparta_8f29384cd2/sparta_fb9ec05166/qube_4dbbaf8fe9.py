_H='execution_count'
_G='cell_type'
_F='code'
_E='outputs'
_D='source'
_C='cells'
_B='sqMetadata'
_A='metadata'
import os,re,uuid,json
from datetime import datetime
from nbconvert.filters import strip_ansi
from project.sparta_8f29384cd2.sparta_7f7bd3a060 import qube_a6ffe53efb as qube_a6ffe53efb
from project.sparta_8f29384cd2.sparta_ccd7e0da68.qube_67447782f4 import sparta_85e1a912d2,sparta_a8c61e81ec
from project.logger_config import logger
def sparta_433dac1784(file_path):return os.path.isfile(file_path)
def sparta_ec025832fe():return qube_a6ffe53efb.sparta_b9f3fdb991(json.dumps({'date':str(datetime.now())}))
def sparta_9f17fbd048():B='python';A='name';C={'kernelspec':{'display_name':'Python 3 (ipykernel)','language':B,A:'python3'},'language_info':{'codemirror_mode':{A:'ipython','version':3},'file_extension':'.py','mimetype':'text/x-python',A:B,'nbconvert_exporter':B,'pygments_lexer':'ipython3'},_B:sparta_ec025832fe()};return C
def sparta_a9c7362d01():return{_G:_F,_D:[''],_A:{},_H:None,_E:[]}
def sparta_137d4db105():return[sparta_a9c7362d01()]
def sparta_92b6d748e3():return{'nbformat':4,'nbformat_minor':0,_A:sparta_9f17fbd048(),_C:[]}
def sparta_3a338a2623(first_cell_code=''):A=sparta_92b6d748e3();B=sparta_a9c7362d01();B[_D]=[first_cell_code];A[_C]=[B];return A
def sparta_9fc8da6827(full_path):
	A=full_path
	if sparta_433dac1784(A):return sparta_e0ebaeaa34(A)
	else:return sparta_3a338a2623()
def sparta_e0ebaeaa34(full_path):return sparta_64dfcf8386(full_path)
def sparta_db6e540588():A=sparta_92b6d748e3();B=json.loads(qube_a6ffe53efb.sparta_c588b11996(A[_A][_B]));A[_A][_B]=B;return A
def sparta_64dfcf8386(full_path):
	with open(full_path)as C:B=C.read()
	if len(B)==0:A=sparta_92b6d748e3()
	else:A=json.loads(B)
	A=sparta_d1b6e80f8a(A);return A
def sparta_d1b6e80f8a(ipynb_dict):
	A=ipynb_dict;C=list(A.keys())
	if _C in C:
		D=A[_C]
		for B in D:
			if _A in list(B.keys()):
				if _B in B[_A]:B[_A][_B]=qube_a6ffe53efb.sparta_c588b11996(B[_A][_B])
	try:A[_A][_B]=json.loads(qube_a6ffe53efb.sparta_c588b11996(A[_A][_B]))
	except:A[_A][_B]=json.loads(qube_a6ffe53efb.sparta_c588b11996(sparta_ec025832fe()))
	return A
def sparta_38595e9788(full_path):
	B=full_path;A=dict()
	with open(B)as C:A=C.read()
	if len(A)==0:A=sparta_db6e540588();A[_A][_B]=json.dumps(A[_A][_B])
	else:
		A=json.loads(A)
		if _A in list(A.keys()):
			if _B in list(A[_A].keys()):A=sparta_d1b6e80f8a(A);A[_A][_B]=json.dumps(A[_A][_B])
	A['fullPath']=B;return A
def save_ipnyb_from_notebook_cells(notebook_cells_arr,full_path,dashboard_id='-1'):
	R='output_type';Q='markdown';L=full_path;K='tmp_idx';B=[]
	for A in notebook_cells_arr:
		A['bIsComputing']=False;S=A['bDelete'];F=A['cellType'];M=A[_F];T=A['positionIndex'];A[_D]=[M];G=A.get('ipynbOutput',[]);C=A.get('ipynbError',[]);logger.debug('ipynb_output_list');logger.debug(G);logger.debug(type(G));logger.debug('ipynb_error_list');logger.debug(C);logger.debug(type(C));logger.debug('this_cell_dict');logger.debug(A)
		if int(S)==0:
			if F==0:H=_F
			elif F==1:H=Q
			elif F==2:H=Q
			elif F==3:H='raw'
			D={_A:{_B:qube_a6ffe53efb.sparta_b9f3fdb991(json.dumps(A))},'id':uuid.uuid4().hex[:8],_G:H,_D:[M],_H:None,K:T,_E:[]}
			if len(G)>0:
				N=[]
				for E in G:O={};O[E['type']]=[E['output']];N.append({'data':O,R:'execute_result'})
				D[_E]=N
			elif len(C)>0:
				D[_E]=C
				try:
					J=[];U=re.compile('<ipython-input-\\d+-[0-9a-f]+>')
					for E in C:E[R]='error';J+=[re.sub(U,'<IPY-INPUT>',strip_ansi(A))for A in E['traceback']]
					if len(J)>0:D['tbErrors']='\n'.join(J)
				except Exception as V:logger.debug('Except prepare error output traceback with msg:');logger.debug(V)
			else:D[_E]=[]
			B.append(D)
	B=sorted(B,key=lambda d:d[K]);[A.pop(K,None)for A in B];I=sparta_9fc8da6827(L);P=I[_A][_B];P['identifier']={'dashboardId':dashboard_id};I[_A][_B]=qube_a6ffe53efb.sparta_b9f3fdb991(json.dumps(P));I[_C]=B
	with open(L,'w')as W:json.dump(I,W,indent=4)
	return{'res':1}
def sparta_a75416a72c(full_path):
	A=full_path;A=sparta_85e1a912d2(A);C=dict()
	with open(A)as D:E=D.read();C=json.loads(E)
	F=C[_C];B=[]
	for G in F:B.append({_F:G[_D][0]})
	logger.debug('notebook_cells_list');logger.debug(B);return B