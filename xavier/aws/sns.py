import logging

import boto3

logger = logging.getLogger(__name__)

SNS_CLIENT = None


def get_client():
    global SNS_CLIENT
    if not SNS_CLIENT:
        SNS_CLIENT = boto3.client('sns')

    return SNS_CLIENT


def send_sns_message(TopicArn=None, Message=None):
    sns_client = get_client()
    return sns_client.publish(
        TopicArn=TopicArn,
        Message=Message,
    )


def publish_sns_message(topic):
    def _send(event):
        response = send_sns_message(
            TopicArn=topic,
            Message=event,
        )

        if 'MessageId' not in response:
            raise Exception("Failed to send message topic: {} event: {}".format(topic, event))

        logger.info("Sent message topic: %s message_id: %s message: %s", topic, response['MessageId'], event)

    return _send


def handle_sns_message(responder):

    def _recieve(sns_event, context):
        logger.info("Recieved an sns event: %s", sns_event)
        for record in sns_event.get('Records', []):
            sns = record.get('Sns', {})
            message = sns.get('Message')
            if not message:
                raise Exception("Got sns event without a message")

            responder(message)

    return _recieve
