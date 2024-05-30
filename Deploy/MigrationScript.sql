-- Setting the Context correct for installation 
use database dev_db;
use schema dev_db_schema;
use role accountadmin;

-- Migration script to execute table1.sql and table2.sql in order

-- Execute table1.sql
!source table1.sql;

-- Execute table2.sql
!source table2.sql;