
HOST = "127.0.0.1"
PORT = "5432"
DATABASE = "docxplorer"
USER = "postgres"
PASSWORD = "password"


INSERT_QUERY = "insert into document_data (document_id, document_name, document_size, uploaded_date) values (%s, %s, %s, %s)"
DELETE_QUERY = "delete from document_data where document_id = %s"
SELECT_QUERY = "select * from document_data"