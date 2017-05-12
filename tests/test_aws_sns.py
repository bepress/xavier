import pytest
from unittest.mock import patch, MagicMock

from xavier.aws.sns import publish_sns_message, handle_sns_message


def test_publish_sns_event():

    TEST_ARN = 'arn:abc'
    TEST_MESSAGE = "message"
    with patch('xavier.aws.sns.send_sns_message') as mock_send_sns_message:
        mock_send_sns_message.return_value = {"MessageId": "1234"}

        message_publisher = publish_sns_message(TEST_ARN)

        message_publisher(TEST_MESSAGE)

        mock_send_sns_message.assert_called_once_with(TopicArn=TEST_ARN, Message=TEST_MESSAGE)

    with patch('xavier.aws.sns.send_sns_message') as mock_send_sns_message:
        mock_send_sns_message.return_value = None

        message_publisher = publish_sns_message(TEST_ARN)
        with pytest.raises(Exception):
            message_publisher(TEST_MESSAGE)

        mock_send_sns_message.assert_called_once_with(TopicArn=TEST_ARN, Message=TEST_MESSAGE)


def test_handle_sns_message():
    responder = MagicMock()
    responder.return_value = True

    message_consumer = handle_sns_message(responder)

    message_consumer({
        "Records": [{
            'Sns': {
                'Message': "message"
            }
        }]
    })

    responder.assert_called_once_with("message")
