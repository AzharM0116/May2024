-- Setting the Context correct for installation 
use database dev_db;
use schema dev_db_schema;
use role accountadmin;

-- Migration script to execute table1.sql and table2.sql in order

-- Execute table1.sql
table1.sql;

-- Execute table2.sql
table2.sql;

-- changed this to be called from snowsql directly only requirement is to make sure that this file should be copied to deploy folder. we will configure this later 
-- for now move this files manually to deploy folder so that migrationscript.sql should point to this files 