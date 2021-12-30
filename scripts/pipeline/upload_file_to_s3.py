import os.path
import sys

import boto3
import yaml


def main():
    # read config values from the yml into a dictionary
    with open('scripts/pipeline/upload_file_to_s3.yml', 'r') as config_file:
        config_values = yaml.safe_load(config_file)

    # parse the config values into program variables
    bucket_name = config_values['s3']['bucket_name']
    object_path = config_values['s3']['obj_destination_path']
    source_config = config_values['data_warehouse']['source_directory']
    # get the abs path of the source directory relative to the current directory
    source_directory = os.path.abspath(os.path.dirname(source_config))

    # create the s3 resource object
    s3 = boto3.resource(
        service_name='s3',
        region_name='us-east-1',
        aws_access_key_id=sys.argv[1],
        aws_secret_access_key=sys.argv[2]
    )

    # get the bucket from s3 and the objects in the bucket within the object path
    bucket = s3.Bucket(bucket_name)
    existing_objects = bucket.objects.filter(Prefix=object_path)

    # for each file in the source dir check to see if it exists in the s3 bucket and upload it if not
    for local_file in os.listdir(source_directory):
        put_path = object_path + local_file

        if any([obj.key == put_path for obj in existing_objects]):
            print(f'Existing file: {local_file} is already in the s3 bucket path: {object_path}.')
        else:
            # create the new s3 object and put it in s3
            new_s3_object = s3.Object(bucket_name, object_path + local_file)
            new_s3_object.put()
            print(f'Uploaded: {local_file} to s3 in the bucket path: {object_path}.')


main()
