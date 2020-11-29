import os
import boto3
import json
import joblib


def decoder(number):
    if number == 0:
        return 'left'
    elif number == 1:
        return 'left-center'
    elif number == 2:
        return 'center'
    elif number == 3:
        return 'right'
    elif number == 4:
        return 'right-center'
    else:
        return np.nan
    
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

    mod = 'media-bias-model.sav'

    s3.download_file('media-bais', mod, mod)
        
    #except:
        #return bad_response("Prep Failed")
    
    print('Import Info')
    #try:
    model = joblib.load(mod)
    
    print("Apply Text")
    
    body = event['body']
    X = json.loads(body)['text']

    #except:
        #return bad_response("Data Clean Failed")
    
    print('Apply Model')
    #try:
        # Use the loaded model to make predictions
    pred = model.predict(X)

        #convert the numberic categories back to words
    pred_word = decoder(pred)

        #build json response
    return good_response(pred_word)
    #except:
        #return bad_response("Model Failed")