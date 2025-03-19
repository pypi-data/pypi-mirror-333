_C='postgres'
_B='json_api'
_A=None
import time,json,pandas as pd
from pandas.api.extensions import no_default
import project.sparta_8f29384cd2.sparta_99ae4fa4f2.qube_663812ae0c as qube_663812ae0c
from project.sparta_8f29384cd2.sparta_99ae4fa4f2.sparta_0b31e27222.qube_da10cb678b import AerospikeConnector
from project.sparta_8f29384cd2.sparta_99ae4fa4f2.sparta_43cafa971c.qube_20dbe1212b import CassandraConnector
from project.sparta_8f29384cd2.sparta_99ae4fa4f2.sparta_ef22a2f722.qube_5ed56e3f1b import ClickhouseConnector
from project.sparta_8f29384cd2.sparta_99ae4fa4f2.sparta_61d7863fff.qube_745a1c238e import CouchdbConnector
from project.sparta_8f29384cd2.sparta_99ae4fa4f2.sparta_b49c454163.qube_94e9977005 import CsvConnector
from project.sparta_8f29384cd2.sparta_99ae4fa4f2.sparta_c2d9321e6c.qube_359cb76e18 import DuckDBConnector
from project.sparta_8f29384cd2.sparta_99ae4fa4f2.sparta_f687e9392b.qube_29aec88d57 import JsonApiConnector
from project.sparta_8f29384cd2.sparta_99ae4fa4f2.sparta_26eb3ad16d.qube_73daf06b60 import InfluxdbConnector
from project.sparta_8f29384cd2.sparta_99ae4fa4f2.sparta_dc3a48e05a.qube_462cfa1416 import MariadbConnector
from project.sparta_8f29384cd2.sparta_99ae4fa4f2.sparta_2e33b4ef6b.qube_d4a1b91d00 import MongoConnector
from project.sparta_8f29384cd2.sparta_99ae4fa4f2.sparta_e19636df4d.qube_f7b01afc06 import MssqlConnector
from project.sparta_8f29384cd2.sparta_99ae4fa4f2.sparta_ebe2a0b30c.qube_13d58a8c6e import MysqlConnector
from project.sparta_8f29384cd2.sparta_99ae4fa4f2.sparta_c1c8524b17.qube_287e40120c import OracleConnector
from project.sparta_8f29384cd2.sparta_99ae4fa4f2.sparta_8e2a19b4a8.qube_c7228f35d1 import ParquetConnector
from project.sparta_8f29384cd2.sparta_99ae4fa4f2.sparta_c4f16270aa.qube_7c240dc6ca import PostgresConnector
from project.sparta_8f29384cd2.sparta_99ae4fa4f2.sparta_86eddeaad3.qube_309d4bd4de import PythonConnector
from project.sparta_8f29384cd2.sparta_99ae4fa4f2.sparta_b4aee54585.qube_fed2c643d7 import QuestDBConnector
from project.sparta_8f29384cd2.sparta_99ae4fa4f2.sparta_173ad045ff.qube_dfcbfc43ca import RedisConnector
from project.sparta_8f29384cd2.sparta_99ae4fa4f2.sparta_f653a73fe4.qube_adb18cca5c import ScylladbConnector
from project.sparta_8f29384cd2.sparta_99ae4fa4f2.sparta_b9490d092a.qube_d874c5343c import SqliteConnector
from project.sparta_8f29384cd2.sparta_99ae4fa4f2.sparta_4cc67c44c6.qube_350131e26a import WssConnector
from project.logger_config import logger
class Connector:
	def __init__(A,db_engine=_C):A.db_engine=db_engine
	def close_db(A):
		try:A.connector.close()
		except:pass
	def init_with_model(C,connector_obj):
		A=connector_obj;E=A.host;F=A.port;G=A.user;H=A.password_e
		try:B=qube_663812ae0c.sparta_d4078e7450(H)
		except:B=_A
		try:
			if A.password is not _A:B=A.password
		except:pass
		I=A.database;J=A.oracle_service_name;K=A.keyspace;L=A.library_arctic;M=A.database_path;N=A.read_only;O=A.json_url;P=A.socket_url;Q=A.db_engine;R=A.csv_path;S=A.csv_delimiter;T=A.token;U=A.organization;V=A.lib_dir;W=A.driver;X=A.trusted_connection;D=[]
		if A.dynamic_inputs is not _A:
			try:D=json.loads(A.dynamic_inputs)
			except:pass
		Y=A.py_code_processing;C.db_engine=Q;C.init_with_params(host=E,port=F,user=G,password=B,database=I,oracle_service_name=J,csv_path=R,csv_delimiter=S,keyspace=K,library_arctic=L,database_path=M,read_only=N,json_url=O,socket_url=P,dynamic_inputs=D,py_code_processing=Y,token=T,organization=U,lib_dir=V,driver=W,trusted_connection=X)
	def init_with_params(A,host,port,user=_A,password=_A,database=_A,oracle_service_name='orcl',csv_path=_A,csv_delimiter=_A,keyspace=_A,library_arctic=_A,database_path=_A,read_only=False,json_url=_A,socket_url=_A,redis_db=0,token=_A,organization=_A,lib_dir=_A,driver=_A,trusted_connection=True,dynamic_inputs=_A,py_code_processing=_A):
		J=keyspace;I=py_code_processing;H=dynamic_inputs;G=database_path;F=database;E=password;D=user;C=port;B=host
		if A.db_engine=='aerospike':A.db_connector=AerospikeConnector(host=B,port=C,user=D,password=E,database=F)
		if A.db_engine=='cassandra':A.db_connector=CassandraConnector(host=B,port=C,user=D,password=E,keyspace=J)
		if A.db_engine=='clickhouse':A.db_connector=ClickhouseConnector(host=B,port=C,database=F,user=D,password=E)
		if A.db_engine=='couchdb':A.db_connector=CouchdbConnector(host=B,port=C,user=D,password=E)
		if A.db_engine=='csv':A.db_connector=CsvConnector(csv_path=csv_path,csv_delimiter=csv_delimiter)
		if A.db_engine=='duckdb':A.db_connector=DuckDBConnector(database_path=G,read_only=read_only)
		if A.db_engine=='influxdb':A.db_connector=InfluxdbConnector(host=B,port=C,token=token,organization=organization,bucket=F,user=D,password=E)
		if A.db_engine==_B:A.db_connector=JsonApiConnector(json_url=json_url,dynamic_inputs=H,py_code_processing=I)
		if A.db_engine=='mariadb':A.db_connector=MariadbConnector(host=B,port=C,user=D,password=E,database=F)
		if A.db_engine=='mongo':A.db_connector=MongoConnector(host=B,port=C,user=D,password=E,database=F)
		if A.db_engine=='mssql':A.db_connector=MssqlConnector(host=B,port=C,trusted_connection=trusted_connection,driver=driver,user=D,password=E,database=F)
		if A.db_engine=='mysql':A.db_connector=MysqlConnector(host=B,port=C,user=D,password=E,database=F)
		if A.db_engine=='oracle':A.db_connector=OracleConnector(host=B,port=C,user=D,password=E,database=F,lib_dir=lib_dir,oracle_service_name=oracle_service_name)
		if A.db_engine=='parquet':A.db_connector=ParquetConnector(database_path=G)
		if A.db_engine==_C:A.db_connector=PostgresConnector(host=B,port=C,user=D,password=E,database=F)
		if A.db_engine=='python':A.db_connector=PythonConnector(py_code_processing=I,dynamic_inputs=H)
		if A.db_engine=='questdb':A.db_connector=QuestDBConnector(host=B,port=C,user=D,password=E,database=F)
		if A.db_engine=='redis':A.db_connector=RedisConnector(host=B,port=C,user=D,password=E,db=redis_db)
		if A.db_engine=='scylladb':A.db_connector=ScylladbConnector(host=B,port=C,user=D,password=E,keyspace=J)
		if A.db_engine=='sqlite':A.db_connector=SqliteConnector(database_path=G)
		if A.db_engine=='wss':A.db_connector=WssConnector(socket_url=socket_url,dynamic_inputs=H,py_code_processing=I)
	def get_db_connector(A):return A.db_connector
	def test_connection(A):return A.db_connector.test_connection()
	def sparta_1ad49902ed(A):return A.db_connector.preview_output_connector()
	def get_error_msg_test_connection(A):return A.db_connector.get_error_msg_test_connection()
	def get_available_tables(A):B=A.db_connector.get_available_tables();return B
	def get_available_views(A):B=A.db_connector.get_available_views();return B
	def get_table_columns(A,table_name):B=A.db_connector.get_table_columns(table_name);return B
	def get_data_table(A,table_name):
		if A.db_engine==_B:return A.db_connector.get_json_api_dataframe()
		else:
			B=A.db_connector.get_data_table(table_name)
			if isinstance(B,pd.DataFrame):return B
			return pd.DataFrame(B)
	def get_data_table_top(A,table_name,top_limit=100):
		if A.db_engine==_B:return A.db_connector.get_json_api_dataframe()
		else:
			B=A.db_connector.get_data_table_top(table_name,top_limit)
			if isinstance(B,pd.DataFrame):return B
			return pd.DataFrame(B)
	def get_data_table_query(A,sql,table_name=_A):return A.db_connector.get_data_table_query(sql,table_name=table_name)