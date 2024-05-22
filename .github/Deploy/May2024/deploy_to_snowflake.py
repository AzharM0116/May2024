import os
import snowflake.connector

# Connect to Snowflake
conn = snowflake.connector.connect(
    user=os.getenv('SNOWFLAKE_USER'),
    password=os.getenv('SNOWFLAKE_PASSWORD'),
    account=os.getenv('SNOWFLAKE_ACCOUNT'),
    warehouse=os.getenv('SNOWFLAKE_WAREHOUSE'),
    database=os.getenv('SNOWFLAKE_DATABASE'),
    role=os.getenv('SNOWFLAKE_ROLE')
)

# Create a cursor object
cur = conn.cursor()

# Get list of SQL files in the deploy directory
sql_files = [f for f in os.listdir('deploy') if f.endswith('.sql')]

# Execute each SQL file
for sql_file in sql_files:
    with open(os.path.join('deploy', sql_file), 'r') as file:
        sql_commands = file.read()
    # Execute the SQL commands in the file
    for command in sql_commands.split(';'):
        if command.strip():
            cur.execute(command)

# Close the cursor and connection
cur.close()
conn.close()
