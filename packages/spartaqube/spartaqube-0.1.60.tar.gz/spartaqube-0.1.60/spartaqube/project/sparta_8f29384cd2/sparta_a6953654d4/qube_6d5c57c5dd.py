import os,zipfile,pytz
UTC=pytz.utc
from django.conf import settings as conf_settings
def sparta_d19467f4ad():
	B='APPDATA'
	if conf_settings.PLATFORMS_NFS:
		A='/var/nfs/notebooks/'
		if not os.path.exists(A):os.makedirs(A)
		return A
	if conf_settings.PLATFORM=='LOCAL_DESKTOP'or conf_settings.IS_LOCAL_PLATFORM:
		if conf_settings.PLATFORM_DEBUG=='DEBUG-CLIENT-2':return os.path.join(os.environ[B],'SpartaQuantNB/CLIENT2')
		return os.path.join(os.environ[B],'SpartaQuantNB')
	if conf_settings.PLATFORM=='LOCAL_CE':return'/app/notebooks/'
def sparta_9949daa3ee(userId):A=sparta_d19467f4ad();B=os.path.join(A,userId);return B
def sparta_081a71087f(notebookProjectId,userId):A=sparta_9949daa3ee(userId);B=os.path.join(A,notebookProjectId);return B
def sparta_3dd5e83902(notebookProjectId,userId):A=sparta_9949daa3ee(userId);B=os.path.join(A,notebookProjectId);return os.path.exists(B)
def sparta_1699ebdeae(notebookProjectId,userId,ipynbFileName):A=sparta_9949daa3ee(userId);B=os.path.join(A,notebookProjectId);return os.path.isfile(os.path.join(B,ipynbFileName))
def sparta_ba7ece9659(notebookProjectId,userId):
	C=userId;B=notebookProjectId;D=sparta_081a71087f(B,C);G=sparta_9949daa3ee(C);A=f"{G}/zipTmp/"
	if not os.path.exists(A):os.makedirs(A)
	H=f"{A}/{B}.zip";E=zipfile.ZipFile(H,'w',zipfile.ZIP_DEFLATED);I=len(D)+1
	for(J,M,K)in os.walk(D):
		for L in K:F=os.path.join(J,L);E.write(F,F[I:])
	return E
def sparta_074a76d1d8(notebookProjectId,userId):B=userId;A=notebookProjectId;sparta_ba7ece9659(A,B);C=f"{A}.zip";D=sparta_9949daa3ee(B);E=f"{D}/zipTmp/{A}.zip";F=open(E,'rb');return{'zipName':C,'zipObj':F}