import os 

HOST = "pg-docxplorer-docxplorer.k.aivencloud.com"
PORT = "24116"
DATABASE = "docxplorer"
USER = os.getenv("PSQL_USER")
PASSWORD = os.getenv("PSQL_PASSWORD")


INSERT_QUERY = "insert into document_data (document_id, document_name, document_size, uploaded_date) values (%s, %s, %s, %s)"
DELETE_QUERY = "delete from document_data where document_id = %s"
SELECT_QUERY = "select * from document_data"