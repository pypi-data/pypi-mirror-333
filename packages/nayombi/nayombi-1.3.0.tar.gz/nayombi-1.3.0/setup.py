from setuptools import setup, find_packages

setup(
    name="nayombi",
    version="1.3.0",
    description="Handle customer inquiries with AI and database integration",
    author="Marvin avi",
    author_email="marvinavi24@gmail.com",
    packages = find_packages(),    
    install_requires = [ 
        "langchain-core==0.3.45",  
        "langchain-google-genai==2.0.10",  
        "langchain-mistralai==0.2.8", 
        "langchain-community==0.3.19",
        "langchain==0.3.20", 
        "google-ai-generativelanguage==0.6.15",
        # "langchain-openai>=0.3.7,<0.4.0",  
        # # "multidict>=6.1.0,<7.0.0",  
        # "mysql-connector-python",  
        # # "neo4j>=5.28.1,<6.0.0",  
        # # "openai>=1.65.1,<2.0.0",  
        # "packaging",  
        # "pip",  
        "psycopg2-binary==2.9.10",  
        # # "pymongo>=4.11.1,<5.0.0",  
        # "PyMySQL",  
        # "python-dotenv",  
        # # "redis>=5.2.1,<6.0.0",  
        "langchain_community==0.3.19",
        "requests==2.32.3",  
        "setuptools==76.0.0",
        "pymongo==4.11.2",
        "python-dotenv==1.0.1",
        
        #"snowflake-connector-python>=3.13.2,<4.0.0",  
        "SQLAlchemy==2.0.38",  
        # "trino>=0.333.0,<1.0.0",  
    ],


    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)
