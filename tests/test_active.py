from xavier.active import register_brain, get_active_brain, unregister_brain


def test_active():
    brain = 'a'

    assert None is get_active_brain()

    register_brain(brain)

    assert brain == get_active_brain()

    unregister_brain()

    assert None is get_active_brain()
