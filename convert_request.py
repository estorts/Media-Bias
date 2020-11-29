import os
import boto3
import json
import joblib

    
def good_response(result):
    return {
        'statusCode': '200',
        'body': json.dumps(result),
        'headers': {
            'Content-Type': 'model result',
        },
    }

def bad_response(result):
    return {
        'statusCode': '400',
        'body': json.dumps(result),
        'headers': {
            'Content-Type': 'error',
        },
    }

def lambda_handler(event, context):
    print('Download Info')
    #try:
        #set working directory
    os.chdir('/tmp/')

        #download everything from s3
    s3 = boto3.client('s3')

    vect = 'media-bias-count-vectorizer.sav'

    s3.download_file('media-bais', vect, vect)
 
    #except:
        #return bad_response("Prep Failed")
    
    print('Import Info')
    #try:
    count_vectorizer = joblib.load(vect)

    print("Apply Text")
    
    body = event['body']
    text = json.loads(body)['text']

        #vectorize text
    X = count_vectorizer.transform(text)
    
    good_response(X)
    #except:
        #return bad_response("Model Failed")