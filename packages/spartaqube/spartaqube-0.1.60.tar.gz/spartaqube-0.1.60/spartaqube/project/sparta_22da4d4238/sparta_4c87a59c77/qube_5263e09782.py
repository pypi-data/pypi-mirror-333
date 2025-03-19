import os
from project.sparta_22da4d4238.sparta_4c87a59c77.qube_4ee8a29da0 import qube_4ee8a29da0
from project.sparta_22da4d4238.sparta_4c87a59c77.qube_e6d6a97184 import qube_e6d6a97184
from project.logger_config import logger
class db_custom_connection:
	def __init__(A):A.dbCon=None;A.dbIdManager='';A.spartAppId=''
	def setSettingsSqlite(B,dbId,dbLocalPath,dbFileNameWithExtension):G='spartApp';E=dbLocalPath;C=dbId;from bqm import settings as F,settingsLocalDesktop as H;B.dbType=0;B.spartAppId=C;A={};A['id']=C;A['ENGINE']='django.db.backends.sqlite3';A['NAME']=str(E)+'/'+str(dbFileNameWithExtension);A['USER']='';A['PASSWORD']='2change';A['HOST']='';A['PORT']='';F.DATABASES[C]=A;H.DATABASES[C]=A;D=qube_e6d6a97184();D.setPath(E);D.setDbName(G);B.dbCon=D;B.dbIdManager=G;logger.debug(F.DATABASES)
	def getConnection(A):return A.dbCon
	def setAuthDB(A,authDB):A.dbType=authDB.dbType