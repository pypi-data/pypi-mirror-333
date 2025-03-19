import os
from project.sparta_22da4d4238.sparta_4c87a59c77.qube_e6d6a97184 import qube_e6d6a97184
from project.sparta_22da4d4238.sparta_4c87a59c77.qube_4ee8a29da0 import qube_4ee8a29da0
from project.sparta_22da4d4238.sparta_4c87a59c77.qube_28dc3339d5 import qube_28dc3339d5
from project.sparta_22da4d4238.sparta_4c87a59c77.qube_c80b441dba import qube_c80b441dba
class db_connection:
	def __init__(A,dbType=0):A.dbType=dbType;A.dbCon=None
	def get_db_type(A):return A.dbType
	def getConnection(A):
		if A.dbType==0:
			from django.conf import settings as B
			if B.PLATFORM in['SANDBOX','SANDBOX_MYSQL']:return
			A.dbCon=qube_e6d6a97184()
		elif A.dbType==1:A.dbCon=qube_4ee8a29da0()
		elif A.dbType==2:A.dbCon=qube_28dc3339d5()
		elif A.dbType==4:A.dbCon=qube_c80b441dba()
		return A.dbCon