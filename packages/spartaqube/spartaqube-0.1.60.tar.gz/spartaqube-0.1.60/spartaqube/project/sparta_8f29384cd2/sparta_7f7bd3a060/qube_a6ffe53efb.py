_A='utf-8'
import os,json,base64,hashlib,random
from cryptography.fernet import Fernet
def sparta_0df76d00fb():A='__API_AUTH__';A=A.encode(_A);A=hashlib.md5(A).hexdigest();A=base64.b64encode(A.encode(_A));return A
def sparta_b378bb719d(objectToCrypt):A=objectToCrypt;C=sparta_0df76d00fb();D=Fernet(C);A=A.encode(_A);B=D.encrypt(A).decode(_A);B=base64.b64encode(B.encode(_A)).decode(_A);return B
def sparta_d4d57805cf(apiAuth):A=apiAuth;B=sparta_0df76d00fb();C=Fernet(B);A=base64.b64decode(A);return C.decrypt(A).decode(_A)
def sparta_b88df68541(kCrypt):A='__SQ_AUTH__'+str(kCrypt);A=A.encode(_A);A=hashlib.md5(A).hexdigest();A=base64.b64encode(A.encode(_A));return A
def sparta_e90fff65cc(objectToCrypt,kCrypt):A=objectToCrypt;C=sparta_b88df68541(kCrypt);D=Fernet(C);A=A.encode(_A);B=D.encrypt(A).decode(_A);B=base64.b64encode(B.encode(_A)).decode(_A);return B
def sparta_7ff57394f5(objectToDecrypt,kCrypt):A=objectToDecrypt;B=sparta_b88df68541(kCrypt);C=Fernet(B);A=base64.b64decode(A);return C.decrypt(A).decode(_A)
def sparta_ebddfc8a54(kCrypt):A='__SQ_EMAIL__'+str(kCrypt);A=A.encode(_A);A=hashlib.md5(A).hexdigest();A=base64.b64encode(A.encode(_A));return A
def sparta_e6d7839bf7(objectToCrypt,kCrypt):A=objectToCrypt;C=sparta_ebddfc8a54(kCrypt);D=Fernet(C);A=A.encode(_A);B=D.encrypt(A).decode(_A);B=base64.b64encode(B.encode(_A)).decode(_A);return B
def sparta_a074293899(objectToDecrypt,kCrypt):A=objectToDecrypt;B=sparta_ebddfc8a54(kCrypt);C=Fernet(B);A=base64.b64decode(A);return C.decrypt(A).decode(_A)
def sparta_978dcb27d1(kCrypt):A='__SQ_KEY_SSO_CRYPT__'+str(kCrypt);A=A.encode(_A);A=hashlib.md5(A).hexdigest();A=base64.b64encode(A.encode(_A));return A
def sparta_2ae0596733(objectToCrypt,kCrypt):A=objectToCrypt;C=sparta_978dcb27d1(kCrypt);D=Fernet(C);A=A.encode(_A);B=D.encrypt(A).decode(_A);B=base64.b64encode(B.encode(_A)).decode(_A);return B
def sparta_2b12828dab(objectToDecrypt,kCrypt):A=objectToDecrypt;B=sparta_978dcb27d1(kCrypt);C=Fernet(B);A=base64.b64decode(A);return C.decrypt(A).decode(_A)
def sparta_2a383927d3():A='__SQ_IPYNB_SQ_METADATA__';A=A.encode(_A);A=hashlib.md5(A).hexdigest();A=base64.b64encode(A.encode(_A));return A
def sparta_b9f3fdb991(objectToCrypt):A=objectToCrypt;C=sparta_2a383927d3();D=Fernet(C);A=A.encode(_A);B=D.encrypt(A).decode(_A);B=base64.b64encode(B.encode(_A)).decode(_A);return B
def sparta_c588b11996(objectToDecrypt):A=objectToDecrypt;B=sparta_2a383927d3();C=Fernet(B);A=base64.b64decode(A);return C.decrypt(A).decode(_A)