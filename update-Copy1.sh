#!/usr/bin/env bash

rm response.json
rm API-1.zip

cd package

#update zip file
zip -r API-1.zip ./*

mv API-1.zip /home/sagemaker-user/Media-Bias/API/

cd ..

zip -g API-1.zip convert_request.py


#send update to s3
aws s3 cp API-1.zip s3://media-bais/API-1.zip

aws lambda update-function-code \
    --function-name  Media-Bias-GET-Convert-to-Numbers \
    --s3-bucket media-bais \
    --s3-key API-1.zip
    
aws lambda invoke \
    --function-name Media-Bias-GET-Convert-to-Numbers \
    --payload { "body": { "text": "Hello World"  } } \
    response.json