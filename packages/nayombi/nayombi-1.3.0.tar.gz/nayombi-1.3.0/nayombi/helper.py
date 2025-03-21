# helper.py
from .models import initialize_policy_model, initialize_execution_model
from .database import initialize_database, initialize_sql_chain
from dotenv import load_dotenv
load_dotenv()
import os
import requests  
def nayombi_api(api_key):  
    try:  
        response = requests.post("http://127.0.0.1:5000/get-db-credentials", data={"api_key": api_key})  
        if response.status_code == 200:  
            #print(f"=====================================================\nResponse: {response.status_code} - {response.text}")  
            credentials = response.json()  

            return {
                "db_type": "postgresql",
                "db_user": credentials.get("db_user"),
                "db_password": credentials.get("db_password"),
                "db_host": credentials.get("db_host"),
                "db_name": credentials.get("db_name"),
                "db_port": credentials.get("db_port"),
                "google_api_key": credentials.get("google_api_key"),
                "mistral_api": credentials.get("mistral_api"),
            }  
        else:  
            raise Exception("Failed to retrieve database credentials.")  
    except Exception as e:  
        print(f"An error occurred while fetching DB credentials: {e}")

 
def initialize_system(credentials):
    """Initialize the complete system with models and database."""
    supported_db_types = ["postgresql", "mysql", "sqlite", "mssql", "mongodb",  
                          "elasticsearch", "bigquery", "snowflake", "teradata",  
                          "clickhouse", "redshift", "dask_sql", "neo4j", "trino", "redis"]  
    #print(api_key)
    if credentials["db_type"] not in supported_db_types:  
        raise ValueError(f"Unsupported database type: {db_type}. Supported types: {', '.join(supported_db_types)}")  
    db = initialize_database(
        credentials["db_type"],
        credentials["db_user"],
        credentials["db_password"],
        credentials["db_host"],
        credentials["db_name"],
        credentials["db_port"],
    )
    policy_model = initialize_policy_model(credentials["mistral_api"])
    execution_model = initialize_execution_model(credentials["google_api_key"])
    sql_chain = initialize_sql_chain(execution_model, db)

    return {
        "policy_model": policy_model,
        "execution_model": execution_model,
        "db": db,
        "sql_chain": sql_chain,
    }
