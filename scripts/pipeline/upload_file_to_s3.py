import os.path
import boto3
import sys
import yaml


def main():
    # read config values from the yml into a dictionary
    with open('upload_file_to_s3.yml', 'r') as config_file:
        config_values = yaml.safe_load(config_file)

    # parse the config values into program variables
    bucket_name = config_values['s3']['bucket_name']
    object_path = config_values['s3']['obj_destination_path']
    file_abs_path = sys.argv[1]

    print(f'bucket_name: {bucket_name}')
    print(f'object_name: {object_path}')
    print(f'file_abs_path: {file_abs_path}')

    file_name = os.path.basename(file_abs_path)

    # setup the s3 resource
    s3 = boto3.resource(
        service_name='s3',
        region_name='us-east-1'
    )

    # get the bucket from s3
    bucket = s3.Bucket(bucket_name)
    # get the objects in the bucket within the object path
    objects = bucket.objects.filter(Prefix=object_path)
    for obj in objects:
        # if the file is not in the bucket already, put the file in s3
        if obj.key == object_path + file_name:
            print(f'File {file_name} already exists in the s3 bucket path {object_path}.')
        else:
            new_s3_object = s3.Object(bucket_name, object_path + file_name)
            # new_s3_object.put()
            print(f'Uploaded {file_name} to s3.')

    print('Upload complete.')


main()
