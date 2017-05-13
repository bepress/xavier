from xavier.brain import Brain


def test_brain_name():
    assert Brain(name='test-bot').name == 'test-bot'
