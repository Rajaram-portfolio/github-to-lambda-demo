import pandas as pd
import boto3
from io import StringIO


s3_client = boto3.client('s3')
sns_client = boto3.client('sns')
sns_arn='arn:aws:sns:us-west-1:709114567321:doordash_delivery_notification'
target_s3='doordash-target-zon'

def lambda_handler(event, context):

    #print(event)

    try:
        #Getting bucket name
        bucket  = event['Records'][0]['s3']['bucket']['name']
        #print(bucket)
        
        #Getting s3 filename
        s3_file = event['Records'][0]['s3']['object']['key'] 
        #print(s3_file)
        
        #Reading the s3 file using bucket and key
        resp = s3_client.get_object(Bucket=bucket, Key=s3_file) 
        
        #Reading the file content as json
        file_content = resp["Body"].read().decode('utf-8')
        
        # Read the content using pandas
        df = pd.read_json(StringIO(file_content),lines=True)
        #print(df)
        
        #Filetering the records with status as delivered
        result_df=df[df['status'] == 'delivered']
        print(result_df)
        #writing the filetered df as json file into s3 bucket
        df1=result_df.to_json()
        target_file = s3_file[:16]
        s3_client.put_object(Body=df1, Bucket=target_s3,Key=target_file.json)
        #sending success alert mail
        message = "DoorDash {} file has been processed successfully !!".format("s3://"+bucket+"/"+s3_file)
        success_alert = sns_client.publish(Subject="SUCCESS - Daily data processing",TargetArn=sns_arn,Message=message,MessageStructure='text')

    except Exception as err:
         
         print(err)
         #sending failure alert mail
         message = "DoorDash {} file process is failed !!".format("s3://"+bucket+"/"+s3_file)
         failure_alert = sns_client.publish(Subject="FAILED - Daily data processing",TargetArn=sns_arn,Message=message,MessageStructure='text')
