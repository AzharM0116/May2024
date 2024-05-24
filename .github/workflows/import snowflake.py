import snowflake.connector
import os

# Replace with your Snowflake connection details
conn = snowflake.connector.connect(
    user=os.getenv('SNOWFLAKE_USER'),
    password=os.getenv('SNOWFLAKE_PASSWORD'),
    account=os.getenv('SNOWFLAKE_ACCOUNT'),
    warehouse=os.getenv('SNOWFLAKE_WAREHOUSE'),
    database=os.getenv('SNOWFLAKE_DATABASE'),
    role=os.getenv('SNOWFLAKE_ROLE')
)

def get_ddl_for_objects(conn, database):
    cursor = conn.cursor()

    # Query to get all schemas in the database
    cursor.execute(f"SHOW SCHEMAS IN DATABASE {database}")
    schemas = cursor.fetchall()

    # Get DDL for all objects in each schema
    for schema in schemas:
        schema_name = schema[1]  # Assuming the schema name is in the second column

        # Query to get all object types and their names in the schema
        cursor.execute(f"""
            SELECT 
                'TABLE' AS OBJECT_TYPE, 
                TABLE_NAME AS OBJECT_NAME 
            FROM INFORMATION_SCHEMA.TABLES 
            WHERE TABLE_SCHEMA = '{schema_name}' 
            AND TABLE_CATALOG = '{database}'
            UNION ALL
            SELECT 
                'VIEW' AS OBJECT_TYPE, 
                TABLE_NAME AS OBJECT_NAME 
            FROM INFORMATION_SCHEMA.VIEWS 
            WHERE TABLE_SCHEMA = '{schema_name}' 
            AND TABLE_CATALOG = '{database}'
            UNION ALL
            SELECT 
                'PROCEDURE' AS OBJECT_TYPE, 
                PROCEDURE_NAME AS OBJECT_NAME 
            FROM INFORMATION_SCHEMA.PROCEDURES 
            WHERE PROCEDURE_SCHEMA = '{schema_name}' 
            AND PROCEDURE_CATALOG = '{database}'
            UNION ALL
            SELECT 
                'FUNCTION' AS OBJECT_TYPE, 
                FUNCTION_NAME AS OBJECT_NAME 
            FROM INFORMATION_SCHEMA.FUNCTIONS 
            WHERE FUNCTION_SCHEMA = '{schema_name}' 
            AND FUNCTION_CATALOG = '{database}'
            UNION ALL
            SELECT 
                'SEQUENCE' AS OBJECT_TYPE, 
                SEQUENCE_NAME AS OBJECT_NAME 
            FROM INFORMATION_SCHEMA.SEQUENCES 
            WHERE SEQUENCE_SCHEMA = '{schema_name}' 
            AND SEQUENCE_CATALOG = '{database}'
        """)

        objects = cursor.fetchall()

        for obj in objects:
            object_type = obj[0]
            object_name = obj[1]
            fully_qualified_name = f"{database}.{schema_name}.{object_name}"
            cursor.execute(f"SELECT GET_DDL('{object_type}', '{fully_qualified_name}')")
            ddl = cursor.fetchone()[0]

            file_name = f"{fully_qualified_name}.sql"
            with open(file_name, 'w') as file:
                file.write(ddl)
            print(f"Saved DDL for {fully_qualified_name} to {file_name}")

get_ddl_for_objects(conn, 'YOUR_DATABASE')

# Close the connection
conn.close()
