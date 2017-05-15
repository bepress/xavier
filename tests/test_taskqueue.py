from unittest.mock import patch, MagicMock
import jsonpickle

from xavier.taskqueue import TaskQueue
from xavier.aws.sns import publish_sns_message, handle_sns_message


funcy_called = 0


def test_background_queue():
    publish_event = MagicMock()
    publish_event.return_value = 'aaa'

    task_queue = TaskQueue(publish_event)

    @task_queue.task()
    def funcy():
        global funcy_called
        funcy_called += 1
        return "blah"

    assert funcy() == "blah"

    assert funcy.delay() is True

    event = jsonpickle.dumps((funcy.path, (), {}))

    publish_event.assert_called_once_with(event)

    task_queue.process_event(event)
    assert funcy_called == 2


def test_schedule_queue():
    publish_event = MagicMock()
    publish_event.return_value = 'aaa'

    task_queue = TaskQueue(publish_event)

    @task_queue.task(schedules=['bbb'])
    def funcy():
        return "blah"

    task_queue.process_schedule('bbb')
    event = jsonpickle.dumps((funcy.path, (), {}))

    publish_event.assert_called_once_with(event)


def test_sns_background_queue():

    with patch('xavier.aws.sns.send_sns_message') as mock_send_sns_message:
        mock_send_sns_message.return_value = {"MessageId": "1234"}
        publish_event = publish_sns_message("sns:topic")
        task_queue = TaskQueue(publish_event)

        @task_queue.task(schedules=['bbb'])
        def funcy():
            return "Blah"

        funcy.delay()
        event = jsonpickle.dumps((funcy.path, (), {}))
        mock_send_sns_message.assert_called_once_with(
            Message=event,
            TopicArn="sns:topic",
        )

        mock_background_func = MagicMock()
        mock_background_func.__name__ = "background_func"
        mock_background_func.__module__ = "testing"
        mock_background_func.return_value = "awesome"
        composed_mock = task_queue.task()(mock_background_func)

        event = jsonpickle.dumps((composed_mock.path, (), {}))
        sns_consumer = handle_sns_message(task_queue.process_event)
        sns_consumer({
            "Records": [{
                'Sns': {
                    'Message': event
                }
            }]
        }, {})

        mock_background_func.assert_called_once_with()
