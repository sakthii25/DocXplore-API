import os 

HOST = "pg-docxplorer-docxplorer.k.aivencloud.com"
PORT = "24116"
DATABASE = "docxplorer"
USER = os.getenv("PSQL_USER")
PASSWORD = os.getenv("PSQL_PASSWORD") 

LOCAL_HOST = "localhost"
LOCAL_PORT = "5432" 
LOCAL_USER = "postgres" 
LOCAL_PASSWORD = "password"

#document_data
INSERT_QUERY = "insert into document_data (document_id, user_id, document_name, document_size, uploaded_time) values (%s, %s, %s, %s, %s)"
DELETE_QUERY = "delete from document_data where document_id = %s"
SELECT_QUERY = "select * from document_data where user_id = %s"

#user_data
INSERT_USER_QUERY = "insert into user_data (user_id, user_name, user_email, last_login) values (%s, %s, %s, %s)"
SELECT_USER_QUERY = "select * from user_data where user_email = %s"
UPDATE_USER_QUERY = "update user_data set last_login = %s where user_email = %s"

#collection_data 

INSERT_COLLECTION_QUERY = "insert into collection_data (user_id, collection_name, summary_collection_name) values(%s, %s, %s)"
SELECT_COLLECTION_QUERY = "select * from collection_data where user_id = %s"

#api_key 

INSERT_API_KEY_QUERY = "insert into api_key (api_key, user_id, created_at) values(%s, %s, %s)"
SELECT_API_KEY_QUERY = "select * from api_key where user_id = %s"
DELETE_API_KEY_QUERY = "delete from api_key where api_key = %s"