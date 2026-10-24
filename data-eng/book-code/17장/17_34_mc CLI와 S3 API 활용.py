# s3_demo.py — endpoint_url과 키만 바꾸면 AWS S3 에서도 그대로 돕니다
import boto3

s3 = boto3.client(
    's3',
    endpoint_url='http://localhost:9000',
    aws_access_key_id='minioadmin',
    aws_secret_access_key='minioadmin',
)

# 버킷 목록
print('버킷:', [b['Name'] for b in s3.list_buckets()['Buckets']])

# 오브젝트 목록 (접두사로 거르기)
resp = s3.list_objects_v2(Bucket='raw', Prefix='demo/')
for obj in resp.get('Contents', []):
    print(f"  {obj['Key']}  ({obj['Size']} bytes)")

# 올리기
s3.put_object(Bucket='raw', Key='from-python.txt', Body=b'written by boto3')

# 읽기
body = s3.get_object(Bucket='raw', Key='from-python.txt')['Body'].read()
print('읽은 내용:', body.decode())
