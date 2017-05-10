from xavier.active import register_bot, get_active_bot, unregister_bot


def test_active():
    bot = 'a'

    assert None is get_active_bot()

    register_bot(bot)

    assert bot == get_active_bot()

    unregister_bot()

    assert None is get_active_bot()
