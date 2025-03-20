import boto3
import time
from botocore.exceptions import ClientError
import uuid
from django.http import HttpResponse

# CloudWatch 클라이언트 생성
client = boto3.client('logs', region_name='us-east-1')  # 해당 리전 설정

log_group_name = 'WorkSessionLogs'
log_stream_name = 'WorkSessionStream'

def create_log_group_and_stream():
    try:
        response = client.describe_log_groups(logGroupNamePrefix=log_group_name)
        if not any(group['logGroupName'] == log_group_name for group in response.get('logGroups', [])):
            client.create_log_group(logGroupName=log_group_name)
            print(f"Created log group: {log_group_name}")
    except ClientError as e:
        print(f"Error creating log group: {e}")

    try:
        response = client.describe_log_streams(
            logGroupName=log_group_name,
            logStreamNamePrefix=log_stream_name
        )
        if not any(stream['logStreamName'] == log_stream_name for stream in response.get('logStreams', [])):
            client.create_log_stream(
                logGroupName=log_group_name,
                logStreamName=log_stream_name
            )
            print(f"Created log stream: {log_stream_name}")
    except ClientError as e:
        print(f"Error creating log stream: {e}")

def write_to_cloudwatch_log(message):
    timestamp = int(round(time.time() * 1000))  # 밀리초 단위의 타임스탬프 생성

    try:
        response = client.describe_log_streams(
            logGroupName=log_group_name,
            logStreamNamePrefix=log_stream_name
        )

        # 스트림이 없으면 생성
        if not response['logStreams']:
            client.create_log_stream(
                logGroupName=log_group_name,
                logStreamName=log_stream_name
            )

        # 로그 기록
        response = client.put_log_events(
            logGroupName=log_group_name,
            logStreamName=log_stream_name,
            logEvents=[
                {
                    'timestamp': timestamp,
                    'message': message
                }
            ]
        )
        print(f"Log successfully written to CloudWatch: {message}")
    
    except ClientError as e:
        print(f"Error writing log to CloudWatch: {e}")

# 서버 시작 시 한 번만 로그 그룹과 스트림을 생성
create_log_group_and_stream()