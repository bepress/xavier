from mock import MagicMock
import pickle

from xavier.offline import BackgroudQueue

funcy_called = 0


def test_background_queue():
    publish_event = MagicMock()
    publish_event.return_value = 'aaa'

    background_queue = BackgroudQueue(publish_event)

    @background_queue.task
    def funcy():
        global funcy_called
        funcy_called += 1
        return "blah"

    assert funcy() == "blah"

    assert funcy.delay() is True

    event = pickle.dumps((funcy.path, (), {}))

    publish_event.assert_called_once_with(event)

    background_queue.process_event(event)
    assert funcy_called == 2
