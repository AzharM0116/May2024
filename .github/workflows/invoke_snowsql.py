import os
import subprocess

# Environment variables for Snowflake credentials
SNOWFLAKE_USER = os.getenv('SNOWFLAKE_USER')
SNOWFLAKE_PASSWORD = os.getenv('SNOWFLAKE_PASSWORD')
SNOWFLAKE_ACCOUNT = os.getenv('SNOWFLAKE_ACCOUNT')
SNOWFLAKE_DATABASE = os.getenv('SNOWFLAKE_DATABASE')
SNOWFLAKE_WAREHOUSE = os.getenv('SNOWFLAKE_WAREHOUSE')
SNOWFLAKE_ROLE = os.getenv('SNOWFLAKE_ROLE')

# Path to the migration script file
migration_script_path = 'deploy/migrationscript.txt'
# Path to the codebase directory
codebase_dir = 'codebase'

def execute_snowsql(file_path):
    command = [
        'snowsql',
        '-a', SNOWFLAKE_ACCOUNT,
        '-u', SNOWFLAKE_USER,
        '-w', SNOWFLAKE_WAREHOUSE,
        '-d', SNOWFLAKE_DATABASE,
        '-r', SNOWFLAKE_ROLE,
        '-f', file_path
    ]
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error executing {file_path}: {result.stderr}")
    else:
        print(f"Successfully executed {file_path}: {result.stdout}")

def main():
    if os.path.exists(migration_script_path):
        with open(migration_script_path, 'r') as file:
            content = file.read()
        
        sql_files = content.split(';')
        
        for sql_file in sql_files:
            sql_file = sql_file.strip()  # Remove any leading/trailing whitespace
            if sql_file:
                file_path = os.path.join(codebase_dir, sql_file)
                if os.path.exists(file_path):
                    execute_snowsql(file_path)
                else:
                    print(f"SQL file {file_path} does not exist.")
    else:
        print(f"Migration script {migration_script_path} does not exist.")

if __name__ == "__main__":
    main()
