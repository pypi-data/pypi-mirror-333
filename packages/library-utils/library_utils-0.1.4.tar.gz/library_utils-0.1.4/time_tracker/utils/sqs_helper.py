import boto3
from botocore.exceptions import ClientError
from django.conf import settings

# SQS 클라이언트 생성
sqs = boto3.client('sqs', region_name='us-east-1')

# SQS 큐에 메시지 보내기
def send_message_to_sqs(message_body):
    try:
        response = sqs.send_message(
            QueueUrl=settings.SQS_QUEUE_URL,
            MessageBody=message_body
        )
        print(f"Message sent to SQS: {response['MessageId']}")
    except ClientError as e:
        print(f"Error sending message to SQS: {e}")

# SQS 큐에서 메시지 받기
def receive_message_from_sqs():
    try:
        # 메시지 수신
        response = sqs.receive_message(
            QueueUrl=settings.SQS_QUEUE_URL,
            MaxNumberOfMessages=1,  # 최대 1개 메시지 받기
            WaitTimeSeconds=10  # Long Polling (10초 대기)
        )

        messages = response.get('Messages', [])
        if not messages:
            print("No messages in the queue.")
            return None

        # 첫 번째 메시지 가져오기
        message = messages[0]
        receipt_handle = message['ReceiptHandle']

        # 메시지 삭제 (받은 메시지는 SQS에서 삭제해야 함)
        sqs.delete_message(
            QueueUrl=settings.SQS_QUEUE_URL,
            ReceiptHandle=receipt_handle
        )

        print(f"Message received from SQS: {message['Body']}")
        return message['Body']
    
    except ClientError as e:
        print(f"Error receiving message from SQS: {e}")
        return None
