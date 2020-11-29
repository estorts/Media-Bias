#!/usr/bin/env bash

rm response.json
rm API.zip

cd package

#update zip file
zip -r API.zip ./*

mv API.zip /home/sagemaker-user/Media-Bias/API/

cd ..

zip -g API.zip get_request.py


#send update to s3
aws s3 cp API.zip s3://media-bais/API.zip

aws lambda update-function-code \
    --function-name  Media-Bias-GET-model-results \
    --s3-bucket media-bais \
    --s3-key API.zip
    
aws lambda invoke \
    --function-name Media-Bias-GET-model-results \
    response.json