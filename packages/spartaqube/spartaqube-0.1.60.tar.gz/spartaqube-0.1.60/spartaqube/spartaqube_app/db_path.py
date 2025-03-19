import os,sys,getpass,platform
from project.sparta_8f29384cd2.sparta_ccd7e0da68.qube_56413a793d import sparta_21526a056d,sparta_5618ce909a
def sparta_aead81b4e6(full_path,b_print=False):
	B=b_print;A=full_path
	try:
		if not os.path.exists(A):
			os.makedirs(A)
			if B:print(f"Folder created successfully at {A}")
		elif B:print(f"Folder already exists at {A}")
	except Exception as C:print(f"An error occurred: {C}")
def sparta_995a01bc18():
	if sparta_5618ce909a():A='/app/APPDATA/local_db/db.sqlite3'
	else:C=sparta_21526a056d();B=os.path.join(C,'data');sparta_aead81b4e6(B);A=os.path.join(B,'db.sqlite3')
	return A