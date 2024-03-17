import pandas as pd
import boto3
import io
import datetime

s3_client = boto3.client('s3')
sns_client = boto3.client('sns')
sns_arn='arn:aws:sns:us-west-1:709114567321:doordash_delivery_notification'
target_s3='doordash-target-zon'

def lambda_handler(event, context):

    print(event)

    try:
        #Getting bucket name
        bucket  = event['Records'][0]['s3']['bucket']['name']
        print(bucket)
        #Getting s3 filename
        s3_file = event['Records'][0]['s3']['object']['key'] 
        print(s3_file)
        #Reading the s3 file using bucket and key
        resp = s3_client.get_object(Bucket=bucket, Key=s3_file)        
        #Reading the file content as json
        df = pd.read_csv(resp['Body'])       
        #Filetering the records with status as delivered
        result_df=df['status'] = 'delivered'
        #writing the filetered df as json file into s3 bucket
        print(result_df)
        # json_buffer = io.StringIO()
        # result_df.to_json(json_buffer)        
        # tgt_bucket = s3_client.Bucket('doordash-target-zon')
        # destination = "output_" + str(datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')) + '.json'
        # tgt_bucket.put_object(Key=destination, Body=json_buffer.getvalue())
        #sending success alert mail
        message = "DoorDash {} file has been processed successfully !!".format("s3://"+bucket+"/"+s3_file)
        success_alert = sns_client.publish(Subject="SUCCESS - Daily data processing",TargetArn=sns_arn,Message=message,MessageStructure='text')

    except Exception as err:
         
         print(err)
         #sending failure alert mail
         message = "DoorDash {} file process is failed !!".format("s3://"+bucket+"/"+s3_file)
         failure_alert = sns_client.publish(Subject="FAILED - Daily data processing",TargetArn=sns_arn,Message=message,MessageStructure='text')
