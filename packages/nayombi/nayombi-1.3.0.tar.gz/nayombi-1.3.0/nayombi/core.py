# core.py
import json
from .models import initialize_policy_model, initialize_execution_model
from .database import initialize_database, initialize_sql_chain
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
import os
from langchain_mistralai.chat_models import ChatMistralAI
from dotenv import load_dotenv  
from langchain_openai import ChatOpenAI
load_dotenv() 
def process_query(user_role, user_id, query, system, language):
    """
    Process the query based on the user's role and system policies.
    Args:
        user_role: Role of the user (e.g., 'admin', 'general_user').
        user_id: ID of the user.
        query: User's query.
        system: The initialized system with models and database.
    Returns:
        JSON response with query processing results.
    """
    policy_model = system["policy_model"]
    execution_model = system["execution_model"]
    sql_chain = system["sql_chain"]
    db = system["db"]
    from langchain.prompts import ChatPromptTemplate
    from langchain.chains import LLMChain

    if language == "kinyarwanda":
        # Initialize the LLM model
        structured_llm = ChatMistralAI(
            temperature=0,
            max_retries=2,
            response_format = {
            "type": "json_object",
      },
            max_tokens=100,
            api_key=os.environ["MISTRAL_API_KEY2"]
        )
    
        # Define the prompt template
        prompt_template = ChatPromptTemplate.from_template(
            "Translate the following Kinyarwanda query into English, always, remember , whenever you see umubare ndanga,  umubare wumuntu muri databesi, or something similar, it means id of something being said: {input}"
        )
    
        # Create a chain with the model and the prompt
        translation_chain = LLMChain(llm=structured_llm, prompt=prompt_template)
    
        # Execute the chain with the user query
        translation_result = translation_chain.invoke(input=query)
    
        # Update the query with the translated content
        query = translation_result
        #print(f"{query} , is translated")

        
        
    
    # Enforce system policy using the policy model
    structured_llm = policy_model.with_structured_output(
    method="json_mode",
    include_raw=False
    )   

    system_policy = """
    You are a strict pre-screener, tasked with ensuring that only authorized users can access specific data in a database.
    Users have different roles, and each role has access to different data:
    - 'admin' and 'manager' can access all data.
    - 'general_user' can only access their own data, filtered by their user_id.
    
    If a user tries to access data they are not authorized to view, return an explicit error message stating that their access is restricted. Do **not** provide any SQL code or further explanation, just the error message.
    
    - For 'admin' or 'manager' roles, allow the query to proceed and return the result as requested.
    - For 'general_user' role, ensure the query is limited to their own data (filtered by their user_id). If the query attempts to access data outside of this scope, immediately return an error indicating that they are not authorized to access that data.
    
    For example, if a general user tries to query all users in the database (e.g., "How many users are there?"), the response should be: 
    'Unauthorized: You are not allowed to access this data.' 
    
    The query should be rejected with no further processing. Only allow queries that are related to the general user's own data. If a general user tries to perform a query that is not related to them, do not rewrite the query or try to make it contextually relevant. Simply reject the query as unauthorized.
    
    
    The query or question should be outputted exactly as received if it's well-formed and falls within the access policy. If there are grammar errors or unclear wording, rewrite it in a grammatically correct manner, but ensure that the user's role limitations are always enforced.
    attention, do not make things up , no fabricating.
    User role: {user_role}, User ID: {user_id}.
    For queries that are within the user's scope, return the output as usual, but include the user_id in the response to indicate which user's data the query is related to if teh user is a general_user, for admin no need because, he can access everything.
    return in json format like this, please, make it eal json stritructures, not thsi way you are seeing , here but real json , and which , can be easily extracted
    remember:the JSON object must be str, bytes or bytearray, not dict or list.the wrapper should , be content, then equal(=)
    (
     
        "user_role": "user_role",  
        "user_id": "user_id",  
        "is_admin": "is_admin",  
        "is_in_scopeoftheuser": "is_in_scopeoftheuser",  
        "output": "output"  
    , I think , you know True or False
        
    )., 
    
    """
    
    messages = [
        ("system", system_policy),
        ("human", "{query}"),
    ]
    
    # Create the prompt by filling in the partials
    prompt = ChatPromptTemplate.from_messages(messages)
    formatted_prompt = prompt.format(user_role=user_role,
                                     user_id=user_id,
                                     query=query,   
                                    )
    policy_response = structured_llm.invoke(formatted_prompt)
    #print(policy_response)

    user_role = policy_response['user_role'] if 'user_role' in policy_response else None  
    user_id = policy_response['user_id'] if 'user_id' in policy_response else None  
    is_in_scope = policy_response['is_in_scopeoftheuser'] if 'is_in_scopeoftheuser' in policy_response else None  
    output = policy_response['output'] if 'output' in policy_response else None  
    is_admin = policy_response['is_admin'] if 'is_admin' in policy_response else None  
    # Execute the query using the SQL chain
    if not is_in_scope:
        #print("Unauthorized1: You are not allowed to access this data.")
        return {"status": "error", "message": "Unauthorized: You are not allowed to access this data."}
    if is_admin:
        #print("This is an admin, so they can access everything.")
        question=f"{output}."
        try:
            response = sql_chain.invoke({"question": question})
            #print(f"{response}\n======================================================")
            if not "SQLQuery:" in response:
                print("SQL query not found in the response.")
                return {"status": "error", "message": "SQL query not found in the response."}
            sql_query = response.split("SQLQuery:")[-1].strip()
            result = db.run(sql_query)
            return {"status": "success", "data": result}
        except Exception as e:
                return {"status": "error", "message": str(e)}
    else:
        #print("This is a general user, so they can only access their own data.")
        question=f"{output}, the asking user id, is {user_id}."
        try:
            response = sql_chain.invoke({"question": question})
            #print(f"{response}\n======================================================")
            if "SQLQuery:" in response:
                print("SQL query not found in the response.")
                return {"status": "error", "message": "SQL query not found in the response."}
            sql_query = response.split("SQLQuery:")[-1].strip()
            result = db.run(sql_query)
            return {"status": "success", "data": result}
        except Exception as e:
            return {"status": "error", "message": str(e)}

