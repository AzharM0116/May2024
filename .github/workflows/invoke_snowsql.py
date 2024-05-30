import os
import subprocess

# Environment variables for Snowflake credentials
SNOWFLAKE_USER = os.getenv('SNOWFLAKE_USER')
SNOWFLAKE_PASSWORD = os.getenv('SNOWFLAKE_PASSWORD')
SNOWFLAKE_ACCOUNT = os.getenv('SNOWFLAKE_ACCOUNT')
SNOWFLAKE_DATABASE = os.getenv('SNOWFLAKE_DATABASE')
SNOWFLAKE_WAREHOUSE = os.getenv('SNOWFLAKE_WAREHOUSE')
SNOWFLAKE_ROLE = os.getenv('SNOWFLAKE_ROLE')

# Path to the Deploy directory
deploy_dir = 'Deploy'

def execute_snowsql(file_path):
    command = [
        'snowsql',
        '-a', SNOWFLAKE_ACCOUNT,
        '-u', SNOWFLAKE_USER,
        '-w', SNOWFLAKE_WAREHOUSE,
        '-d', SNOWFLAKE_DATABASE,
        '-r', SNOWFLAKE_ROLE,
        '-f', file_path,
        '--variable', f'SNOWFLAKE_PASSWORD={SNOWFLAKE_PASSWORD}'
    ]
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error executing {file_path}: {result.stderr}")
    else:
        print(f"Successfully executed {file_path}: {result.stdout}")

if os.path.exists(deploy_dir) and os.path.isdir(deploy_dir):
    sql_files = [f for f in os.listdir(deploy_dir) if f.endswith('.sql')]
    for sql_file in sql_files:
        file_path = os.path.join(deploy_dir, sql_file)
        execute_snowsql(file_path)
else:
    print(f"Directory {deploy_dir} does not exist.")
