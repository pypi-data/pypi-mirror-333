import boto3
from django.conf import settings
from botocore.exceptions import ClientError

class SNSNotification:
    def __init__(self):
        """AWS SNS 클라이언트 생성"""
        self.client = boto3.client(
            'sns',
            region_name='us-east-1'  # 사용 중인 리전으로 변경
        )
        self.topic_arn = settings.SNS_TOPIC_ARN

    def send_notification(self, message, subject="Work Session Update"):
        """SNS 알림을 전송하는 함수"""
        try:
            response = self.client.publish(
                TopicArn=self.topic_arn,
                Subject=subject,
                Message=message
            )
            print(f"✅ SNS Notification Sent: {response}")
            return response
        except ClientError as e:
            print(f"❌ Error sending SNS message: {e}")
            return None
