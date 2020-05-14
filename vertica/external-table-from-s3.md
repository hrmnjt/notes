# Create external table from S3 source

Awesome stuff if you have IAM role setup. If so, we can ignore setting session
parameters.

```sql
ALTER SESSION SET AWSAuth='AWS-ACCESS-KEY-ID:AWS-SECRET-ACCESS-KEY';
ALTER SESSION SET AWSRegion='AWS-REGION';

DROP TABLE IF EXISTS V_SCHEMA_NAME.V_TABLE_NAME;

CREATE EXTERNAL TABLE V_SCHEMA_NAME.V_TABLE_NAME
(
  col1 varchar(1000),
  col2 varchar(1000),
  col3 date,
  col4 numeric(19, 5),
  sc_timestamp timestamp,
  sc_processing_date timestamp,
  sc_file_name varchar(2047)
) AS
COPY
FROM 's3://path/to/target/folder/file.gz' GZIP
DELIMITER '|'
REJECTED DATA AS TABLE V_SCHEMA_NAME.REJECTIONS_V_TABLE_NAME;
```
