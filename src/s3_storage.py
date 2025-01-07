class S3Storage:
    def __init__(self, aws_access_key, aws_secret_key, bucket_name):
        import boto3
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_key
        )
        self.bucket_name = bucket_name

    def upload_file(self, file_name, object_name=None):
        if object_name is None:
            object_name = file_name
        try:
            self.s3_client.upload_file(file_name, self.bucket_name, object_name)
            print(f"File {file_name} uploaded to {object_name} in bucket {self.bucket_name}.")
        except Exception as e:
            print(f"Failed to upload {file_name}: {e}")

    def list_files(self):
        try:
            response = self.s3_client.list_objects_v2(Bucket=self.bucket_name)
            files = [obj['Key'] for obj in response.get('Contents', [])]
            return files
        except Exception as e:
            print(f"Failed to list files in bucket {self.bucket_name}: {e}")
            return []