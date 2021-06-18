# Export data from Vertica table to S3

Awesome stuff if you have IAM role setup. If so, we can ignore setting session
parameters.


```sql
ALTER SESSION SET UDPARAMETER FOR awslib aws_id='AWS-ACCESS-KEY-ID';
ALTER SESSION SET UDPARAMETER FOR awslib aws_secret='AWS-SECRET-ACCESS-KEY';
ALTER SESSION SET UDPARAMETER FOR awslib aws_region='AWS-REGION';

SELECT S3EXPORT (
    *
    USING PARAMETERS
        url='s3://path/to/target/folder/',
        chunksize='CHUNK_SIZE'
    ) OVER()
FROM V_SCHEMA_NAME.V_TABLE_NAME;
```
