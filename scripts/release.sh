aws_access_key=$1
aws_access_secret=$2

# Install required dependencies for Python script.
pip3 install boto3
pip3 install pyyml

# run upload script
python3 scripts/pipeline/upload_file_to_s3.py
