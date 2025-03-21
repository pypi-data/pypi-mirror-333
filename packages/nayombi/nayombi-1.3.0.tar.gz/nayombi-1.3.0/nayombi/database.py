# database.py
from sqlalchemy import create_engine
from langchain_community.utilities import SQLDatabase
from langchain.chains import create_sql_query_chain
from pymongo import MongoClient  
from elasticsearch import Elasticsearch  
import snowflake.connector  
import pyodbc  
import redis 
from google.cloud import bigquery  
from neo4j import GraphDatabase 
def initialize_database(db_type, db_user, db_password, db_host, db_name, db_port):
    """Initialize database connection."""
    #print(db_type)
    # engine = create_engine(f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}")
    # return SQLDatabase(engine, sample_rows_in_table_info=3)
    if db_type == "postgresql":  
        engine=create_engine(f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}")
        return SQLDatabase(engine, sample_rows_in_table_info=10)  
    elif db_type == "mysql":  
        engine=create_engine(f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}")
        return SQLDatabase(engine, sample_rows_in_table_info=10)  
    elif db_type == "sqlite":  
        engine=create_engine(f"sqlite:///{db_name}")
        return SQLDatabase(engine, sample_rows_in_table_info=10)  
    elif db_type == "mssql":  
        engine=create_engine(f"mssql+pyodbc://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}?driver=ODBC+Driver+17+for+SQL+Server")
        return SQLDatabase(engine, sample_rows_in_table_info=10)  
    elif db_type == "mongodb":  
        # MongoDB requires a different approach, using a separate driver  
        mongo_client=MongoClient(f"mongodb://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}")
        return mongo_client[db_name]  # Return the database instance  

    elif db_type == "elasticsearch":
        # Elasticsearch requires a different approach, using a separate driver  
        es_client = Elasticsearch([f"http://{db_host}:{db_port}"])  
        return es_client  
    elif db_type == "bigquery":
        # BigQuery requires a different approach, using a separate driver  
        client = bigquery.Client(project=db_project, credentials=credentials)  
        return client 
    elif db_type == "snowflake":
        # Snowflake requires a different approach, using a separate driver  
        snowflake_conn = snowflake.connector.connect(user=db_user, password=db_password, account=db_host)  
        return snowflake_conn  
    elif db_type == "teradata":
        # Teradata requires a different approach, using a separate driver  
        teradata_conn = pyodbc.connect(driver='Teradata', server=db_host, database=db_name, uid=db_user, pwd=db_password)  
        return teradata_conn
    elif db_type == "clickhouse":
        from clickhouse_driver import Client
        # Clickhouse requires a different approach, using a separate driver  
        clickhouse_client = Client(host=db_host, user=db_user, password=db_password, database=db_name)  
        return clickhouse_client  
    elif db_type == "redshift":
        # Redshift requires a different approach, using a separate driver  
        redshift_conn = psycopg2.connect(dbname=db_name, user=db_user, password=db_password, host=db_host, port=db_port)  
        return redshift_conn 
    elif db_type == "dask_sql":
        from dask.distributed import Client 
        # Dask SQL requires a different approach, using a separate driver  
        dask_client = Client(f"tcp://{db_host}:{db_port}")  
        return dask_client
    elif db_type == "neo4j":
        # Neo4j requires a different approach, using a separate driver  
        neo4j_driver = GraphDatabase.driver(f"bolt://{db_host}:{db_port}", auth=(db_user, db_password))
        return neo4j_driver#SQLDatabase(engine, sample_rows_in_table_info=3)
    elif db_type == "trino":
        from trino import dbapi 
        # Trino requires a different approach, using a separate driver  
        trino_conn = trino.client.connect(host=db_host, port=db_port, user=db_user, password=db_password, database=db_name)
        return trino_conn
    elif db_type == "redis":
        # Redis requires a different approach, using a separate driver  
        redis_conn = redis.Redis(host=db_host, port=db_port, db=0)
        return redis_conn#SQLDatabase(engine, sample_rows_in_table_info=3)
    else:  
        raise ValueError("Unsupported database type")
def initialize_sql_chain(llm, db):
    """Create the SQL query chain using the LLM and database."""
    return create_sql_query_chain(llm, db)

    #python -m customer_inquiry.main