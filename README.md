# AWS-API-S3Proxy #

An API created with Amazon API gateway as an Amazon S3 Proxy.

### API

Documentation: [API](API.md) (generated with swagger2markdown)

### Components

```
 _____________     ____     
| API Gateway |-->| S3 |
|_____________|   |____|
```

1. A S3 bucket acts as the backend storage.
1. A API Gateway as S3 proxy.
1. API Auth: AWS_IAM

### Create Infrastructure

1. Edit some files first

    1. Edit `api/DataServiceAPI_swagger.json` to specify your AWS account ID and domain.
    1. Edit  `deploy/aws.ini` to specify your API Gateway ID and bucket names.

1. Use `aws\cf_templates\DataService-IAM.template` to create IAM roles and policies.
1. Use `aws\cf_templates\DataService-S3.template` to create S3 buckets (stage and prod) accessible by ApiGateway.
1. Use `aws\deploy_and_test_api_methods.bat|sh` to reimport the API Swagger file to AWS and run method-level tests.
1. Use `aws\deploy_and_test_api_stage.bat|sh` to deploy a stage of the DataService API and run stage-level tests.


### CI and Deployment

#### Running method-level tests

Set environment variables:

- aws_access_key_id=(yours)
- aws_secret_access_key=(yours)

Linux

```bash
cd aws/deploy
./deploy_and_test_api_methods.sh
```

Windows
```cmd
cd aws\deploy
deploy_and_test_api_methods.bat
```

#### Running stage-level tests

Set environment variables (see above).

Linux

```bash
cd aws/deploy
./deploy_and_test_api_stage.sh {stage_name}
```

Windows
```cmd
cd aws\deploy
deploy_and_test_api_stage.bat {stage_name}
```

#### To generate API.md

```cmd
pip install swagger2markdown
swagger2markdown -i api\DataServiceAPI_swagger.json -o API.md
```

#### References

1. [Integrating API with AWS services S3](http://docs.aws.amazon.com/apigateway/latest/developerguide/integrating-api-with-aws-services-s3.html)
1. [S3 Bucket Restriction](http://docs.aws.amazon.com/AmazonS3/latest/dev/BucketRestrictions.html)
1. [S3 Transfer Acceleration](http://docs.aws.amazon.com/AmazonS3/latest/dev/transfer-acceleration.html)

