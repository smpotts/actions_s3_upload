# Gitlab CI Demo

## Overview
This project leverages the GitHub Actions functionality and uploads files from the local 'uploads' folder to an AWS S3 bucket. It iterates through the objects in the local 'uploads' folder, checks them against the objects in the destination bucket, and uploads the files that have not been added yet to S3. 

## Initial Setup and Config 
The first step is adding the IAM user credentials as entries to the GitHub Actions Secrets for the repository. Create one called "AWS_ACCESS_KEY" and another called "AWS_ACCESS_SECRET" and put the corresponding credentials in the secrets.

The configuration for the project are in [upload_file_to_s3.yml](scripts/pipeline/upload_file_to_s3.yml). The yaml file currently has two sections: s3, for the configuration values related to the s3 aspects of the project and local, for local configs. If you want to change the S3 bucket and destination folder for where the files will be uploaded in s3, do so under "bucket_name" and "upload_destination". The local section only has one config value for now which is just pointing to where the files to upload are located.

At the moment, the project is setup to upload all the files in the 'uploads' folder to S3, but this can be adapted in the [s3release.yml](.github/workflows/s3release.yml) file. The program can scan multiple directories by adding them to the 'paths' section of the s3release.yml file, or it can be modified to only add specific file types.

## Testing Locally
To test this locally, I find the best thing to do is to copy line in the release.sh file that runs the upload script:
```
python3 scripts/pipeline/upload_file_to_s3.py "$aws_access_key" "$aws_access_secret"
```
If you need to debug the upload script, make sure to modify the path to the config file in "upload_file_to_s3.py" to use the relative path: '../../scripts/pipeline/upload_file_to_s3.yml'.
